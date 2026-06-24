import numpy as np

class Load:
    def __init__(self, point, force):
        self.point = np.array(point, dtype=float)
        self.force = np.array(force, dtype=float)
    def __repr__(self):
        return f"Load(point={self.point}, force={self.force})"

class Unknown:
    def __init__(self, point, direction, name):
        self.point = np.array(point, dtype=float)
        direction = np.array(direction, dtype=float)
        length = np.linalg.norm(direction)
        if length == 0:
            raise ValueError("Unknown direction cannot be zero-length")
        self.direction = direction / length
        self.name = name
    def __repr__(self):
        return f"Unknown(point={self.point}, direction={self.direction}, name={self.name})"

# Creating matrices
def assemble(loads, unknowns):
    A = np.zeros((6, len(unknowns)))
    for j, u in enumerate(unknowns):
        A[0:3, j] = u.direction
        A[3:6, j] = np.cross(u.point, u.direction)
    b = np.zeros(6)
    for load in loads:
        b[0:3] += load.force
        b[3:6] += np.cross(load.point, load.force)
    b = -b
    return A, b

# Solving A·x = b, x is list of 6 unknown reaction components
def solve(loads, unknowns):
    if len(unknowns) != 6:
        raise ValueError("Matrix must be 6x6")
    A, b = assemble(loads, unknowns)
    x = np.linalg.solve(A, b)
    answers = {u.name: x[i] for i, u in enumerate(unknowns)}
    residual = A @ x - b
    if not np.allclose(residual, 0, atol=1e-6):
        raise ValueError("Equilibrium not satisified, residual = {residual}")
    return answers




