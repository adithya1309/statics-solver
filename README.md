# statics3d

A Python library that solves **3D rigid-body equilibrium** problems — the kind you work by hand i had to do in my statics course where you would have to manually set up a system fo equations and solve.

## The idea

A rigid body is in equilibrium when the forces and moments on it sum to zero. In 3D that's six scalar equations:

```
ΣFx = 0    ΣMx = 0
ΣFy = 0    ΣMy = 0
ΣFz = 0    ΣMz = 0
```

Some forces are **known** (applied loads, weights); some are **unknown** (support and cable reactions). `statics3d` collects every force, splits known from unknown, and builds a linear system `A · x = b` where `x` is the vector of unknown reactions. Solving it with NumPy gives the reactions, and a built-in residual check plugs the answer back in to confirm actually in equilibrium. 

A properly constrained body in 3D has exactly **6 unknown reaction components**, so `A` is 6×6 and solvable directly.

## Install

```bash
pip install -r requirements.txt
```

## Usage

A rectangular plate lies flat, supported by a ball-and-socket at one corner and three cables, carrying a 600 N weight at its center:

```python
from core import Load, solve
from supports import ball_and_socket, cable

# 600 N weight acting downward at the plate's center
weight = Load((3, 2, 0), (0, 0, -600))

# 6 unknowns: 3 from the ball-and-socket + 3 cable tensions
unknowns = (
    ball_and_socket((0, 0, 0), "O")
    + cable((6, 0, 0), (6, 0, 5), "T_A")
    + cable((6, 4, 0), (8, 5, 6), "T_B")
    + cable((0, 4, 0), (-2, 5, 6), "T_C")
)

answers = solve([weight], unknowns)
for name, value in answers.items():
    print(f"{name:6s} = {value:10.3f}")
```

Output:

```
O_x    =    -60.000
O_y    =    -50.000
O_z    =    240.000
T_A    =     60.000
T_B    =    256.125
T_C    =     64.031
```

A full runnable version is in [`examples/plate.py`](examples/plate.py).

## Supports

| Function | Unknowns | Models |
|----------|----------|--------|
| `ball_and_socket(point, name)` | 3 (force in x, y, z) | a joint that resists force in any direction, no moment |
| `cable(point, target, name)` | 1 (tension) | a cable that pulls along its length toward its anchor |
| `roller(point, normal, name)` | 1 (normal force) | a roller / smooth surface that pushes perpendicular to itself |

Each returns a list of `Unknown`s, so a full problem is built by concatenating them with `+`.

## Running the tests

```bash
pytest -v
```

Tests verify the solver against known textbook answers.

## Project structure

```
statics3d/
├── statics3d/
│   ├── core.py        # Load, Unknown, assemble(), solve() + residual check
│   └── supports.py    # ball_and_socket, cable, roller
├── examples/          # worked, verified problems
├── tests/             # answers checked against known values
├── requirements.txt
└── README.md
```

## Scope and limitations

- **Single rigid body**, statically determinate (exactly 6 unknowns).
- **Force-only reactions.** Supports that resist with a moment/couple (fixed/built-in supports, some bearings) aren't modeled yet — that needs a moment-type unknown.
- No trusses / multi-body systems (a possible future extension).
```