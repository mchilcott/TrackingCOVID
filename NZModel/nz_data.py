 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#filename = "covid-19-confirmed-cases-28mar20.xlsx"
#date_column = "Report Date"
#header = 3
#filename = "covid-19-confirmed-probable-cases-29mar20.xlsx"
#date_column = date_column_sus = "Date of report"
#header=0
#filename = "covid-cases-30_mar_2020.xlsx"
#date_column = "Report Date"
#date_column_sus = "ReportDate"
#header=3
filename = "covidcase_list_31_mar_2020_for_web_-_updated.xlsx"
date_column = date_column_sus = "Date of report"
header=3


data = pd.read_excel(filename, header=header)

# Suspected
data_sus = pd.read_excel(filename, header=header, sheet_name=1)


rates = data[date_column].value_counts()
rates = rates.sort_index()

rates_sus = data_sus[date_column_sus].value_counts().sort_index()

rates_total = rates_sus.add(rates, fill_value = 0)

plt.figure()


#rates_total.plot(style = 'c-')
#d = rates_total.index.values # For Numpy
#plt.fill_between(d, rates_total, alpha=0.5, color='c')

d = rates_total.index.values # For Numpy
plt.bar(d, rates_total)

d = rates_sus.index.values # For Numpy
plt.bar(d, rates_sus)


plt.legend(["Confirmed Cases", "Suspected Cases"])


#rates.plot.bar()
#rates_sus.plot.bar()

plt.xlabel("Date")
plt.ylabel("Cases per day")
plt.title("NZ COIVD-19 Cases")

plt.savefig("NZCasesPerDay.png")

plt.figure()

rc_sus = rates_sus.cumsum()
rc_total = rates_total.cumsum()

rc_total.plot(style = '.-')
d = rc_total.index.values # For Numpy
plt.fill_between(d, rc_total, alpha=0.5)

rc_sus.plot(style = '.-')
d = rc_sus.index.values # For Numpy
plt.fill_between(d, rc_sus, alpha=0.5)

plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.title("NZ COIVD-19 Cases")
plt.legend(["Total Cases", "Suspected Cases"])
plt.savefig("NZCases.png")
plt.gca().set_yscale('log')
plt.savefig("NZCasesLog.png")

plt.figure()

data = data.append(data_sus, sort=True)
data.sort_index()
# Add a dummy column for counting
data.insert(len(data.columns), "Count", [1] * len(data))

tb = data.pivot_table(values="Count", index = [date_column,"DHB"], aggfunc="count")
pi = tb['Count']

DHBs = pi.keys().levels[1]

for DHB in DHBs:
    series = pi[:, DHB].cumsum()
    ax = series.plot(label=DHB, alpha=0.8)
    line= ax.lines[-1]
    plt.text(line._x[-1] + np.random.rand()*8, series[-1], DHB, color=line.get_color(), alpha=0.8)
    
x = plt.xlim()
plt.xlim((x[0], x[1] + 10))
plt.ylabel("Total Reported Cases")
plt.title("Cases by DHB")
plt.savefig("NZByDHB.png")

plt.figure()

dhb_file = "DHBPopulations.xlsx"
dhb_data = pd.read_excel(dhb_file, header=None, names=["DHB", "Population"], usecols=[0,2], skiprows=7, skipfooter=1)

for DHB in DHBs:
    pop = dhb_data["Population"].where(dhb_data['DHB'] == DHB).sum()
    series = pi[:, DHB].cumsum() / pop * 1e6
    ax = series.plot(label=DHB, alpha=0.8)
    line= ax.lines[-1]
    plt.text(line._x[-1] + np.random.rand()*8, series[-1], DHB, color=line.get_color(), alpha=0.8)
    
x = plt.xlim()
plt.xlim((x[0], x[1] + 10))
plt.ylabel("Reported Cases per Capita [ppm]")
plt.title("Cases by DHB")
plt.savefig("NZByDHBPerCap.png")

plt.show()
