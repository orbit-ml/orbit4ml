from orbit4ml.sim.isl import compute_link_state
from orbit4ml.sim.types import LinkState

EARTH_RADIUS_KM = 6371.0


def test_close_satellites_have_link():
    sat_positions = {
        "sat-0": (EARTH_RADIUS_KM + 550, 0.0, 0.0),
        "sat-1": (EARTH_RADIUS_KM + 549, 50.0, 0.0),
    }
    state = compute_link_state("sat-0", sat_positions)
    assert isinstance(state, LinkState)
    assert len(state.active) == 1
    assert state.bandwidth_mbps > 0


def test_distant_satellites_no_link():
    sat_positions = {
        "sat-0": (EARTH_RADIUS_KM + 550, 0.0, 0.0),
        "sat-1": (-(EARTH_RADIUS_KM + 550), 0.0, 0.0),
    }
    state = compute_link_state("sat-0", sat_positions)
    assert len(state.active) == 0
    assert state.bandwidth_mbps == 0.0


def test_single_satellite_no_links():
    sat_positions = {"sat-0": (EARTH_RADIUS_KM + 550, 0.0, 0.0)}
    state = compute_link_state("sat-0", sat_positions)
    assert len(state.active) == 0


def test_link_state_contains_correct_ids():
    sat_positions = {
        "sat-0": (EARTH_RADIUS_KM + 550, 0.0, 0.0),
        "sat-1": (EARTH_RADIUS_KM + 550, 10.0, 0.0),
    }
    state = compute_link_state("sat-0", sat_positions)
    assert ("sat-0", "sat-1") in state.active


def test_bandwidth_decreases_with_distance():
    close = {
        "sat-0": (EARTH_RADIUS_KM + 550, 0.0, 0.0),
        "sat-1": (EARTH_RADIUS_KM + 550, 100.0, 0.0),
    }
    far = {
        "sat-0": (EARTH_RADIUS_KM + 550, 0.0, 0.0),
        "sat-1": (EARTH_RADIUS_KM + 550, 2000.0, 0.0),
    }
    close_state = compute_link_state("sat-0", close)
    far_state = compute_link_state("sat-0", far)
    assert close_state.bandwidth_mbps > far_state.bandwidth_mbps
