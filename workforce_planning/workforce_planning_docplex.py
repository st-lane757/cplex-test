
# workforce_planning_docplex.py
from docplex.mp.model import Model

# --- Toy data (replace with client data) ---
Workers = ['W1','W2','W3','W4']
Days    = ['Mon','Tue','Wed']
Shifts  = ['Day','Night']
Skills  = ['Weld','Fit','Test']

# demand[(d,s,k)]
demand = {
 ('Mon','Day','Weld'):1, ('Mon','Day','Fit'):1, ('Mon','Day','Test'):0,
 ('Mon','Night','Weld'):1, ('Mon','Night','Fit'):0, ('Mon','Night','Test'):0,
 ('Tue','Day','Weld'):1, ('Tue','Day','Fit'):1, ('Tue','Day','Test'):1,
 ('Tue','Night','Weld'):1, ('Tue','Night','Fit'):0, ('Tue','Night','Test'):1,
 ('Wed','Day','Weld'):1, ('Wed','Day','Fit'):1, ('Wed','Day','Test'):0,
 ('Wed','Night','Weld'):1, ('Wed','Night','Fit'):1, ('Wed','Night','Test'):1,
}

# hasSkill[(w,k)]
hasSkill = {
 ('W1','Weld'):1, ('W1','Fit'):1,  ('W1','Test'):0,
 ('W2','Weld'):1, ('W2','Fit'):0,  ('W2','Test'):1,
 ('W3','Weld'):0, ('W3','Fit'):1,  ('W3','Test'):1,
 ('W4','Weld'):1, ('W4','Fit'):1,  ('W4','Test'):1,
}
assign_cost = {(w,d,s):1.0 for w in Workers for d in Days for s in Shifts}
max_shifts_per_worker = 2

# --- Model ---
mdl = Model('workforce_planning')

x = mdl.binary_var_dict(((w,d,s) for w in Workers for d in Days for s in Shifts), name='x')

# Coverage by skill
for d in Days:
    for s in Shifts:
        for k in Skills:
            mdl.add_constraint(mdl.sum(hasSkill[w,k]*x[(w,d,s)] for w in Workers) >= demand[(d,s,k)],
                               ctname=f'cover_{d}_{s}_{k}')

# One shift per day per worker
for w in Workers:
    for d in Days:
        mdl.add_constraint(mdl.sum(x[(w,d,s)] for s in Shifts) <= 1, ctname=f'oneshift_{w}_{d}')

# Load cap
for w in Workers:
    mdl.add_constraint(mdl.sum(x[(w,d,s)] for d in Days for s in Shifts) <= max_shifts_per_worker,
                       ctname=f'cap_{w}')

# Objective: minimize assignment cost
mdl.minimize(mdl.sum(assign_cost[(w,d,s)]*x[(w,d,s)] for w in Workers for d in Days for s in Shifts))

sol = mdl.solve(log_output=True)
if sol is None:
    print('No solution found')
else:
    print(f"Objective: {sol.objective_value}")
    for d in Days:
        for s in Shifts:
            assigned = [w for w in Workers if x[(w,d,s)].solution_value > 0.5]
            print(f"{d} {s}: {assigned}")
