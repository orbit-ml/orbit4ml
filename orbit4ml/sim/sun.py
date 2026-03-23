"""Approximate Sun position in ECI frame for orbit4ml.sim.

Uses a low-precision solar position algorithm sufficient for eclipse
determination. Based on the Astronomical Almanac's approximate formula.
"""

import math
from datetime import datetime


def sun_position_eci(dt: datetime) -> tuple[float, float, float]:
    """Compute approximate Sun position in ECI coordinates.

    Args:
        dt: UTC datetime.

    Returns:
        (x, y, z) Sun position in km, ECI frame.
    """
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jd = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    jd += (dt.hour - 12) / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0

    n = jd - 2451545.0

    L = (280.460 + 0.9856474 * n) % 360.0
    g = math.radians((357.528 + 0.9856003 * n) % 360.0)

    ecliptic_lon = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))

    obliquity = math.radians(23.439 - 0.0000004 * n)

    R_au = 1.00014 - 0.01671 * math.cos(g) - 0.00014 * math.cos(2 * g)
    R_km = R_au * 149597870.7

    x = R_km * math.cos(ecliptic_lon)
    y = R_km * math.cos(obliquity) * math.sin(ecliptic_lon)
    z = R_km * math.sin(obliquity) * math.sin(ecliptic_lon)

    return (x, y, z)
