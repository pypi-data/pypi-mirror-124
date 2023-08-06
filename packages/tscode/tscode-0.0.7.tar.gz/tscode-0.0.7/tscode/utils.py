# coding=utf-8
'''

TSCODE: Transition State Conformational Docker
Copyright (C) 2021 Nicolò Tampellini

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''

import os
import sys
from subprocess import CalledProcessError, run

import networkx as nx
import numpy as np
from periodictable import core, covalent_radius, mass
from scipy.spatial.transform import Rotation as R

from tscode.errors import TriangleError
from tscode.fast_algebra import norm, norm_of

pt = core.PeriodicTable(table="H=1")
covalent_radius.init(pt)
mass.init(pt)


class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def clean_directory():
    for f in os.listdir():
        if f.split('.')[0] == 'temp':
            os.remove(f)
        elif f.startswith('temp_'):
            os.remove(f)

def run_command(command:str, p=False):
    if p:
        print("Command: {}".format(command))
    result = run(command.split(), shell=False, capture_output=True)
    if result.stderr:
        raise CalledProcessError(
                returncode = result.returncode,
                cmd = result.args,
                stderr = result.stderr
                )
    if p and result.stdout:
        print("Command Result: {}".format(result.stdout.decode('utf-8')))
    return result

def write_xyz(coords:np.array, atomnos:np.array, output, title='temp'):
    '''
    output is of _io.TextIOWrapper type

    '''
    assert atomnos.shape[0] == coords.shape[0]
    assert coords.shape[1] == 3
    string = ''
    string += str(len(coords))
    string += f'\n{title}\n'
    for i, atom in enumerate(coords):
        string += '%s     % .6f % .6f % .6f\n' % (pt[atomnos[i]].symbol, atom[0], atom[1], atom[2])
    output.write(string)

def time_to_string(total_time: float, verbose=False):
    '''
    Converts totaltime (float) to a timestring
    with hours, minutes and seconds.
    '''
    timestring = ''

    names = ('hours', 'minutes', 'seconds') if verbose else ('h', 'm', 's')

    if total_time > 3600:
        h = total_time // 3600
        timestring += f'{int(h)} {names[0]} '
        total_time %= 3600
    if total_time > 60:
        m = total_time // 60
        timestring += f'{int(m)} {names[1]} '
        total_time %= 60
    timestring += f'{round(total_time, 3)} {names[2]}'

    return timestring

def loadbar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='#'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

def dihedral(p):
    '''
    Returns dihedral angle in degrees from 4 3D vecs
    Praxeolitic formula: 1 sqrt, 1 cross product
    
    '''
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    p3 = p[3]

    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2

    # normalize b1 so that it does not influence magnitude of vector
    # rejections that come next
    b1 /= norm_of(b1)

    # vector rejections
    # v = projection of b0 onto plane perpendicular to b1
    #   = b0 minus component that aligns with b1
    # w = projection of b2 onto plane perpendicular to b1
    #   = b2 minus component that aligns with b1
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1

    # angle between v and w in a plane is the torsion angle
    # v and w may not be normalized but that's fine since tan is y/x
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    
    return np.degrees(np.arctan2(y, x))

def vec_angle(v1, v2):
    v1_u = norm(v1)
    v2_u = norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))*180/np.pi

def point_angle(p1, p2, p3):
    return np.arccos(np.clip(norm(p1 - p2) @ norm(p3 - p2), -1.0, 1.0))*180/np.pi

def cartesian_product(*arrays):
    return np.stack(np.meshgrid(*arrays), -1).reshape(-1, len(arrays))

def rotation_matrix_from_vectors(vec1, vec2):
    """
    Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.

    """
    assert vec1.shape == (3,)
    assert vec2.shape == (3,)

    a, b = (vec1 / norm_of(vec1)).reshape(3), (vec2 / norm_of(vec2)).reshape(3)
    v = np.cross(a, b)
    if norm_of(v) != 0:
        c = np.dot(a, b)
        s = norm_of(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
        return rotation_matrix
    
    # if the cross product is zero, then vecs must be parallel or perpendicular
    if norm_of(a + b) == 0:
        pointer = np.array([0,0,1])
        return rot_mat_from_pointer(pointer, 180)
        
    return np.eye(3)

def rot_mat_from_pointer(pointer, angle):
    '''
    Returns the rotation matrix that rotates a system around the given pointer
    of angle degrees. The algorithm is based on scipy quaternions.
    :params pointer: a 3D vector
    :params angle: an int/float, in degrees
    :return rotation_matrix: matrix that applied to a point, rotates it along the pointer
    '''
    assert pointer.shape[0] == 3

    pointer = norm(pointer)
    angle *= np.pi/180
    quat = np.array([np.sin(angle/2)*pointer[0],
                    np.sin(angle/2)*pointer[1],
                    np.sin(angle/2)*pointer[2],
                    np.cos(angle/2)])            # normalized quaternion, scalar last (i j k w)
    
    return R.from_quat(quat).as_matrix()

def polygonize(lengths):
    '''
    Returns coordinates for the polygon vertexes used in cyclical TS construction,
    as a list of vector couples specifying starting and ending point of each pivot 
    vector. For bimolecular TSs, returns vertexes for the centered superposition of
    two segments. For trimolecular TSs, returns triangle vertexes.

    :params vertexes: list of floats, used as polygon side lenghts.
    :return vertexes_out: list of vectors couples (start, end)
    '''
    assert len(lengths) in (2,3)

    arr = np.zeros((len(lengths),2,3))

    if len(lengths) == 2:

        arr[0,0] = np.array([-lengths[0]/2,0,0])
        arr[0,1] = np.array([+lengths[0]/2,0,0])
        arr[1,0] = np.array([-lengths[1]/2,0,0])
        arr[1,1] = np.array([+lengths[1]/2,0,0])

        vertexes_out = np.vstack(([arr],[arr]))
        vertexes_out[1,1] *= -1

    else:
        
        if not all([lengths[i] < lengths[i-1] + lengths[i-2] for i in (0,1,2)]): 
            raise TriangleError(f'Impossible to build a triangle with sides {lengths}')
            # check that we can build a triangle with the specified vectors

        arr[0,1] = np.array([lengths[0],0,0])
        arr[1,0] = np.array([lengths[0],0,0])

        a = np.power(lengths[0], 2)
        b = np.power(lengths[1], 2)
        c = np.power(lengths[2], 2)
        x = (a-b+c)/(2*a**0.5)
        y = (c-x**2)**0.5

        arr[1,1] = np.array([x,y,0])
        arr[2,0] = np.array([x,y,0])

        vertexes_out = np.vstack(([arr],[arr],[arr],[arr],
                                  [arr],[arr],[arr],[arr]))

        swaps = [(1,2),(2,1),(3,1),(3,2),(4,0),(5,0),(5,1),(6,0),(6,2),(7,0),(7,1),(7,2)]

        for t,v in swaps:
            # triangle, vector couples to be swapped
            vertexes_out[t,v][[0,1]] = vertexes_out[t,v][[1,0]]

    return vertexes_out

def ase_view(mol):
    '''
    Display an Hypermolecule instance from the ASE GUI
    '''
    from ase import Atoms
    from ase.gui.gui import GUI
    from ase.gui.images import Images

    if mol.hyper:
        images = []

        for c, coords in enumerate(mol.atomcoords):
            centers = np.vstack([atom.center for atom in mol.reactive_atoms_classes_dict[c].values()])
            atomnos = np.concatenate((mol.atomnos, [0 for _ in centers]))
            totalcoords = np.concatenate((coords, centers))
            images.append(Atoms(atomnos, positions=totalcoords))

    else:
        images = [Atoms(mol.atomnos, positions=coords) for coords in mol.atomcoords]
        
    GUI(images=Images(images), show_bonds=True).run()

double_bonds_thresholds_dict = {
    'CC':1.4,
    'CN':1.3,
}

def get_double_bonds_indexes(coords, atomnos):
    '''
    Returns a list containing 2-elements lists
    of indexes involved in any double bond
    '''
    mask = (atomnos != 1)
    numbering = np.arange(len(coords))[mask]
    coords = coords[mask]
    atomnos = atomnos[mask]
    output = []

    for i1, _ in enumerate(coords):
        for i2 in range(i1+1, len(coords)):
            dist = norm_of(coords[i1] - coords[i2])
            tag = ''.join(sorted([pt[atomnos[i1]].symbol,
                                  pt[atomnos[i2]].symbol]))
            
            threshold = double_bonds_thresholds_dict.get(tag)
            if threshold is not None and dist < threshold:
                output.append([numbering[i1], numbering[i2]])

    return output

def findPaths(G, u, n, excludeSet = None):
    '''
    Recursively find all paths of a NetworkX
    graph G with length = n, starting from node u
    '''
    if excludeSet is None:
        excludeSet = set([u])

    else:
        excludeSet.add(u)

    if n == 0:
        return [[u]]

    paths = [[u]+path for neighbor in G.neighbors(u) if neighbor not in excludeSet for path in findPaths(G,neighbor,n-1,excludeSet)]
    excludeSet.remove(u)

    return paths

def neighbors(graph, index):
    neighbors = list([(a, b) for a, b in graph.adjacency()][index][1].keys())
    neighbors.remove(index)
    return neighbors

def is_sigmatropic(mol, conf):
    '''
    mol: Hypermolecule object
    conf: conformer index

    A hypermolecule is considered sigmatropic when:
    - has 2 reactive atoms
    - they are of sp2 or analogous types
    - they are connected, or at least one path connecting them
      is made up of atoms that do not make more than three bonds each
    - they are less than 3 A apart (cisoid propenal makes it, transoid does not)

    Used to set the mol.sigmatropic attribute, that affects orbital
    building (p or n lobes) for Ketone and Imine reactive atoms classes.
    '''
    sp2_types = (
                'Ketone',
                'Imine',
                'sp2',
                'sp',
                'bent carbene'
                )
    if len(mol.reactive_indexes) == 2:

        i1, i2 = mol.reactive_indexes
        if norm_of(mol.atomcoords[conf][i1] - mol.atomcoords[conf][i2]) < 3:

            if all([str(r_atom) in sp2_types for r_atom in mol.reactive_atoms_classes_dict[conf].values()]):

                paths = nx.all_simple_paths(mol.graph, i1, i2)

                for path in paths:
                    path = path[1:-1]

                    full_sp2 = True
                    for index in path:
                        if len(neighbors(mol.graph, index))-2 > 1:
                            full_sp2 = False
                            break

                    if full_sp2:
                        return True
    return False

def is_vicinal(mol):
    '''
    A hypermolecule is considered vicinal when:
    - has 2 reactive atoms
    - they are of sp3 or Single Bond type
    - they are bonded

    Used to set the mol.sp3_sigmastar attribute, that affects orbital
    building (BH4 or agostic-like behavior) for Sp3 and Single Bond reactive atoms classes.
    '''
    vicinal_types = (
                'sp3',
                'Single Bond',
                )

    if len(mol.reactive_indexes) == 2:

        i1, i2 = mol.reactive_indexes

        if all([str(r_atom) in vicinal_types for r_atom in mol.reactive_atoms_classes_dict[0].values()]):
            if i1 in neighbors(mol.graph, i2):
                return True

    return False

def molecule_check(old_coords, new_coords, atomnos, max_newbonds=0):
    '''
    Checks if two molecules have the same bonds between the same atomic indexes
    '''
    old_bonds = {(a, b) for a, b in list(graphize(old_coords, atomnos).edges) if a != b}
    new_bonds = {(a, b) for a, b in list(graphize(new_coords, atomnos).edges) if a != b}

    delta_bonds = (old_bonds | new_bonds) - (old_bonds & new_bonds)

    if len(delta_bonds) > max_newbonds:
        return False

    return True

def scramble_check(TS_structure, TS_atomnos, constrained_indexes, mols_graphs, max_newbonds=0) -> bool:
    '''
    Check if a transition state structure has scrambled during some optimization
    steps. If more than a given number of bonds changed (formed or broke) the
    structure is considered scrambled, and the method returns False.
    '''
    assert len(TS_structure) == sum([len(graph.nodes) for graph in mols_graphs])

    bonds = set()
    for i, graph in enumerate(mols_graphs):

        pos = 0
        while i != 0:
            pos += len(mols_graphs[i-1].nodes)
            i -= 1

        for bond in [tuple(sorted((a+pos, b+pos))) for a, b in list(graph.edges) if a != b]:
            bonds.add(bond)
    # creating bond set containing all bonds present in the desired transition state

    new_bonds = {tuple(sorted((a, b))) for a, b in list(graphize(TS_structure, TS_atomnos).edges) if a != b}
    delta_bonds = (bonds | new_bonds) - (bonds & new_bonds)
    # delta_bonds -= {tuple(sorted(pair)) for pair in constrained_indexes}

    for bond in delta_bonds.copy():
        for a1, a2 in constrained_indexes:
            if (a1 in bond) or (a2 in bond):
                delta_bonds -= {bond}
    # removing bonds involving constrained atoms: they are not counted as scrambled bonds

    if len(delta_bonds) > max_newbonds:
        return False

    return True

def d_min_bond(e1, e2):
    return 1.2 * (pt[e1].covalent_radius + pt[e2].covalent_radius)
    # return 0.2 + (pt[e1].covalent_radius + pt[e2].covalent_radius)
# if this is somewhat prone to bugs, this might help https://cccbdb.nist.gov/calcbondcomp1x.asp

def graphize(coords, atomnos, mask=None):
    '''
    :params coords: atomic coordinates as 3D vectors
    :params atomnos: atomic numbers as a list
    :params mask: bool array, with False for atoms
                  to be excluded in the bond evaluation
    :return connectivity graph
    '''

    mask = np.array([True for _ in atomnos], dtype=bool) if mask is None else mask

    matrix = np.zeros((len(coords),len(coords)))
    for i, _ in enumerate(coords):
        for j in range(i,len(coords)):
            if mask[i] and mask[j]:
                if norm_of(coords[i]-coords[j]) < d_min_bond(atomnos[i], atomnos[j]):
                    matrix[i][j] = 1

    graph = nx.from_numpy_matrix(matrix)
    nx.set_node_attributes(graph, dict(enumerate(atomnos)), 'atomnos')

    return graph

def rotate_dihedral(coords, dihedral, angle, mask=None, indexes_to_be_moved=None):
    '''
    Rotate a molecule around a given bond.
    Atoms that will move are the ones
    specified by mask or indexes_to_be_moved.
    If both are None, only the first index of
    the dihedral iterable is moved.

    angle: angle, in degrees
    '''

    i1, i2, i3 ,_ = dihedral

    if indexes_to_be_moved is not None:
        mask = np.array([i in indexes_to_be_moved for i, _ in enumerate(coords)])

    if mask is None:
        mask = i1

    axis = coords[i2] - coords[i3]
    mat = rot_mat_from_pointer(axis, angle)
    center = coords[i3]

    coords[mask] = (mat @ (coords[mask] - center).T).T + center

    return coords