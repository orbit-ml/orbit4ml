from datetime import datetime

from orbit4ml.sim.types import (
    EpochState,
    FaultState,
    LinkState,
    PowerState,
    SatelliteState,
    ThermalState,
)


def test_power_state_creation():
    ps = PowerState(available=True, watts=500.0)
    assert ps.available is True
    assert ps.watts == 500.0


def test_power_state_eclipse():
    ps = PowerState(available=False, watts=0.0)
    assert ps.available is False
    assert ps.watts == 0.0


def test_thermal_state_creation():
    ts = ThermalState(gpu_budget_watts=150.0, within_budget=True, radiator_efficiency=0.85)
    assert ts.gpu_budget_watts == 150.0
    assert ts.within_budget is True
    assert ts.radiator_efficiency == 0.85


def test_link_state_creation():
    ls = LinkState(active=[("sat-0", "sat-1"), ("sat-0", "sat-5")], bandwidth_mbps=100.0)
    assert len(ls.active) == 2
    assert ls.bandwidth_mbps == 100.0


def test_fault_state_creation():
    fs = FaultState(active=["seu", "thermal_shutdown"])
    assert "seu" in fs.active
    assert len(fs.active) == 2


def test_fault_state_no_faults():
    fs = FaultState(active=[])
    assert len(fs.active) == 0


def test_satellite_state_creation():
    sat = SatelliteState(
        id="sat-0",
        position_eci=(6878.0, 0.0, 0.0),
        power=PowerState(available=True, watts=500.0),
        thermal=ThermalState(gpu_budget_watts=150.0, within_budget=True, radiator_efficiency=0.85),
        links=LinkState(active=[], bandwidth_mbps=0.0),
        faults=FaultState(active=[]),
    )
    assert sat.id == "sat-0"
    assert sat.position_eci == (6878.0, 0.0, 0.0)


def test_epoch_state_creation():
    sat = SatelliteState(
        id="sat-0",
        position_eci=(6878.0, 0.0, 0.0),
        power=PowerState(available=True, watts=500.0),
        thermal=ThermalState(gpu_budget_watts=150.0, within_budget=True, radiator_efficiency=0.85),
        links=LinkState(active=[], bandwidth_mbps=0.0),
        faults=FaultState(active=[]),
    )
    epoch = EpochState(timestamp=datetime(2026, 6, 1), satellites=[sat])
    assert len(epoch.satellites) == 1
    assert epoch.timestamp.year == 2026
