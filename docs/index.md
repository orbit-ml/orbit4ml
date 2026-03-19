# orbit4ml

<p align="center">
  <img src="assets/logo.png" alt="orbit4ml" width="400"/>
</p>

<p align="center">
  <a href="https://github.com/orbit-ml/orbit4ml/actions"><img src="https://img.shields.io/github/actions/workflow/status/orbit-ml/orbit4ml/ci.yml?label=tests" alt="Tests"></a>
  <a href="https://pypi.org/project/orbit4ml/"><img src="https://img.shields.io/pypi/v/orbit4ml" alt="PyPI"></a>
  <a href="https://github.com/orbit-ml/orbit4ml/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License"></a>
</p>

---

**orbit4ml** is an open ecosystem for machine learning in space.

Space is the next frontier for intelligent systems — but running ML in orbit, on the lunar surface, or deep in the solar system is fundamentally different from running it in a terrestrial data center. orbit4ml brings together the libraries, tools, and frameworks needed to navigate that gap.

## Why orbit4ml?

Deploying ML in space introduces a unique set of constraints that terrestrial frameworks are not designed for:

- **Compute** — radiation-hardened processors run at a fraction of the speed and capability of modern GPUs. FPGAs and ASICs dominate.
- **Bandwidth** — downlink windows are short and expensive. Models must process data on-board and transmit only what matters.
- **Latency** — the speed of light makes real-time ground control loops impossible beyond LEO. Autonomy is not optional.
- **Data scarcity** — labeled datasets from space missions are rare. Few-shot and meta-learning approaches are essential.
- **Reliability** — cosmic ray bit flips, thermal cycling, and single-event upsets demand fault-tolerant training and inference.

orbit4ml is built to address these constraints directly, providing implementations and abstractions that space ML practitioners can use out of the box.

## Overview

orbit4ml is organized into focused submodules:

- **`orbit4ml.data`** — Datasets, transforms, and task samplers for space imagery, telemetry, and scientific observations.
- **`orbit4ml.compress`** — Model compression, quantization, and pruning pipelines optimized for low-bandwidth uplink/downlink constraints.
- **`orbit4ml.edge`** — Inference engines and model exporters targeting space-grade hardware: FPGAs, radiation-tolerant SoCs, and embedded processors.
- **`orbit4ml.adapt`** — Meta-learning and continual learning algorithms for in-orbit adaptation with minimal data and no ground-in-the-loop.
- **`orbit4ml.comm`** — Utilities for delay-tolerant networking (DTN), intermittent connectivity, and federated learning across satellite constellations.
- **`orbit4ml.bench`** — Standardized benchmarks and evaluation protocols for space ML tasks, enabling fair comparison across methods.

## Installation

!!! note "Coming soon"
    orbit4ml is under active development. The first release will be announced on GitHub.

```bash
pip install orbit4ml
```

## Snippets & Examples

### High-level Wrappers

```python
import orbit4ml

# Coming soon
```

### Learning Domains

orbit4ml will ship with ready-to-use learning domains covering:

- Earth observation (multispectral, SAR, hyperspectral)
- Spacecraft telemetry anomaly detection
- Space situational awareness
- On-board science autonomy

### Low-Level Utilities

```python
# Coming soon
```

## Citation

If you use orbit4ml in your research, please cite:

```bibtex
@software{orbit4ml2026,
  author  = {Mainak Mallick},
  title   = {orbit4ml: An Open Ecosystem for Machine Learning in Space},
  year    = {2026},
  url     = {https://github.com/orbit-ml/orbit4ml}
}
```

## Acknowledgements & Friends

orbit4ml draws inspiration from [learn2learn](https://learn2learn.net), [PyTorch](https://pytorch.org), and the broader open-source ML community. We also draw on the excellent work coming out of space agencies, satellite operators, and the NewSpace community pushing the boundaries of on-board intelligence.
