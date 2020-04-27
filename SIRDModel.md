{% include mathjax.html %}

Disclaimer - The following investigation is not fitted to the data, but is loosely based on COVID. This should not be taken too seriously.

The Susceptible, Infected, Recovered, Dead (SIRD) model is simply a set of differential equations specifying the rate of infection and recovery in terms of the population in each of these stages of the disease, and some coefficients.

Let $$s, i, r, d$$ be the susceptible, infected, recovered, and dead fraction of the population, i.e, they are a number from 0 to 1, where 1 represents the entire population. The SIRD model is then based on the set of equations:

#### Decay of the Susceptible

$$ \frac{\text{d}s}{\text{d}t} = - \beta\ s(t)\ i(t) $$

The susceptible become infected at a rate proportional to the product of the susceptible fraction, and the infected fraction: if $$i = 0$$ or $$s = 0$$, then there is no infection, and the larger $$s$$ or $$i$$ is, the more likely infection is to occur. This is scaled by $$\beta$$, which is a parameter governed by how easily transmissible the virus is, and (hopefully) effected by things like lock-down.


#### Growth of the Infected, and decay - recovery or death

$$ \frac{\text{d}i}{\text{d}t} = \beta\ s(t)\ i(t) - \gamma\ i(t) - \delta\ i(t) $$

The infected population increases due to the process described above, and decreases as infected people either recover (at a rate $$\gamma$$) or die (at rate $$\delta$$).

The parameter $$\gamma$$ is approximately the inverse of the recovery time. People have estimated the recovery time from COVID-19 to be anywhere between 2 and 30 days, which isn't very useful, but most reports are around the two week mark, so for this model, we take $$\gamma = 1/14$$.

The mortality rate (fraction of fatal infections) governs $$\delta$$. The mortality rate is extremely hard to estimate, as one must know both the number of fatalities from the disease (which is generally easy to measure), and the total number of cases, which is much harder to measure. Not all infected people are tested, and are therefore not counted as having the disease. This is a mechanism by which it is easy to *overestimate* the mortality rate of the infection. The mortality rate is of course strongly effected by available medical care. Testing lots and testing early has two advantages:
 - You can prepare
   - by quarantining people who have no/little symptoms but can infect others to reduce overall infected population (reducing the $$\beta$$ parameter)
   - by getting your medical care systems ready to deal with the symptomatic cases where it is needed -  resulting in (hopefully) fewer deaths.
 - Your country gets the benefit of reporting a low mortality rate, because you have a better (larger) idea of how many people actually have the disease.
 
The former is of course much less important for your population, but is interesting for the purpose of getting the best handle on the data.

#### Recovery and Death

$$ \frac{\text{d}r}{\text{d}t} = \gamma\ i(t) $$

$$ \frac{\text{d}d}{\text{d}t} = \delta\ i(t) $$

The recovered and dead population increases as described above.

#### Reproduction number and other parameters

The number,

$$ R_0 = \frac{\beta}{\gamma} $$

is known as the basic reproduction number (or ratio). It can be interpreted as the number of new infections caused by a single infection. I.e. if you're sick, how many people catch it.

The other interesting parameters to extract are:
 - the time between contacts (infection transmissions)
 
 $$ T_c = \frac{1}{\beta}, $$
 
 - the recovery time as discussed above,
 
 $$ T_r = \frac{1}{\gamma} $$
 
 - and the mortality rate
 
 $$ m = \frac{\text{Number of deaths}}{\text{Number of infections}} = \frac{\delta}{\gamma} $$


#### Results

The plot below shows a typical outcome for letting the simulation run, assuming a tenth of a billion of the population starts with the disease, each person infects 2.5 other people ($$R_0 = 2.5$$), they are infected for 14 days ($$\gamma = 1/14$$), and 2.5% of people who become infected die ($$ \delta = 0.025 \gamma$$).

![Single SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/SingleRun.png)

If we allow for a 10% standard deviation for each of the infection parameters, and randomly sample from the possibilities, then we get a range of possible trajectories as shown below.

![Monte-Carlo SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/MCSIRD.png)

#### Model Behaviour

In terms of the properties defined above, we can explore some predictions of the SIRD model. In the figure below, we look at:
 - The peak infected population - the maximum fraction of the population to infected at the same time.
 - The total infected population - the total fraction of the population that has been infected at some time.
 - The duration of the outbreak, defined as the amount of time spent with the number of people currently infected, greater than half of the peak as described above. (The Full-Width Half-Maximum or FWHM width of the infection peak)

![Behaviours of the SIRD model](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/ModelProperties.png)

#### Lock-down Bubbles

Consider also, that during a lock down, we are kept in small groups or "bubbles", who are each in close contact inside the group, but the groups are isolated from each other. To reduce the time we need to be locked down, we need the virus to die off quickly. This means:
 - Zero transmission and let people recover, or
 - Quick transmission so that the virus is unable to spread quickly, because most people have it. (Herd immunity)

The latter has a large number of cases of infection, and subsequently deaths, so let's not do this to the entire population. Locking down hopefully (nearly) eliminates transmission between our bubbles. The somewhat controversial part - we then also kinda want fast transmission inside the bubble - ideally, we want to isolate any sick people, but if people sharing a bubble are going to get it anyway, the sooner the better so bubbles recover (and become no longer infectious to the larger population) faster. A quick look at this process, only taking into account the fact that a sick member of a bubble means a larger starting fraction of the virus can be seen in the following figure. The bold line is for a bubble of four people.

![Bubble SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/SmallBubble.png)

<!--
#### Fitting

We can fit the data collected to the "infected" part of the SIRD model we discussed above. For the following calculation, I have assumed the the death rate is zero, and used the parameters I discussed above as the starting point for the curve fit. Please note that the follow graph:
 - Assumes that $$\beta$$ and $$\gamma$$ are constant - this should be vastly changed by the lockdown,
 - Assumes that the entire population of NZ is accessible to the virus. Hopefully this is not the case in the lockdown,
 - Doesn't take into account the recovered cases (as the data is less availble), which encourages the fit to think that things are growing faster than they might be,
 - Shows that when the govenment keeps saying that what happens in the next 10 days will be interesting, that they're right!
 

![Fitting a SIR(D=0) model to NZ data](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZSIRDFit.png)

We're doing a lot to attempt to prevent the above explosion of cases from happening.
-->
