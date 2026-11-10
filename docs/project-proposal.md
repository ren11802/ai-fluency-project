# Project proposal

## 1. The problem and goal

I want to increase the production of B in a jacketed continuous stirred-tank
reactor (CSTR) that converts A to B in a first-order, exothermic reaction. A
warmer reactor can make more product, but it can also release heat faster than
the jacket can remove it. A setting that works with a steady feed can become
infeasible when the incoming liquid gets warmer or more concentrated.

I will compare jacket policies in 20-minute simulations at a fixed nominal
flow rate. The primary score is the lowest time-averaged outlet production
rate of B across four cases: nominal feed, a 3 K feed-temperature increase, a
5% feed-concentration increase, and both increases together. The disturbances
last from minute 5 to minute 10. I will use the same initial state in all cases.
The initial target is a 10% improvement over a fixed 300 K jacket, with reactor
temperature at or below 350 K and normalized heat removal at or below 75 K/min
throughout every case. These are simulation targets for a teaching benchmark.

## 2. The simulator

The ground will be a local, callable Python function based on the
[APMonitor stirred-reactor model](https://apmonitor.com/apps/reactor/instructions.php).
It will integrate material balances for A and B and an energy balance using
SciPy's [`solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html).
I will assume a well-mixed liquid, constant volume and physical properties,
Arrhenius kinetics, and a jacket temperature that follows the specified policy
instantaneously. I will express cooling load as heat removed per unit reactor
thermal capacity, `max(UA * (T - T_jacket), 0) / (rho * Cp * V)`, in K/min.

The function will accept JSON-compatible inputs for the initial state, feed
schedule, benchmark parameters and jacket policy. It will return concentration
and temperature traces, average product rate, peak temperature, peak cooling
load, and the first constraint violation if one occurs. I will split the
integration at feed changes and check whether the reported peaks stabilize
as solver tolerances and step sizes are tightened. Before connecting an agent,
I will check the nominal steady state and verify that the model produces no
B with the reaction disabled and no B in the initial state or feed. I will
measure repeatability and aim for less than one second per four-case evaluation.

## 3. The agent's role

The agent will propose two parameters for the same deterministic jacket
policy on every run. It can set the nominal jacket temperature between
300 and 305 K and the feedback gain between 0 and 3 K/K. When the reactor
exceeds 330 K, the policy lowers the jacket temperature by the gain times
the excess temperature, with a 290 K lower bound. The agent reads the
simulated scores and violations before choosing the next pair. For example,
if only the warmer feed causes a temperature excursion, it can try stronger
feedback while retaining the nominal jacket temperature. If cooling load
then exceeds its cap, it can try lowering the nominal temperature to reduce
heat generation before the disturbance arrives. The simulator evaluates
each policy, and the final recommendation must pass all four cases.

A grid search can solve this small numerical problem given enough runs. I
will compare the agent with a prespecified grid of 20 candidates, giving
each method the same evaluation budget and comparing the best feasible
score found. My open question is whether the agent finds feasible settings
with fewer evaluations by using the type and timing of a violation. I will
also recheck the selected policies on a separate disturbance case with a
longer feed pulse.

## Explain your project to someone outside your field

Imagine a tank that turns an incoming liquid into a useful product while
giving off heat. A cooling jacket wraps around the tank. Running warmer
can make more product, but a small change in the incoming liquid can make
the tank heat up faster than the jacket can cool it.

I will build a computer model that lets me try different cooling settings
when the incoming liquid changes. The AI will use the model's results to
choose what to try next. I will compare its choices with a simple checklist
of settings and see which approach finds a way to make more product while
staying within the temperature and cooling limits.
