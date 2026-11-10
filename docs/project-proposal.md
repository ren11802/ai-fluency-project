# MembraneProbe — Making Sense of Membrane Resistance

## 1. The problem and goal

An ion-exchange membrane is a thin film that lets certain charged particles,
called ions, pass through. When two labs report different resistance readings,
the difference could come from the film material, the film thickness, or the way
each lab measured it. That makes it hard to tell from the reported numbers how
easily ions move through the film itself.

I will build a tool that estimates how much of a reading comes from the film
and how much comes from the test setup. The first version will use measurements
from films of the same material at several thicknesses under the same test
conditions. I will test how well it predicts the resistance at a thickness it
has not seen and whether an AI agent can decide which extra evidence would help
when two readings are difficult to compare.

## 2. The simulator

A standalone Python model will take measurements and test details from a
structured file. If a paper reports raw resistance in ohms, the model will
multiply it by the active test area to get area-specific resistance (ASR) in
Ω·cm². Measurements already reported in those units will enter directly. To
estimate the setup contribution, the model will fit uncorrected total ASR
against thickness for measurements of the same material and ion form made
under the same conditions with the same test setup.

```math
\mathrm{ASR}_{\mathrm{total}}(d) = \frac{d}{\sigma} + \mathrm{ASR}_{\mathrm{extra}}
```

Here, $d$ is the film thickness in cm, and $\sigma$ is the conductivity across
the film in S/cm. The model assumes the conductivity and the extra resistance
stay constant across the thickness series. The slope estimates $1/\sigma$, and
the intercept estimates the combined resistance from the setup and its contacts.
I will start by checking the method on one fixed-humidity series from the
published example below. I can then apply the same procedure to my own research
samples once comparable measurements are available. To check the predictions, I
will leave out all measurements at one thickness at a time and report the mean
absolute error of the held-out predictions in Ω·cm².

[Cooper (2010), Figure 7](https://www.scribner.com/wp-content/uploads/2017/10/Cooper-on-Through-Plane-Resistance-of-PEM-J-Elect-Soc-2010.pdf#page=7)

## 3. The agent's role

The agent will trace measurements to their sources and check whether the papers
measured and reported the same quantity. When the evidence is incomplete, it
will decide what to check next. If a methods excerpt can reveal whether a lab
already subtracted the setup resistance, the agent can request that excerpt. If
the test conditions match but the available samples are close in thickness, it
can request a reading at a different thickness. After each request it will
reassess the comparison and rerun the Python model when the inputs change. It
will cite the evidence for its conclusion and report **insufficient evidence**
when the available information cannot support a decision.

I will compare the agent with a fixed rule that first asks for the comparable
reading that extends the thickness range most, then checks the methods if no
such reading remains. Both will start with the same records and may request up
to two evidence items from the same set. I will score their conclusions against
answers set in advance, including cases that remain unresolved and cases where
checking a test method matters more than obtaining another reading.

## Explain your project to someone outside your field

Imagine two labs testing the same kind of film. One lab reports the resistance
of the film and its holder together. The other lab subtracts its holder's
contribution before reporting a number. The two results can differ even when
the films behave the same way. Testing several thicknesses under the same
conditions helps separate the two contributions. The way the reading rises as
the film gets thicker tells us about the film, and the model estimates what
would be left at zero thickness.

When two numbers are hard to compare, the tool will suggest a specific next
step, such as checking how one lab reported its result. It will explain what
that check tells us and say when the comparison is still uncertain.
