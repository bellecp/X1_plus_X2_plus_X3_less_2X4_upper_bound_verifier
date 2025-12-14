## The upper bound problem

To prove an upper bound on the quantity
```math
C=\sup_\mu P(X_1 + X_2 + X_3 < 2 X_4),
```
where $X_1,X_2,X_3,X_4$ are iid with distribution $\mu$ and $\mu$ is a probability measure on $[0,+\infty)$,
one strategy is to first derive the upper bound, for any $0\le x_1\le \dots \le x_m$,
```math
C\le \frac{1}{2|T|} \sum_{(i,j,k,l)\in T} I(x_i + x_j + x_k < 2 x_l )
```
where $I(\cdot)$ denotes the indicator function and $T$ is the set of $(i,j,k,l)\in [m]^4$ such that
$i<j<k$ and $j < l$ and $l \ne k$. A short argument to prove the above inequality starts by noticing
that $P(X_1 + X_2 + X_3  < 2X_4) = P(X_a + X_b + X_c < 2X_d)$ for any pairwise distinct $a,b,c,d \in [m]$ and averaging over all such quadruples,
see Sections 3 and 4 of <https://arxiv.org/abs/2412.15179> for details.

To prove an upper bound on
```math
\sum_{(i,j,k,l)\in T} I(x_i + x_j + x_k < 2 x_l ),
```
one strategy is to partition $T$ into disjoint subsets such that the linear inequalities in each subset are not jointly satisfiable.
Then for each set $g$ in the partition, infeasibility implies
```math
\sum_{(i,j,k,l)\in g} I(x_i + x_j + x_k < 2 x_l ) \le |g|-1.
```

## What this repository is about

This repository provides a simple verifier that takes as input disjoint subsets of $T$, and verifies that each subset of inequalities is indeed infeasible using linear programming. It also computes the corresponding upper bound on $C$.

Two example files are provided, one with $m=6$ and one with $m=7$. The paper <https://arxiv.org/abs/2412.15179> follows this strategy up to $m=20$, which gives $C\le 4.17$.

## How to use the verifier

Clone the current gist

```console
$ git clone https://github.com/bellecp/X1_plus_X2_plus_X3_less_2X4_upper_bound_verifier.git 
```

Install ``python3`` and ``scipy``. Run the verifier on the two provided examples:

```console
$ cd X1_plus_X2_plus_X3_less_2X4_upper_bound_verifier
$ python3 verify_witness_linprog.py --file=optimality_witness_m_is_6.log 

All checks passed! The systems of inequalities are disjoint and each system is infeasible.
2 disjoint subsystems infeasible found
Probability: 28 / 60 = 0.4666666666666667
```


```console
$ python3 verify_witness_linprog.py --file=optimality_witness_m_is_7.log

All checks passed! The systems of inequalities are disjoint and each system is infeasible.
6 disjoint subsystems infeasible found
Probability: 64 / 140 = 0.45714285714285713
```

## See also

- Bellec, P. C., & Fritz, T. (2024). Optimizing over iid distributions and the Beat the Average game. <https://arxiv.org/abs/2412.15179>.
- The MathOverflow discussion <https://mathoverflow.net/questions/474916/how-large-can-mathbfpx-1-x-2-x-3-2-x-4-get/474927> where [Tobias](http://tobiasfritz.science/) initially posed the problem.
- Disjoint systems of inequalities, each not jointly satisfiable, for $m=15$ <https://arxiv.org/src/2412.15179v5/anc/optimality_witness_m_is_15.log> 
and $m=20$
<https://arxiv.org/src/2412.15179v5/anc/optimality_witness_m_is_20.log>. Those
give $C\le 4.22$ and $C\le 4.17$ respectively. The code of the programs used to
obtain these disjoint systems is provided in the ancillary files of the arXiv
submission and takes around 24h on a desktop computer. More powerful hardware
should allow to go further with the same programs.
- A web-friendly writeup <https://bellecp.github.io/optimizing_iid.html>.
