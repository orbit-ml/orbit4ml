"""Integration test: full orbit4ml MVP experiment loop.

Verifies that sim + data work together end-to-end.
Does NOT download EuroSAT — uses synthetic data to keep CI fast.
"""

from datetime import datetime

import torch

from orbit4ml.sim import Constellation, DigitalTwin


def test_full_mvp_loop():
    """Run the complete MVP example from the spec."""
    constellation = Constellation(
        planes=1, sats_per_plane=2, altitude=550, inclination=53.0
    )
    twin = DigitalTwin(constellation)

    model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(3 * 64 * 64, 10))
    optimizer = torch.optim.Adam(model.parameters())

    steps_run = 0
    sunlit_steps = 0
    eclipse_steps = 0

    for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=0.17, step_seconds=60):
        for sat in epoch.satellites:
            steps_run += 1
            if sat.power.available and sat.thermal.within_budget:
                sunlit_steps += 1
                batch_x = torch.randn(4, 3, 64, 64)
                batch_y = torch.randint(0, 10, (4,))
                loss = torch.nn.functional.cross_entropy(model(batch_x), batch_y)
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            else:
                eclipse_steps += 1

    assert steps_run > 0, "should have run at least one step"
    assert sunlit_steps > 0, "expected some sunlit steps"


def test_sim_types_accessible_from_top_level():
    """Verify the public API is accessible via orbit4ml.sim."""
    from orbit4ml.sim import (
        Constellation,
        DigitalTwin,
        EpochState,
        FaultState,
        LinkState,
        PowerState,
        SatelliteState,
        ThermalState,
    )
    assert Constellation is not None
    assert DigitalTwin is not None
