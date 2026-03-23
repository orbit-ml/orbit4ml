from datetime import datetime

from orbit4ml.sim.constellation import Constellation
from orbit4ml.sim.twin import DigitalTwin
from orbit4ml.sim.types import EpochState, SatelliteState


def test_digital_twin_creation():
    c = Constellation(planes=1, sats_per_plane=2, altitude=550, inclination=53.0)
    twin = DigitalTwin(c)
    assert twin is not None


def test_propagate_yields_epoch_states():
    c = Constellation(planes=1, sats_per_plane=1, altitude=550, inclination=53.0)
    twin = DigitalTwin(c)
    epochs = list(twin.propagate(start=datetime(2026, 6, 1), hours=0.1, step_seconds=60))
    assert len(epochs) > 0
    assert all(isinstance(e, EpochState) for e in epochs)


def test_propagate_correct_step_count():
    c = Constellation(planes=1, sats_per_plane=1, altitude=550, inclination=53.0)
    twin = DigitalTwin(c)
    epochs = list(twin.propagate(start=datetime(2026, 6, 1), hours=1.0, step_seconds=60))
    assert len(epochs) == 61


def test_each_epoch_has_correct_satellite_count():
    c = Constellation(planes=2, sats_per_plane=3, altitude=550, inclination=53.0)
    twin = DigitalTwin(c)
    for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=0.05, step_seconds=60):
        assert len(epoch.satellites) == 6


def test_satellite_states_have_all_fields():
    c = Constellation(planes=1, sats_per_plane=1, altitude=550, inclination=53.0)
    twin = DigitalTwin(c)
    epoch = next(iter(twin.propagate(start=datetime(2026, 6, 1), hours=0.1, step_seconds=60)))
    sat = epoch.satellites[0]
    assert isinstance(sat, SatelliteState)
    assert sat.id is not None
    assert sat.position_eci is not None
    assert sat.power is not None
    assert sat.thermal is not None
    assert sat.links is not None
    assert sat.faults is not None


def test_propagate_default_start():
    c = Constellation(planes=1, sats_per_plane=1, altitude=550, inclination=53.0)
    twin = DigitalTwin(c)
    epochs = list(twin.propagate(hours=0.05, step_seconds=60))
    assert len(epochs) > 0


def test_iss_orbit_eclipse_intervals():
    """ISS-like orbit should produce eclipse periods within expected range."""
    c = Constellation(planes=1, sats_per_plane=1, altitude=408, inclination=51.6)
    twin = DigitalTwin(c)
    epochs = list(twin.propagate(start=datetime(2026, 6, 1), hours=3.0, step_seconds=30))

    eclipse_seconds = sum(
        30 for e in epochs if not e.satellites[0].power.available
    )

    eclipse_minutes = eclipse_seconds / 60.0
    assert 40 < eclipse_minutes < 100, f"eclipse was {eclipse_minutes} min in 3 hours"
