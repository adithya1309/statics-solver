import numpy as np
from core import Unknown

def ball_and_socket(point, name):
    x = Unknown(point, (1, 0, 0), f"{name}_x")
    y = Unknown(point, (0, 1, 0), f"{name}_y")
    z = Unknown(point, (0, 0, 1), f"{name}_z")
    unknowns = [x, y, z]
    return unknowns

def cable(point, target, name):
    target = np.array(target)
    point = np.array(point)
    direct = target - point
    unknown = Unknown(point, direct, name)
    unknowns = [unknown]
    return unknowns

def roller(point, normal, name):
    unknown = Unknown(point, normal, name)
    unknowns = [unknown]
    return unknowns


