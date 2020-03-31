## A quick look at COVID-19

Firstly, I should mention my data sources. International data is taken from [JHU CSSE](https://github.com/CSSEGISandData/COVID-19.git), who has a nice [map and monitoring dashboard](https://coronavirus.jhu.edu/map.html). New Zealand data is taken directly from the [Ministry of Health](https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus). They keep changing their data format...

Secondly, and probably more importantly: Take care of yourself. Don't get stupid ideas from my silly graphs and panic, or lull yourself into a false sense of security. I take no responsibility for how these are used. I also apologise for not making everything more pretty / understandable. Maybe it will get there.

### The SIRD Model

Disclaimer - The following investigation is not fitted to the data, but is loosely based on COVID. This should not be taken too seriously.

The Susceptible, Infected, Recovered, Dead (SIRD) model is simply a set of differential equations specifying the rate of infection and recovery in terms of the population in each of these stages of the disease, and some coefficients.

The plot below shows a typical outcome for letting the simulation run, assuming a tenth of a billion of the population starts with the disease, each person infects 2.5 other people, they are infected for 14 days, and 2.5% of people who become infected die.

![Single SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/SingleRun.png)

If we allow for a 10% standard deviation for each of the infection parameters, and randomly sample from the possibilities, then we get a range of possible trajectories as shown below.

![Monte-Carlo SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/MCSIRD.png)

Consider also, that during a lock down, we are kept in small groups or "bubbles", who are each in close contact inside the group, but the groups are isolated from each other. To reduce the time we need to be locked down, we need the virus to die off quickly. This means:
 - Zero transmission and let people recover, or
 - Quick transmission so that the virus is unable to spread quickly, because most people have it. (Herd immunity)

The latter has a large number of cases of infection, and subsequently deaths, so let's not do this to the entire population. Locking down hopefully (nearly) eliminates transmission between our bubbles. The somewhat controversial part - we then also kinda want fast transmission inside the bubble - ideally, we want to isolate any sick people, but if people sharing a bubble are going to get it anyway, the sooner the better so bubbles recover (and become no longer infectious to the larger population) faster. A quick look at this process, only taking into account the fact that a sick member of a bubble means a larger starting fraction of the virus can be seen in the following figure. The bold line is for a bubble of four people.

![Bubble SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/SmallBubble.png)



### The New Zealand Situation

![NZ's new cases per day](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZCasesPerDay.png)

![NZ's Total Cases, Linear Scale](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZCases.png)

![NZ's Total Cases, Log Scale](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZCasesLog.png)

Especially, consider this split up by District Health Board.

![NZ's Total Cases, By DHB](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZByDHB.png)

And taking into account how many people are actually serviced by that District Health Board, we see that the Southern district has an unfair share of the number of cases.
![NZ's Total Cases, By DHB Per Capita](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZByDHBPerCap.png)

### NZ vs The World
In each of these graphs, New Zealand's state is shown in black. (GO THE BLACKS! Oh wait... no sport in a lock-down.)

![International Cases, Log Scale](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/NZvsWorld.png)

But more interestingly, consider our growth rate. Firstly, let's take a look at the trajectory we're taking compared to other countries since each hit 10 cases.

![International Cases, from 10 cases](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/Comparason.png)

And finally, another check to see if we're getting away from exponential growth. The following figure shows the number of new cases over the previous week, against the total number of cases. This is a straight rising line for exponential growth (thinking back to a little calculus: the derivative of exp(x) is exp(x), so the rate of change of exponential growth is proportional to the exponential growth itself). What we really want to see is something other than a straight line going up. We want to see it go drastically down, to zero new cases.

![International Cases, from 10 cases](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/ExponentialGrowth.png)


