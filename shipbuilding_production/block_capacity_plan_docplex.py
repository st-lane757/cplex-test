
# block_capacity_plan_docplex.py
from docplex.mp.model import Model

Blocks  = ['B001','B002','B003']
Centers = ['PanelLine','WeldingBay','Outfitting']
Periods = ['W1','W2','W3']

hours_req = {
 'B001':{'PanelLine':40,'WeldingBay':60,'Outfitting':20},
 'B002':{'PanelLine':30,'WeldingBay':30,'Outfitting':30},
 'B003':{'PanelLine':20,'WeldingBay':50,'Outfitting':40},
}
cap = {
 'PanelLine': {'W1':50,'W2':50,'W3':50},
 'WeldingBay':{'W1':80,'W2':80,'W3':80},
 'Outfitting':{'W1':40,'W2':40,'W3':40},
}
overtime_cost = {
 'PanelLine': {'W1':5,'W2':5,'W3':5},
 'WeldingBay':{'W1':8,'W2':8,'W3':8},
 'Outfitting':{'W1':10,'W2':10,'W3':10},
}

mdl = Model('block_capacity_plan')

x = mdl.continuous_var_dict(((b,r,t) for b in Blocks for r in Centers for t in Periods), lb=0, name='x')
overtime = mdl.continuous_var_dict(((r,t) for r in Centers for t in Periods), lb=0, name='ot')

# Fulfill hours per block-center
for b in Blocks:
    for r in Centers:
        mdl.add_constraint(mdl.sum(x[(b,r,t)] for t in Periods) == hours_req[b][r], ctname=f'req_{b}_{r}')

# Capacity per center/period + overtime
for r in Centers:
    for t in Periods:
        mdl.add_constraint(mdl.sum(x[(b,r,t)] for b in Blocks) <= cap[r][t] + overtime[(r,t)],
                           ctname=f'cap_{r}_{t}')

mdl.minimize(mdl.sum(overtime_cost[r][t]*overtime[(r,t)] for r in Centers for t in Periods))

sol = mdl.solve(log_output=True)
if sol is None:
    print('No solution found')
else:
    print(f"Objective (overtime cost): {sol.objective_value}")
    for r in Centers:
        for t in Periods:
            used = sum(x[(b,r,t)].solution_value for b in Blocks)
            print(f"{r} {t}: used={used:.1f}, cap={cap[r][t]}, ot={overtime[(r,t)].solution_value:.1f}")
