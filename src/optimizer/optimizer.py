import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds


class HoldetsOptimizer:
    def __init__(self, data, budget):
        self.data = data
        self.budget = budget
        self.price = data["price"].values
        self.points = data["predicted_accumlated_points"].values
        self.current_selection = data["currently_selected_riders"].values
        self.selling_penalty = 0.01
        self.constraints = []
        self.bounds = Bounds(0, 1)

    def add_budget_constraint(self, tolerance=0.01):
        self.constraints.append((self.price, self.budget * (1 - tolerance)))

    def add_rider_count_constraint(self, num_riders=8):
        rider_count_constraint = np.ones(len(self.price))
        self.constraints.append((rider_count_constraint, num_riders))

    def add_rider_change_penalty(self):
        self.price[self.current_selection] = self.price[self.current_selection] * (
            1 + self.selling_penalty
        )

    def optimize(self):
        c = -self.points
        A = [constraint[0] for constraint in self.constraints]
        b = [constraint[1] for constraint in self.constraints]
        linear_constraints = LinearConstraint(A, lb=-np.inf, ub=b)

        A_eq = [np.ones(len(self.price))]
        b_eq = [8]
        equality_constraints = LinearConstraint(A_eq, lb=b_eq, ub=b_eq)

        result = milp(
            c,
            bounds=self.bounds,
            integrality=np.ones(len(self.price)),
            constraints=[linear_constraints, equality_constraints],
        )
        selected_riders = self.data.iloc[result.x.round().astype(bool)]
        return selected_riders


def select_riders(budget: int):
    data = pd.read_csv("data/opti_rider_data.csv", index_col=0)
    optimizer = HoldetsOptimizer(data, budget)
    optimizer.add_budget_constraint()
    optimizer.add_rider_count_constraint()
    optimizer.add_rider_change_penalty
    selected_riders = optimizer.optimize()

    print("Selected riders:")
    print(selected_riders)
    print("\nTotal price:")
    print(selected_riders["price"].sum())


if __name__ == "__main__":
    select_riders()
