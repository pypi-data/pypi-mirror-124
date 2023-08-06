# import os
# os.environ["JAX_PLATFORM_NAME"] = "cpu"
from optimaldesign.linear_model import LinearModel
from jax.config import config
from optimaldesign.optimal_design import OptimalDesign

config.update("jax_enable_x64", True)

__all__ = ["LinearModel", "OptimalDesign"]
