### This Python script takes the sets of inequalities produced by milp2.py and verifies that:
### 1. They are disjoint
### 2. Each group of inequality is infeasible by solving a linear programming feasibility problem.

import argparse
import re
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog


### Determine the value of m from the command line
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str)
args = parser.parse_args()


### Extract the inequalities from the file
with open(args.file, 'r') as file:
    data = file.read()
disjoint_groups = data.split('\n\n')[1:]
groups = defaultdict(list)
pattern = r"X(\d+) \+ X(\d+) \+ X(\d+) < 2\*X(\d+)"

values = set()

for n, g in enumerate(disjoint_groups):
    for line in g.strip().split('\n') :
        t = tuple(map(int, re.search(pattern, line).groups()))
        groups[n].append(t)
        values.update(t)

assert min(values) >= 1
m = max(values)

values = sorted(list(values))

T = [
        (i, j, k, l)
        for i in range(1, m+1)
        for j in range(1, m+1)
        for k in range(1,m+1)
        for l in range(1, m+1)
        if i < j and j < k and l not in [i,j,k] and j < l
    ]

set_T = set(T)

### Then check the conditions
for n, g in groups.items():

    # Ensure that each group is a set of inequalities with variable indices in increasing order
    assert len(set(g)) == len(g)
    for t in g:
        assert t[0] < t[1] < t[2] and t[1] < t[3] and t[3] != t[2]
        assert t in set_T


    # Ensure that the groups are disjoint
    for nn, gg in groups.items():
        if n != nn:
            assert set(g).isdisjoint(set(gg))

    # Prove infeasibility via linear programming
    # Variables: X_1,...,X_m
    # Constraints:
    #   X_i + X_j + X_k - 2 X_l <= - 0.001  for each inequality
    #   X_{r-1} - X_r <= 0             (monotonicity)
    #   X_r >= 0

    A = []
    b = []

    # Inequalities from the group
    for (i, j, k, l) in g:
        row = np.zeros(m)
        row[i-1] += 1
        row[j-1] += 1
        row[k-1] += 1
        row[l-1] -= 2
        A.append(row)
        b.append(-0.001)

    # Order constraints: X_{r-1} - X_r <= 0
    for r in range(1, m):
        row = np.zeros(m)
        row[r-1] = 1
        row[r]   = -1
        A.append(row)
        b.append(0)

    # Nonnegativity handled via bounds
    bounds = [(0, None)] * m

    res = linprog(
        c=np.zeros(m),      # feasibility problem
        A_ub=np.array(A),
        b_ub=np.array(b),
        bounds=bounds,
        method="highs"
    )

    if res.status == 2:
        pass # status == 2 corresponds to sinfeasible, as desired
    else:
        print(f"The following system of group {n} was expected to be infeasible but was not:")
        for (i, j, k, l) in g:
            print("X{} + X{} + X{} < 2*X{}".format(i, j, k, l))
        raise ValueError(f"LP did not conclude that the system is infeasible for group {n}")

print("All checks passed! The systems of inequalities are disjoint and each system is infeasible.")
print(len(groups), "disjoint subsystems infeasible found")
print("Probability:", len(T)-len(groups), "/", (2*len(T)), "=", (len(T)-len(groups))/(2*len(T)))
