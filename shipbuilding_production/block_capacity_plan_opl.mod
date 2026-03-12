
// block_capacity_plan_opl.mod
// Allocate hours from work centers to ship blocks across time buckets subject to capacities.

{string} Blocks = ...;
{string} Centers = ...;
{string} Periods = ...;

// hours_req[b][r] = total hours of center r needed by block b over the horizon
float hours_req[Blocks][Centers] = ...;
// cap[r][t]  = available hours of center r in period t
float cap[Centers][Periods] = ...;

// Decision: x[b][r][t] >= 0 hours of center r spent on block b in period t
dvar float+ x[Blocks][Centers][Periods];

// Optional soft overtime per center/period
dvar float+ overtime[Centers][Periods];

float overtimeCost[Centers][Periods] = ...;

minimize sum(r in Centers, t in Periods) overtimeCost[r][t]*overtime[r][t];

subject to {
  // Fulfill total hours per block/center
  forall(b in Blocks, r in Centers)
    sum(t in Periods) x[b][r][t] == hours_req[b][r];

  // Capacity per center/period with overtime
  forall(r in Centers, t in Periods)
    sum(b in Blocks) x[b][r][t] <= cap[r][t] + overtime[r][t];
}

// KPIs
float totalOvertime = sum(r in Centers, t in Periods) overtime[r][t];
