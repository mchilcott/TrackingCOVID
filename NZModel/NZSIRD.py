 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit


import sys
sys.path.append("../Simulations")

from nz_data import rates_total
from SIRD import do_sird
from data_analysis import monte_carlo_fit, convergence_plots

nz_population = 4.93e6

rc_total = rates_total.cumsum()
d = rc_total.index.values # For Numpy

rc_total_prop = rc_total.values / nz_population
day = np.array((d -d[0]) / (24*3600*1e9), dtype='float')

init_i = rc_total_prop[0]
max_days = np.max(day)

# The SIR model does have an analytic solution, but I'm going to play with the numerics.
# Going to assume delta (death rate) = 0 for variety

def curve(x, beta, gamma):
    t, y = do_sird(beta, gamma, 0, [1, init_i, 0, 0], max_days, max_days)

    return np.interp(x, t, y[:, 1])

mean, low, high, std, popt = monte_carlo_fit({'f': curve, 'p0': [2.0/14, 1.0/14]}, day, rc_total_prop)

reproduction_tests = popt[:,0] / popt[:,1]

recovery_tests = 1/popt[:,1]

print("Reproduction Number = %f, (%f, %f)" % (np.mean(reproduction_tests), np.percentile(reproduction_tests, 2.5), np.percentile(reproduction_tests, 97.5)))
print("Recovery Time = %f, (%f, %f)" % (np.mean(recovery_tests), np.percentile(recovery_tests, 2.5), np.percentile(recovery_tests, 97.5)))

for row in popt:
    t, y = do_sird(row[0], row[1], 0, [1, init_i, 0, 0], max_days * 1.2)
    plt.plot(t, y[:,1], 'k', alpha=0.1)

t, y = do_sird(mean[0], mean[1], 0, [1, init_i, 0, 0], max_days * 1.2)
plt.plot(t, y[:,1], 'k')

plt.plot(day, rc_total/nz_population, 'o')

plt.title("Fitting NZ data to SIR Model")
plt.xlabel("Days since infection reached NZ")
plt.ylabel("Fraction of population infected")

(_, ymax) = plt.ylim()

plt.text(5, ymax*0.9, "Reproduction Number = %.2f, (%.2f, %.2f)" % (np.mean(reproduction_tests), np.percentile(reproduction_tests, 2.5), np.percentile(reproduction_tests, 97.5)))
plt.text(5, ymax*0.8, "Recovery Time = %.2f, (%.2f, %.2f) days" % (np.mean(recovery_tests), np.percentile(recovery_tests, 2.5), np.percentile(recovery_tests, 97.5)))

plt.tight_layout()
plt.savefig("NZSIRDFit.png")

plt.show()
