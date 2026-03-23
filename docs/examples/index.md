# Examples

Runnable scripts demonstrating orbit4ml in action.

## MVP Training Loop

The main v0.1 example: simulate a 66-satellite constellation for 30 minutes and
run a PyTorch training loop gated by orbital power and thermal constraints.

**Source:** [`examples/mvp_training_loop.py`](https://github.com/orbit-ml/orbit4ml/blob/main/examples/mvp_training_loop.py)

```bash
python examples/mvp_training_loop.py
```

??? example "Full source code"

    ```python
    #!/usr/bin/env python3
    """orbit4ml MVP: Training under orbital constraints."""

    import torch
    from datetime import datetime

    import orbit4ml
    from orbit4ml.sim import Constellation, DigitalTwin


    def main():
        print(f"orbit4ml v{orbit4ml.__version__}")
        print("=" * 50)

        # 1. Define a Starlink-like constellation
        constellation = Constellation(
            planes=6, sats_per_plane=11, altitude=550, inclination=53.0
        )
        print(f"Constellation: {constellation.total_satellites} satellites")
        print(f"  {constellation.planes} planes x {constellation.sats_per_plane} sats/plane")
        print(f"  Altitude: {constellation.altitude} km, Inclination: {constellation.inclination} deg")

        # 2. Create the digital twin
        twin = DigitalTwin(constellation)

        # 3. Set up a simple model
        model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(3 * 64 * 64, 10))
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

        print(f"\nSimulating 30 minutes of orbital training...")
        print("-" * 50)

        total_steps = 0
        train_steps = 0
        eclipse_steps = 0

        start = datetime(2026, 6, 1, 12, 0, 0)

        # 4. Propagate and train under constraints
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

        # 5. Report results
        print("-" * 50)
        print(f"Total satellite-steps: {total_steps}")
        print(f"  Training steps (sunlit + thermal OK): {train_steps}")
        print(f"  Idle steps (eclipse or thermal limit): {eclipse_steps}")
        print(f"  Training utilization: {train_steps / total_steps * 100:.1f}%")


    if __name__ == "__main__":
        main()
    ```

### What it demonstrates

1. **Constellation setup** — 66 satellites in a Walker-delta pattern (6 planes x 11 sats)
2. **Orbital simulation** — SGP4 propagation with 60-second timesteps
3. **Constraint gating** — training only happens when `power.available` and `thermal.within_budget` are both True
4. **Fault injection** — stochastic hardware faults (SEUs, thermal shutdowns, link failures) are logged
5. **Utilization metrics** — reports what fraction of satellite-time was usable for training (~70%)

### Expected output

```
orbit4ml v0.1.0
==================================================
Constellation: 66 satellites
  6 planes x 11 sats/plane
  Altitude: 550.0 km, Inclination: 53.0 deg

Simulating 30 minutes of orbital training...
--------------------------------------------------
--------------------------------------------------
Total satellite-steps: 2046
  Training steps (sunlit + thermal OK): 1442
  Idle steps (eclipse or thermal limit): 604
  Training utilization: 70.5%
```

## Planned Examples

- **EuroSAT Classification** — Train a CNN on satellite imagery with orbital constraints
- **Constellation Visualization** — Plot satellite positions and eclipse regions
- **Thermal Profiling** — Analyze GPU thermal budgets across different orbits
- **Multi-Satellite Federated Training** — Gradient exchange over inter-satellite links (v1.0)
