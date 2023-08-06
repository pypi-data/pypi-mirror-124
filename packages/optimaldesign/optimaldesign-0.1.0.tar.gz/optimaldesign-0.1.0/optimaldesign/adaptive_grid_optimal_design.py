from optimaldesign.linear_model import LinearModel
import jax.numpy as np
from jax import vmap
from optimaldesign.interior_point_method import (
    NLPMinimizeLinearEqualityConstraint,
    NLPMinimizeInequalityConstraint,
    NLPMinimizeBound,
    NLPMinimizeOption,
    NLPSolverOption,
    NLPSolver,
    NLPFunction,
)
from optimaldesign.design_measure import DCritWeights, DCritSupp
from typing import List


class AdaptiveGridOptimalDesign:
    def __init__(
        self,
        linear_models: List[LinearModel],
        target_weights: List[np.float64],
        design_x_u,
        design_x_l,
        init_grid,
        optimality: str = "d",
    ):
        self.linear_models = linear_models
        self.target_weights = target_weights
        self.design_x_u = design_x_u
        self.design_x_l = design_x_l
        self.init_grid = init_grid
        self.optimality = optimality

    def _minimize_d_opt_weights(self, weights, supp):
        supp_size = supp.shape[0]
        minimize_option = NLPMinimizeOption(
            x0=weights,
            bound_x=NLPMinimizeBound(
                lower=np.zeros(supp_size), upper=np.ones(supp_size)
            ),
            lin_equal_constr=NLPMinimizeLinearEqualityConstraint(
                mat=np.ones((1, supp_size)), enabled=True
            ),
            inequal_constr=NLPMinimizeInequalityConstraint(),
        )
        solver_option = NLPSolverOption()

        nlp_target = DCritWeights()
        nlp_target.weight = self.target_weights[0]
        nlp_target.set_constants(linear_model=self.linear_models[0], supp=supp)

        nlp_function = NLPFunction()
        nlp_function.add_target(function_target=nlp_target)

        nlp_solver = NLPSolver(func=nlp_function, option=solver_option)

        weights = nlp_solver.minimize(minimize_option=minimize_option)
        return weights

    def minimize_weights(self, weights, supp):
        if self.optimality == "d":
            weights = self._minimize_d_opt_weights(weights, supp)
            weights, supp = self.filter_design(weights, supp)
            weights = self._minimize_d_opt_weights(weights, supp)
        return weights, supp

    def _minimize_d_opt_supp_idx(self, weights, supp, idx):
        x0 = supp[idx]
        minimize_option = NLPMinimizeOption(
            x0=x0,
            bound_x=NLPMinimizeBound(lower=self.design_x_l, upper=self.design_x_u),
            lin_equal_constr=NLPMinimizeLinearEqualityConstraint(enabled=False),
            inequal_constr=NLPMinimizeInequalityConstraint(
                use_template="voronoi", voronoi_supp=supp, voronoi_x_id=idx
            ),
        )
        nlp_target = DCritSupp()
        nlp_target.weight = self.target_weights[0]
        nlp_target.set_constants(
            linear_model=self.linear_models[0], weights=weights, supp=supp
        )

        nlp_function = NLPFunction()
        nlp_function.add_target(function_target=nlp_target)
        solver_option = NLPSolverOption()
        nlp_solver = NLPSolver(func=nlp_function, option=solver_option)
        supp_x_idx = nlp_solver.minimize(minimize_option=minimize_option)
        return supp_x_idx

    def minimize_supp(self, weights, supp):
        if self.optimality == "d":
            supp_list = [
                self._minimize_d_opt_supp_idx(weights, supp, idx)
                for idx in range(supp.shape[0])
            ]
            supp = np.asarray(supp_list)
        return weights, supp

    def solve(self):
        i = 0
        distance_proof = True
        measure_proof = True
        supp = self.init_grid
        supp_size = supp.shape[0]
        weights = np.full(supp_size, 1.0 / float(supp_size))
        design_measure = self.design_measure(weights, supp)
        weights, supp = self.minimize_weights(weights, supp)
        design_measure = self.design_measure(weights, supp)
        while i < 10 and distance_proof and measure_proof:
            i += 1
            old_weights, old_supp = weights, supp
            old_design_measure = design_measure
            weights, supp = self.minimize_supp(weights, supp)
            distance_supp = old_supp - supp
            distance_supp_norm = np.linalg.norm(distance_supp)
            weights, supp = self.collapse_design(weights, supp)

            weights, supp = self.minimize_weights(weights, supp)
            design_measure = self.design_measure(weights, supp)
            if i > 1:
                if design_measure < old_design_measure + 1e-8:
                    distance_proof = False
                elif distance_supp_norm < np.linalg.norm(supp) * 1e-8:
                    weights, supp = old_weights, old_supp
                    distance_proof = False

                if design_measure < old_design_measure:
                    weights, supp = old_weights, old_supp
        design_measure = self.design_measure(weights, supp)
        return weights, supp

    def design_measure(self, weights, supp):
        if self.optimality == "d":
            return np.power(
                np.linalg.det(self.linear_models[0].fim(weights, supp)),
                1.0 / self.linear_models[0].selected_feature_size,
            )

    def filter_design(self, weights: np.ndarray, supp: np.ndarray):
        filter_design_idx = weights > 1e-4
        weights = weights[filter_design_idx]
        supp = supp[filter_design_idx]

        # normalize weights
        weights = self.normalize_weights(weights)
        return weights, supp

    def normalize_weights(self, weights):
        return weights / np.sum(weights)

    def collapse_design(self, weights, supp):
        supp_distance = vmap(
            lambda x: np.linalg.norm(np.array([x]) - supp, axis=1, ord=2)
        )(supp)
        distance_cluster = supp_distance < 1e-4
        collapse_cluster = np.argmax(weights * distance_cluster, axis=1) == np.arange(
            weights.shape[0]
        )
        collapse_cluster_weights = np.sum(weights * distance_cluster, axis=1)[
            collapse_cluster
        ]
        collapse_cluster_supp = supp[collapse_cluster]
        return collapse_cluster_weights, collapse_cluster_supp
