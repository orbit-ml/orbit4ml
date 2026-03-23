#!/usr/bin/env python3
"""orbit4ml MVP: Training under orbital constraints.

Demonstrates using orbit4ml.sim to simulate a satellite constellation
and run a PyTorch training loop that respects orbital power and thermal
constraints.

Uses synthetic data (random tensors) so it runs without downloading datasets.

Usage:
    python examples/mvp_training_loop.py
"""

import torch
from datetime import datetime

import orbit4ml
from orbit4ml.sim import Constellation, DigitalTwin


def main():
    print(f"orbit4ml v{orbit4ml.__version__}")
    print("=" * 50)

    constellation = Constellation(
        planes=6, sats_per_plane=11, altitude=550, inclination=53.0
    )
    print(f"Constellation: {constellation.total_satellites} satellites")
    print(f"  {constellation.planes} planes x {constellation.sats_per_plane} sats/plane")
    print(f"  Altitude: {constellation.altitude} km, Inclination: {constellation.inclination} deg")

    twin = DigitalTwin(constellation)

    model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(3 * 64 * 64, 10))
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print(f"\nSimulating 30 minutes of orbital training...")
    print("-" * 50)

    total_steps = 0
    train_steps = 0
    eclipse_steps = 0

    start = datetime(2026, 6, 1, 12, 0, 0)

    for epoch in twin.propagate(start=start, hours=0.5, step_seconds=60):
        for sat in epoch.satellites:
            total_steps += 1

            if sat.power.available and sat.thermal.within_budget:
                batch_x = torch.randn(8, 3, 64, 64)
                batch_y = torch.randint(0, 10, (8,))
                loss = torch.nn.functional.cross_entropy(model(batch_x), batch_y)
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                train_steps += 1
            else:
                eclipse_steps += 1

        faults = [f for s in epoch.satellites for f in s.faults.active]
        if faults:
            print(f"  [{epoch.timestamp.strftime('%H:%M:%S')}] Faults: {faults}")

    print("-" * 50)
    print(f"Total satellite-steps: {total_steps}")
    print(f"  Training steps (sunlit + thermal OK): {train_steps}")
    print(f"  Idle steps (eclipse or thermal limit): {eclipse_steps}")
    print(f"  Training utilization: {train_steps / total_steps * 100:.1f}%")


if __name__ == "__main__":
    main()
