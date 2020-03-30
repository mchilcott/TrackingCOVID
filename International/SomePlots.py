 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


stats = ["confirmed", "deaths", "recovered"]

file_template = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_%s_global.csv"

# Load file
data = pd.read_csv(file_template % stats[0], header=0, index_col=[0,1,2,3,])

# Take the transpose
data = data.T

# Reinterpret the dates (Stupid American Format)
dates = pd.to_datetime(data.index, format='%m/%d/%y')
data.index = dates

data = data.T

t = data.pivot_table(columns="Country/Region", aggfunc="sum")
nz = "New Zealand"

for country in t:
    t[country].plot(style='-', alpha=0.3)

t[nz].plot(style='k-', linewidth=2)
plt.gca().set_yscale('log')
plt.title("NZ vs Rest of the World")
plt.ylabel("Confirmed Cases")
plt.xlabel("Date")
plt.tight_layout()
plt.savefig("NZvsWorld.png")


plt.figure()
delta = t.diff()
delta = delta.rolling(7).sum()


for country in t:
    plt.loglog(t[country], delta[country], alpha=0.2)
plt.loglog(t[nz], delta[nz], color='k', linewidth=2)
plt.title("Rate of Growth")
plt.ylabel("New Cases")
plt.xlabel("Total Confirmed Cases")
plt.tight_layout()
plt.savefig("ExponentialGrowth.png")

plt.figure()

for country in t:
    d_tmp = np.array(t[country])
    to_plot = d_tmp[d_tmp >= 10]
    plt.semilogy(to_plot, alpha=0.2)
    if country == nz:
        plt.semilogy(to_plot, color='k', linewidth=2)
plt.title("Comparative Rate of Growth")
plt.ylabel("Total Cases")
plt.xlabel("Days since 10 cases")
plt.tight_layout()
plt.savefig("Comparason.png")

plt.show()
