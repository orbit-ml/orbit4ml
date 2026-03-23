"""Cylindrical shadow eclipse model for orbit4ml.sim.

Determines whether a satellite is in Earth's shadow using a
cylindrical shadow approximation. The shadow is modeled as an
infinite cylinder with Earth's radius, extending away from the Sun.
"""

import math

EARTH_RADIUS_KM = 6371.0


def is_in_eclipse(
    sat_eci: tuple[float, float, float],
    sun_eci: tuple[float, float, float],
) -> bool:
    """Check if a satellite is in Earth's cylindrical shadow.

    Args:
        sat_eci: Satellite position (x, y, z) in km, ECI frame.
        sun_eci: Sun position (x, y, z) in km, ECI frame.

    Returns:
        True if the satellite is in eclipse (Earth's shadow).
    """
    sun_dist = math.sqrt(sun_eci[0] ** 2 + sun_eci[1] ** 2 + sun_eci[2] ** 2)
    sun_dir = (sun_eci[0] / sun_dist, sun_eci[1] / sun_dist, sun_eci[2] / sun_dist)

    dot = sat_eci[0] * sun_dir[0] + sat_eci[1] * sun_dir[1] + sat_eci[2] * sun_dir[2]

    if dot >= 0:
        return False

    proj_x = dot * sun_dir[0]
    proj_y = dot * sun_dir[1]
    proj_z = dot * sun_dir[2]

    perp_x = sat_eci[0] - proj_x
    perp_y = sat_eci[1] - proj_y
    perp_z = sat_eci[2] - proj_z

    perp_dist = math.sqrt(perp_x**2 + perp_y**2 + perp_z**2)

    return perp_dist < EARTH_RADIUS_KM
