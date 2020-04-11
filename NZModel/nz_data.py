 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

###################################################################
#   Data files
###################################################################

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
#filename = "covidcase_list_31_mar_2020_for_web_-_updated.xlsx"

date_column = date_column_sus = "Date of report"
header=3
#filename = "covidcase_list_1_apr_2020.xlsx"
#filename = "./covid-19_case_list_2_april_2020.xlsx"
#filename = "./covid-19-case-details-update-3-april-2020.xlsx"
#filename = "./covid-19-case-details-update-4-april-2020.xlsx"
#filename = "./covid-casedetialsupdate-5april.xlsx"
#filename = "./covid-casedetails-update-6april.xlsx"
#filename = "covid-casedetails-8april2020.xlsx"
#filename = "covid-casedetails-9april2020.xlsx"
#filename = "covid-casedetails-10april2020.xlsx"
filename = "case-list-11-april-2020-for-web.xlsx"

# Confirmed Infection Cases
data_conf = pd.read_excel(filename, header=header)

# Suspected Infection Cases
data_sus = pd.read_excel(filename, header=header, sheet_name=1)

# infection rates
rates = data_conf[date_column].value_counts()
rates = rates.sort_index()

# Suspected
rates_sus = data_sus[date_column_sus].value_counts().sort_index()

# Total = Confirmed + Suspected
rates_total = rates.add(rates_sus, fill_value = 0)

# Concatenate all data for summary statistics
data = data_conf.append(data_sus, sort=True)
data.sort_index()
# Add a dummy column for counting
data.insert(len(data.columns), "Count", [1] * len(data))

###################################################################
#   New Cases daily
###################################################################
def plot_new():
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
    plt.ylabel("New Cases per day")
    plt.title("NZ COIVD-19 Cases")

    plt.savefig("NZCasesPerDay.png")

###################################################################
#   Total Cases 
###################################################################
def plot_total():
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
    plt.title("NZ COIVD-19 Cases - Log Scale")
    plt.savefig("NZCasesLog.png")


###################################################################
#   DHB Breakdown
###################################################################
def plot_dhb():
    plt.figure()



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


    ###################################################################
    #   DHB Per Capita
    ###################################################################

    plt.figure()

    dhb_file = "DHBPopulations.xlsx"
    dhb_data = pd.read_excel(dhb_file, header=None, names=["DHB", "Population"], usecols=[0,2], skiprows=7, skipfooter=1)

    for DHB in DHBs:
        pop = dhb_data["Population"].where(dhb_data['DHB'] == DHB).sum() # Should only be one element anyway
        series = pi[:, DHB].cumsum() / pop * 1e6
        ax = series.plot(label=DHB, alpha=0.8)
        line= ax.lines[-1]
        plt.text(line._x[-1] + np.random.rand()*6, series[-1], DHB, color=line.get_color(), alpha=0.8)
        
    x = plt.xlim()
    plt.xlim((x[0], x[1] + 15))
    plt.ylabel("Reported Cases per Capita [ppm]")
    plt.title("Cases by DHB")
    plt.savefig("NZByDHBPerCap.png")


def plot_demographics():
    ###################################################################
    #   Age Breakdown - DHB
    ###################################################################

    plt.figure(figsize=(8,4))

    tb1 = data.pivot_table(values="Count", index = ["DHB", "Age group"], aggfunc="count")
    pi1 = tb1["Count"]

    DHBs = pi1.index.levels[0]

    running_totals = np.zeros((len(DHBs)))

    groups = list(pi1.index.levels[1])

    # Fix the <1 problem in a really bad way. I'm tired
    t = groups[2]
    groups[2] = groups[1]
    groups[1] = groups[0]
    groups[0] = t

    cmap = cm.get_cmap('rainbow')

    plt.gca().set_prop_cycle(color=cmap(np.linspace(0,1,len(groups))))

    for age_group in groups:
                            
        series = pi1[:, age_group]
                            
        d = np.array([DHBs.get_loc(x) for x in series.index.values]) # For Numpy
        y = series.values
        plt.barh(-d, y, left=running_totals[d], label=age_group)
        
        running_totals[d] += y


    plt.title("Area breakdown by Age")
    plt.ylabel("DHB")
    plt.xlabel("Cases")
    plt.yticks(-1 * np.arange(len(DHBs)))
    plt.gca().set_yticklabels(DHBs)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout(rect=(0,0,0.85,1))

    plt.savefig("AgeDHB.png")

    ###################################################################
    #   Age Breakdown - Gender
    ###################################################################
    plt.figure(figsize=(8,3))
    tb1 = data.pivot_table(values="Count", index = ["Age group", "Sex"], aggfunc="count")
    pi1 = tb1["Count"]

    groups = list(pi1.index.levels[0])

    sexes =  list(pi1.index.levels[1])

    running_totals = np.zeros((len(groups)))

    # Fix the <1 problem in a really bad way. I'm tired
    t = groups[2]
    groups[2] = groups[1]
    groups[1] = groups[0]
    groups[0] = t

    cmap = cm.get_cmap('Set2')
    plt.gca().set_prop_cycle(color=[cmap(5), cmap(2), cmap(1)])

    for sex in sexes:
                            
        series = pi1[:, sex]
                            
        d = np.array([groups.index(x) for x in series.index.values]) # For Numpy
        y = series.values
        plt.barh(-d, y, left=running_totals[d], label=sex)
        
        running_totals[d] += y


    plt.yticks(-1 * np.arange(len(groups)))
    plt.gca().set_yticklabels(groups)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title("Age breakdown by Sex")
    plt.ylabel("Age Group")
    plt.xlabel("Cases")

    plt.tight_layout(rect=(0,0,0.85,1))
    plt.savefig("AgeSex.png")

    ###################################################################
    #   Pie Breakdowns
    ###################################################################
    plt.figure(figsize=(8,4))

    plt.subplot(1,2,1)
    plt.title("Sex")
    cmap = cm.get_cmap('Set2')
    plt.gca().set_prop_cycle(color=[cmap(5), cmap(2), cmap(1)])

    tb1 = data.pivot_table(values="Count", index = ["Sex"], aggfunc="count")
    pi1 = tb1["Count"]
    plt.pie(pi1.values, labels=pi1.index.values, autopct='%1.1f%%')
    plt.gca().set_aspect("equal")

    plt.subplot(1,2,2)
    cmap = cm.get_cmap('Set2')
    plt.gca().set_prop_cycle(color=cmap(np.arange(5)))
    plt.title("International Travel")
    data["International travel"] = data["International travel"].fillna("Unspecified")
    pi = data.pivot_table(values="Count", index = ["International travel"], aggfunc="count")["Count"]
    plt.pie(pi.values, labels=pi.index.values, autopct='%1.1f%%',)
    plt.gca().set_aspect("equal")

    plt.savefig("Pies.png")
    
    ###################################################################
    #   Imports
    ###################################################################
    
    plt.figure()
    pi = data.pivot_table(values="Count", index = ["Last country before return"], aggfunc="count")["Count"]
    pi.plot.barh()
    plt.title("Last Contry Before Return")
    plt.tight_layout()
    plt.savefig("ImportedCases.png")


if __name__ == "__main__":
    plot_new()
    plot_total()
    plot_dhb()
    plot_demographics()

    plt.show()
