"""SGP4-based orbit propagation for orbit4ml.sim.

Converts Keplerian elements to SGP4 satellite objects and propagates
positions over time. Returns ECI coordinates in km.
"""

import math
from datetime import datetime, timedelta

from sgp4.api import Satrec, WGS72, jday

EARTH_RADIUS_KM = 6371.0
MU_EARTH = 398600.4418  # km^3/s^2


def _keplerian_to_satrec(
    altitude: float,
    inclination: float,
    raan: float,
    true_anomaly: float,
    eccentricity: float,
    epoch: datetime,
) -> Satrec:
    """Convert Keplerian elements to an SGP4 Satrec object."""
    semi_major_axis = EARTH_RADIUS_KM + altitude
    n_rad_per_sec = math.sqrt(MU_EARTH / semi_major_axis**3)
    n_rad_per_min = n_rad_per_sec * 60.0

    sat = Satrec()
    sat.sgp4init(
        WGS72,
        "i",  # improved mode
        0,  # satnum
        (epoch - datetime(1949, 12, 31)).total_seconds() / 86400.0,  # epoch as days since 1949-12-31
        0.0,  # bstar drag
        0.0,  # ndot
        0.0,  # nddot
        eccentricity,
        math.radians(0.0),  # argument of perigee
        math.radians(inclination),
        math.radians(true_anomaly),  # mean anomaly (approx true anomaly for circular)
        n_rad_per_min,
        math.radians(raan),
    )
    return sat


def propagate_satellite(
    altitude: float,
    inclination: float,
    raan: float,
    true_anomaly: float,
    eccentricity: float,
    start: datetime,
    duration_hours: float,
    step_seconds: float,
) -> list[tuple[datetime, float, float, float]]:
    """Propagate a satellite and return ECI positions over time.

    Args:
        altitude: Altitude above Earth's surface in km.
        inclination: Orbital inclination in degrees.
        raan: Right ascension of ascending node in degrees.
        true_anomaly: True anomaly in degrees.
        eccentricity: Orbital eccentricity.
        start: Propagation start time (UTC).
        duration_hours: Duration to propagate in hours.
        step_seconds: Time step in seconds.

    Returns:
        List of (timestamp, x_km, y_km, z_km) tuples in ECI frame.
    """
    sat = _keplerian_to_satrec(altitude, inclination, raan, true_anomaly, eccentricity, start)

    positions = []
    total_seconds = duration_hours * 3600.0
    num_steps = int(total_seconds / step_seconds) + 1

    for i in range(num_steps):
        dt = start + timedelta(seconds=step_seconds * i)
        jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond / 1e6)
        e, r, v = sat.sgp4(jd, fr)
        if e != 0:
            continue
        positions.append((dt, r[0], r[1], r[2]))

    return positions
