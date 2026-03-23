"""Inter-satellite link (ISL) model for orbit4ml.sim.

v0.1: distance-based link availability with line-of-sight check.
Doppler shift modeling is deferred to v0.3+.
"""

import math

from orbit4ml.sim.types import LinkState

EARTH_RADIUS_KM = 6371.0
MAX_LINK_DISTANCE_KM = 5000.0
MAX_BANDWIDTH_MBPS = 1000.0


def _distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def _has_line_of_sight(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> bool:
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    seg_len_sq = dx * dx + dy * dy + dz * dz
    if seg_len_sq == 0:
        return True
    t = -(a[0] * dx + a[1] * dy + a[2] * dz) / seg_len_sq
    t = max(0.0, min(1.0, t))
    cx = a[0] + t * dx
    cy = a[1] + t * dy
    cz = a[2] + t * dz
    closest_dist = math.sqrt(cx * cx + cy * cy + cz * cz)
    return closest_dist > EARTH_RADIUS_KM


def compute_link_state(
    sat_id: str,
    all_positions: dict[str, tuple[float, float, float]],
) -> LinkState:
    sat_pos = all_positions[sat_id]
    active = []
    total_bandwidth = 0.0

    for peer_id, peer_pos in all_positions.items():
        if peer_id == sat_id:
            continue
        dist = _distance(sat_pos, peer_pos)
        if dist > MAX_LINK_DISTANCE_KM:
            continue
        if not _has_line_of_sight(sat_pos, peer_pos):
            continue
        active.append((sat_id, peer_id))
        bandwidth = MAX_BANDWIDTH_MBPS * (1.0 - (dist / MAX_LINK_DISTANCE_KM) ** 2)
        total_bandwidth += max(0.0, bandwidth)

    return LinkState(active=active, bandwidth_mbps=total_bandwidth)
