"""Simplified piecewise thermal model for orbit4ml.sim.

v0.1 uses a two-state model: sunlit vs eclipse. In sunlight, radiator
panels face the sun and are less efficient. In eclipse, radiators face
deep space and are more efficient, allowing higher GPU power budgets.

Higher-fidelity multi-node thermal networks are deferred to v0.3+.
"""

from orbit4ml.sim.types import ThermalState

SUNLIT_RADIATOR_EFFICIENCY = 0.45
ECLIPSE_RADIATOR_EFFICIENCY = 0.85
BASE_GPU_BUDGET_WATTS = 200.0


def compute_thermal_state(in_eclipse: bool) -> ThermalState:
    """Compute thermal state based on eclipse condition.

    Args:
        in_eclipse: Whether the satellite is currently in Earth's shadow.

    Returns:
        ThermalState with GPU budget and radiator efficiency.
    """
    if in_eclipse:
        efficiency = ECLIPSE_RADIATOR_EFFICIENCY
    else:
        efficiency = SUNLIT_RADIATOR_EFFICIENCY

    gpu_budget = BASE_GPU_BUDGET_WATTS * efficiency

    return ThermalState(
        gpu_budget_watts=gpu_budget,
        within_budget=True,
        radiator_efficiency=efficiency,
    )
