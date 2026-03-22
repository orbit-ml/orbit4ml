import math
from datetime import datetime, timedelta

from orbit4ml.sim.propagator import propagate_satellite


def test_propagate_returns_positions():
    positions = propagate_satellite(
        altitude=550, inclination=53.0, raan=0.0, true_anomaly=0.0,
        eccentricity=0.0, start=datetime(2026, 6, 1),
        duration_hours=1.0, step_seconds=600,
    )
    assert len(positions) == 7


def test_propagate_altitude_reasonable():
    positions = propagate_satellite(
        altitude=550, inclination=53.0, raan=0.0, true_anomaly=0.0,
        eccentricity=0.0, start=datetime(2026, 6, 1),
        duration_hours=0.1, step_seconds=60,
    )
    for ts, x, y, z in positions:
        r = math.sqrt(x**2 + y**2 + z**2)
        assert 6800 < r < 7100, f"radius {r} km out of expected range"


def test_propagate_position_changes():
    positions = propagate_satellite(
        altitude=550, inclination=53.0, raan=0.0, true_anomaly=0.0,
        eccentricity=0.0, start=datetime(2026, 6, 1),
        duration_hours=0.5, step_seconds=300,
    )
    first = positions[0]
    last = positions[-1]
    assert first[1:] != last[1:]


def test_propagate_timestamps_correct():
    start = datetime(2026, 6, 1)
    positions = propagate_satellite(
        altitude=550, inclination=53.0, raan=0.0, true_anomaly=0.0,
        eccentricity=0.0, start=start,
        duration_hours=0.5, step_seconds=300,
    )
    for i, (ts, x, y, z) in enumerate(positions):
        expected_ts = start + timedelta(seconds=300 * i)
        assert ts == expected_ts
