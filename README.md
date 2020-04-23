{% include mathjax.html %}

## A quick look at COVID-19

Firstly, I should mention my data sources. International data is taken from [JHU CSSE](https://github.com/CSSEGISandData/COVID-19.git), who has a nice [map and monitoring dashboard](https://coronavirus.jhu.edu/map.html). New Zealand data is taken directly from the [Ministry of Health](https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus). They keep changing their data format...

Secondly, and probably more importantly: Take care of yourself. Don't get stupid ideas from my silly graphs and panic, or lull yourself into a false sense of security. I take no responsibility for how these are used. I also apologise for not making everything more pretty / understandable. Maybe it will get there.

### The SIRD Model

The SIR, SIRD, or SEIR models are ways of investigating the spread of disease. For parameters approximately matching COVID19, the following graph shows a number of possible trajectories for the fraction of the population that is Susceptible, Infected, Recovered or Dead as a function of time. [Here you can find an exploration of the SIRD model.](SIRDModel.md)

![Monte-Carlo SIRD run](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/Simulations/MCSIRD.png)

### The New Zealand Situation

Moving away from the simulations, we can take a look at some real data. Firstly, let's look at some summary statistics of New Zealand's data. Note that the numbers for the last day on these plots represent a less than 24 hour period, and are hence not representative.

Also note that my new cases plot doesn't match the numbers reported by the Ministry of Health (MoH). These graphs are generated from the report data provided, but the MoH back-dates some of these cases, so they show up on the back-date on the following plot, but not in the MoH's totals.

#### New Cases

![NZ's new cases per day](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZCasesPerDay.png)

![NZ's Total Cases, Linear Scale](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZCases.png)

![NZ's Total Cases, Log Scale](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZCasesLog.png)

#### Regions

Especially, consider this split up by District Health Board.

![NZ's Total Cases, By DHB](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZByDHB.png)

And taking into account how many people are actually serviced by that District Health Board, we see that the Southern district has an unfair share of the number of cases.
![NZ's Total Cases, By DHB Per Capita](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/NZByDHBPerCap.png)

#### Demographics

We can also look at the relationship between age, sex and DHB region of the infected.

![Cases in DHB by Age](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/AgeDHB.png)

![Cases in Age group by Sex](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/AgeSex.png)

![Cases by Sex, Travel](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/Pies.png)

For those cases that have involved international travel, we can also see the sources we may have imported COVID-19 from.

![Cases by Country, Imported](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/NZModel/ImportedCases.png)


### NZ vs The World
In each of these graphs, New Zealand's state is shown in black. (GO THE ALL BLACKS! Oh wait... no sport in a lock-down.) For comparason, the other countries in vivid colours are: China in red, US in green, UK in blue, and Australia in yellow.

![International Cases, Log Scale](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/NZvsWorld.png)

Note that this is a log scale, so that we can see what's going on. On a linear plot, we see the small scale of our infection compared to the rest of the world. China is the early riser, and then the US, Italy and Spain surpass China's reported case number, with the US currently in the lead for case number, and still sky-rocketing.

![International Cases, from 10 cases](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/NZvsWorldLinear.png)

#### Growth

Consider our growth rate. Firstly, let's take a look at the trajectory we're taking compared to other countries since each hit 10 cases.

![International Cases, from 10 cases](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/Comparason.png)

And finally, another check to see if we're getting away from exponential growth. The following figure shows the number of new cases over the previous week, against the total number of cases. This is a straight rising line for exponential growth.

(thinking back to a little calculus: $$ \frac{\text{d}}{\text{d}x} e^x = e^x $$, so the rate of change of exponential growth is proportional to the exponential growth itself).

What we really want to see is something other than a straight line going up. We want to see it drop drastically, to zero new cases. This graph is pessimistic however, as it uses the previous week of growth (to get a smooth curve), so there is some delay in showing the deviation from exponential growth.

![International Cases, from 10 cases](https://raw.githubusercontent.com/mchilcott/TrackingCOVID19/master/International/ExponentialGrowth.png)


