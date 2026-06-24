import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "statics3d"))

from core import Load, solve
from supports import ball_and_socket, cable


def test_plate_equilibrium():
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

    assert answers["O_x"] == pytest.approx(-60.0)
    assert answers["O_y"] == pytest.approx(-50.0)
    assert answers["O_z"] == pytest.approx(240.0)
    assert answers["T_A"] == pytest.approx(60.0)
    assert answers["T_B"] == pytest.approx(256.125)
    assert answers["T_C"] == pytest.approx(64.031, abs=1e-2)
    



