Degree level: Master’s

# Project proposal

## 1. The problem and goal

An ion-exchange membrane is a thin film that lets certain charged particles,
called ions, pass through. When two labs report different resistance readings
for the same kind of membrane, the difference could come from the film
thickness, the test setup, or how the labs report their results. A lower reading
alone gives us little basis for deciding which film conducts ions more easily.

My project, **MembraneProbe**, will investigate how reliably we can separate
the film's resistance from the contribution of the test setup. I will start
with different thicknesses of the same membrane material and fit them only
within a common test setup and set of conditions. I will measure prediction
error at a thickness left out of the fit and examine how the range of available
thicknesses and the amount of measurement noise affect the uncertainty in both
estimates.

## 2. The simulator

I will build a Python model that runs locally and reads a JSON file containing
film thickness, resistance, active test area, and measurement details such as
temperature, hydration, and whether the reported reading includes the setup.
When the input is in ohms, the model will multiply resistance by active area
to obtain area-specific resistance (ASR) in Ω·cm². For comparable readings
that include the setup contribution, it will fit the following model.

```math
\mathrm{ASR}_{\mathrm{total}}(d) = \frac{d}{\sigma} + \mathrm{ASR}_{\mathrm{setup}}
```

The thickness $d$ is in cm, and $\sigma$ is conductivity across the film in
S/cm. For each series, the model assumes a common conductivity and a common
setup contribution, which includes contact resistance. It will return
conductivity and setup ASR with uncertainty intervals, along with the
predicted total ASR at a requested thickness.

I will first use one humidity series from Cooper's published measurements. I
will hold out each thickness in turn, along with all its available readings,
and report the mean absolute prediction error in Ω·cm². I will then use
simulated series with known parameters to vary thickness span and measurement
noise separately. For each condition, I will measure how far the estimates
are from the known values and how wide the uncertainty intervals are.
[Cooper (2010), Figure 7](https://www.scribner.com/wp-content/uploads/2017/10/Cooper-on-Through-Plane-Resistance-of-PEM-J-Elect-Soc-2010.pdf#page=7)

## 3. The agent's role

The agent will decide which evidence to retrieve from a fixed set of published
readings and methods excerpts. If a preliminary fit gives an uncertain
estimate of the setup contribution and the available films are close in
thickness, it can request a measurement farther from the existing ones. If
the papers are unclear about whether they included the setup resistance, it
can check the measurement method first. It will rerun the Python model when
the usable data change, cite the evidence for its decision, and report
**insufficient evidence** when it cannot justify a comparison.

I will compare this approach with a fixed rule that prioritizes the largest
increase in thickness span among comparable readings and checks the methods
when no such reading is available. Both approaches will start with the same
records and have up to two evidence requests per case. I will score their
decisions against conclusions established from the full evidence, including
cases where a justified conclusion remains out of reach. One question is
whether the agent can recognize when checking the measurement method will
resolve more uncertainty than obtaining another reading.

## Explain your project to someone outside your field

Imagine two labs measuring how hard it is for tiny charged particles to cross
the same kind of film. One lab reports a reading for the film and its holder
together. The other subtracts the holder's contribution first. Their numbers
can differ even when the films behave the same way. I will use measurements
at several thicknesses to see how the reading changes as the film gets
thicker. A computer model can use that pattern to estimate the film's share
of the reading.

When two readings are hard to compare, the AI will choose what to check next.
It might look up how a lab calculated its reading or look for a measurement at
a different thickness. I will test whether those choices help it reach a
well-supported conclusion with only two checks.
