 
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
emphasis_countries = [("China", 'r'),("US", 'g'),("Australia", 'y'),("United Kingdom", 'b'), ("New Zealand", 'k')]

for country in t:
    t[country].plot(style='-', alpha=0.3, label=None)

for country, colour in emphasis_countries:
    t[country].plot(color=colour, label=country, linewidth=2)
plt.gca().set_yscale('log')
plt.title("Worldwide Cases by Country")
plt.ylabel("Confirmed Cases")
plt.xlabel("Date")
#plt.legend()
plt.tight_layout()
plt.savefig("NZvsWorld.png")
plt.gca().set_yscale('linear')
plt.tight_layout()
plt.savefig("NZvsWorldLinear.png")


plt.figure()
delta = t.diff()
delta = delta.rolling(7).sum()

#Window it a bit

for country in t:
    plt.loglog(t[country], delta[country], alpha=0.3, label=None)
for country, colour in emphasis_countries:
    plt.loglog(t[country], delta[country], color=colour, alpha=0.8, label=country, linewidth=2)
    plt.loglog(t[country][-1], delta[country][-1], 'o', color=colour, alpha=0.8)
plt.title("Rate of Growth")
plt.ylabel("New Cases")
plt.xlabel("Total Confirmed Cases")
#plt.legend()
plt.tight_layout()
plt.savefig("ExponentialGrowth.png")

plt.figure()
plt.yscale('log')


for country in t:
    d_tmp = np.array(t[country])
    to_plot = d_tmp[d_tmp >= 10]
    plt.semilogy(to_plot, alpha=0.3, label=None)

for rate in [2, 5]:
    label = "Doubling every %d days" % rate
    x = np.linspace(0, 70, 100)
    y = 2 ** (x / rate) * 10
    y[y > 1e6] = float('NaN')
    plt.semilogy(x, y, '--', alpha=0.5, color = 'k')
    
    i = np.argmax(np.nan_to_num(y,0))
    
    pos = int(3*i/5)
    
    angle_data = np.rad2deg(np.arctan2(y[pos]-y[pos-2], x[pos]-x[pos-2]))

    # angle in screen coordinates
    angle_screen = plt.gca().transData.transform_angles(np.array((angle_data,)), 
                                              np.array([x[pos], y[pos]]).reshape((1, 2)))[0]
    
    plt.gca().annotate(label, xy=(x[pos],y[pos]), xytext=(5,5), textcoords="offset points", 
                rotation_mode='anchor', rotation=angle_screen, alpha=0.5).set_bbox(
                dict(facecolor='w', alpha=0.7, edgecolor='k', linewidth=0)) 

for country, colour in emphasis_countries:
    d_tmp = np.array(t[country])
    to_plot = d_tmp[d_tmp >= 10]
    plt.semilogy(to_plot, color=colour, alpha=0.8, label=country)

plt.title("Comparative Rate of Growth")
plt.ylabel("Total Cases")
plt.xlabel("Days since 10 cases")
plt.tight_layout()
plt.savefig("Comparason.png")

plt.show()
