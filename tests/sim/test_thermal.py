from orbit4ml.sim.thermal import compute_thermal_state
from orbit4ml.sim.types import ThermalState


def test_sunlit_thermal_state():
    state = compute_thermal_state(in_eclipse=False)
    assert isinstance(state, ThermalState)
    assert 0.0 < state.radiator_efficiency < 1.0
    assert state.gpu_budget_watts > 0


def test_eclipse_thermal_state():
    state = compute_thermal_state(in_eclipse=True)
    assert isinstance(state, ThermalState)
    assert state.radiator_efficiency > 0.5


def test_eclipse_has_higher_efficiency_than_sunlit():
    sunlit = compute_thermal_state(in_eclipse=False)
    eclipse = compute_thermal_state(in_eclipse=True)
    assert eclipse.radiator_efficiency > sunlit.radiator_efficiency


def test_eclipse_has_higher_gpu_budget():
    sunlit = compute_thermal_state(in_eclipse=False)
    eclipse = compute_thermal_state(in_eclipse=True)
    assert eclipse.gpu_budget_watts > sunlit.gpu_budget_watts


def test_within_budget_default():
    state = compute_thermal_state(in_eclipse=False)
    assert state.within_budget is True
