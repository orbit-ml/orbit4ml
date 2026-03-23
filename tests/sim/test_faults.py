from orbit4ml.sim.faults import FaultInjector
from orbit4ml.sim.types import FaultState


def test_no_faults_by_default():
    injector = FaultInjector(seed=42)
    state = injector.sample()
    assert isinstance(state, FaultState)
    assert isinstance(state.active, list)


def test_deterministic_with_seed():
    inj1 = FaultInjector(seed=42)
    inj2 = FaultInjector(seed=42)
    results1 = [inj1.sample() for _ in range(100)]
    results2 = [inj2.sample() for _ in range(100)]
    for r1, r2 in zip(results1, results2):
        assert r1.active == r2.active


def test_faults_are_valid_types():
    injector = FaultInjector(seed=0, seu_rate=1.0, thermal_shutdown_rate=1.0, link_failure_rate=1.0)
    state = injector.sample()
    valid_types = {"seu", "thermal_shutdown", "link_failure"}
    for fault in state.active:
        assert fault in valid_types


def test_high_rate_produces_faults():
    injector = FaultInjector(seed=42, seu_rate=1.0)
    state = injector.sample()
    assert "seu" in state.active


def test_zero_rate_produces_no_faults():
    injector = FaultInjector(seed=42, seu_rate=0.0, thermal_shutdown_rate=0.0, link_failure_rate=0.0)
    for _ in range(100):
        state = injector.sample()
        assert len(state.active) == 0
