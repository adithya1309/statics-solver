import sys
import os

# Make the statics3d/ folder importable (so `from core import ...` works
# regardless of where you run this script from).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "statics3d"))

from core import Load, solve
from supports import ball_and_socket, cable

# --- Problem setup: weighted plate, ball-and-socket at O + 3 cables ---

# 600 N weight acting downward at the plate's center G.
weight = Load((3, 2, 0), (0, 0, -600))

# 6 unknowns: 3 from the socket + 3 cable tensions.
unknowns = (
    ball_and_socket((0, 0, 0), "O")
    + cable((6, 0, 0), (6, 0, 5), "T_A")
    + cable((6, 4, 0), (8, 5, 6), "T_B")
    + cable((0, 4, 0), (-2, 5, 6), "T_C")
)

answers = solve([weight], unknowns)

for name, value in answers.items():
    print(f"{name:6s} = {value:10.3f}")
