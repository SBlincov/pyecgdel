import numpy as np


def unit_vector(vector):
    """ Returns the unit vector of the vector. """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

    »> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    »> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    »> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def distance_point_to_line(p0, p1, p2):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    nom = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denom = pow((pow((y2 - y1), 2.0) + pow((x2 - x1), 2.0)), 0.5)
    result = nom / denom
    return result