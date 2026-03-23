import math
from datetime import datetime

from orbit4ml.sim.sun import sun_position_eci


def test_sun_position_returns_tuple():
    pos = sun_position_eci(datetime(2026, 6, 21, 12, 0, 0))
    assert isinstance(pos, tuple)
    assert len(pos) == 3


def test_sun_distance_approximately_1au():
    pos = sun_position_eci(datetime(2026, 6, 21, 12, 0, 0))
    dist = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
    assert 1.46e8 < dist < 1.53e8


def test_sun_position_changes_over_year():
    summer = sun_position_eci(datetime(2026, 6, 21))
    winter = sun_position_eci(datetime(2026, 12, 21))
    assert summer != winter
