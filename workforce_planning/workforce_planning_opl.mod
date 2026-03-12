
// workforce_planning_opl.mod
// Multi-skill shift coverage with basic fairness constraints

{string} Workers = ...;
{string} Days = ...;
{string} Shifts = ...;
{string} Skills = ...;

// demand[d][s][k] = number of heads needed with skill k on day d, shift s
int demand[Days][Shifts][Skills] = ...;
// hasSkill[w][k] = 1 if worker w has skill k
int hasSkill[Workers][Skills] = ...;
// cost of assigning worker w to (d,s)
float assignCost[Workers][Days][Shifts] = ...;

// Max shifts per worker over the horizon (fairness / workload cap)
int maxShiftsPerWorker = ...;

// Decision: x[w][d][s] = 1 if worker w works shift s on day d
dvar boolean x[Workers][Days][Shifts];

minimize sum(w in Workers, d in Days, s in Shifts) assignCost[w][d][s] * x[w][d][s];

subject to {
  // Coverage with skills: for each (d,s,k), sum of assigned workers possessing k must meet demand
  forall(d in Days, s in Shifts, k in Skills)
    sum(w in Workers) hasSkill[w][k] * x[w][d][s] >= demand[d][s][k];

  // One shift per day per worker
  forall(w in Workers, d in Days)
    sum(s in Shifts) x[w][d][s] <= 1;

  // Per-worker load cap over the horizon
  forall(w in Workers)
    sum(d in Days, s in Shifts) x[w][d][s] <= maxShiftsPerWorker;
}

// KPIs for reporting
float totalAssignments = sum(w in Workers, d in Days, s in Shifts) x[w][d][s];
{string} kpiWorkers = { w | w in Workers };
