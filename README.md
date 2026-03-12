
# Shipyard Decision Optimization Starter Kit (CPLEX/OPL/DOcplex)

This kit contains **shareable, client-ready** examples for:

- **Workforce planning** (multi-skill, shift-based coverage) — OPL and Python/DOcplex
- **Shipbuilding production capacity allocation** (blocks → work centers across time buckets) — OPL and Python/DOcplex

> These are educational templates you can extend with client data. They run with the **IBM ILOG CPLEX Optimization Studio** (OPL models) or with **Python + DOcplex** (Python models). For quick trials, clients can use the **Community Edition** of CPLEX (size-limited). See the product page for editions and limits.

## Contents

```
shipyard_cplex_starter_kit/
  README.md
  LICENSE.txt (Apache-2.0 for *this* starter kit)
  workforce_planning/
    workforce_planning_opl.mod
    workforce_planning_opl.dat
    workforce_planning_docplex.py
  shipbuilding_production/
    block_capacity_plan_opl.mod
    block_capacity_plan_opl.dat
    block_capacity_plan_docplex.py
```

## How to run (quick)

### Option A — OPL (inside CPLEX Optimization Studio)
1. Open the `.mod` file in the IDE, attach the matching `.dat`, and **Run**.
2. Or use command line: `oplrun workforce_planning_opl.mod workforce_planning_opl.dat`

### Option B — Python (DOcplex)
1. `pip install docplex` (requires a local CPLEX installation for solving beyond Community limits)
2. `python workforce_planning_docplex.py`

> **Note:** The Python scripts include small inline datasets; replace with client CSV/DB as needed.

## Disclaimer
These examples are simplified to keep them readable and adaptable in presales / PoC contexts. You should refine objective terms (e.g., overtime cost, lateness penalties) and operational constraints (e.g., rest rules, union rules, training, clearances) per client requirements.
