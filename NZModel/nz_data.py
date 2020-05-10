import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re

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

#date_column = date_column_sus = "Date of report"
header=3
#filename = "covidcase_list_1_apr_2020.xlsx"
date_column = date_column_sus = "Date notified of potential case"
#filename = "covid-cases-7may20.xlsx"
filename = "covid-cases10_may_2020-updated.xlsx"

# The data keeps getting worse *sigh*
def date_decoder(x):
    # test that we're getting the strings (or array of) that we want

    if isinstance(x, list) and len(x) > 0:
        if not isinstance(x[0], str) or not isinstance(x[0], unicode):
            return x
        
    return pd.to_datetime(x, format="%d/%m/%Y", exact=False)

# Confirmed Infection Cases
data_conf = pd.read_excel(filename, header=header, parse_dates=[date_column], date_parser=date_decoder, encoding = 'utf8')

# Suspected Infection Cases
data_sus = pd.read_excel(filename, header=header, sheet_name=1, parse_dates=[date_column_sus], date_parser=date_decoder, encoding = 'utf8')

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
    plt.title("NZ COVID-19 Cases")
    
    plt.xticks(rotation=20)
    plt.tight_layout()

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
    plt.title("NZ COVID-19 Cases")
    plt.legend(["Total Cases", "Suspected Cases"])
    plt.savefig("NZCases.png")

    plt.gca().set_yscale('log')
    plt.title("NZ COVID-19 Cases - Log Scale")
    plt.savefig("NZCasesLog.png")


###################################################################
#   DHB Breakdown
###################################################################
def plot_dhb():
    
    plt.figure()
    
    pi = data.pivot_table(index = [date_column,"DHB"], aggfunc="size")

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
    dhb_data = pd.read_excel(dhb_file, header=None, names=["DHB", "Population"], usecols=[0,2], skiprows=7, skipfooter=1, encoding = 'utf8')

    for DHB in DHBs:
        # Replace macron a with normal a to make it compatable
        filters = dhb_data['DHB'] == DHB.replace(u'\u0101', 'a');
        pop = dhb_data["Population"].where(filters).sum() # Should only be one element anyway
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

    plt.figure(figsize=(6.4,4))
    age = "Age group"
    data[age].replace(' ', np.nan, inplace=True)
    data[age].fillna("Unspecified", inplace=True)

    def reformat_age_range(label):
        label = label.strip()

        if label[0] == '<':
            return '00 to %02d' % int(label[1:])
        elif label[-1] == '+':
            return str(int(label[:-1])) + '+'
        elif label == "Unspecified":
            return label
        else:
            x = [int(x) for x in label.split(' to ')]
            return "%02d to %02d" % (x[0], x[1])
        
    # Clean up ages
    data[age] = data[age].map(reformat_age_range)
    
    pi1 = data.pivot_table(index = ["DHB", age], aggfunc="size")

    DHBs = pi1.index.levels[0]

    running_totals = np.zeros((len(DHBs)))

    groups = list(pi1.index.levels[1])

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
    plt.tight_layout(rect=(0,0,0.8,1))

    plt.savefig("AgeDHB.png")

    ###################################################################
    #   Age Breakdown - Gender
    ###################################################################
    plt.figure(figsize=(6.4,3))
    data["Sex"].fillna("Unspecified", inplace=True)
    pi1 = data.pivot_table(index = ["Age group", "Sex"], aggfunc="size")

    groups = list(pi1.index.levels[0])

    sexes =  list(pi1.index.levels[1])

    running_totals = np.zeros((len(groups)))

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

    plt.tight_layout(rect=(0,0,0.8,1))
    plt.savefig("AgeSex.png")

    ###################################################################
    #   Pie Breakdowns
    ###################################################################
    plt.figure(figsize=(6.4,4))

    plt.subplot(1,2,1)
    plt.title("Sex")
    cmap = cm.get_cmap('Set2')
    plt.gca().set_prop_cycle(color=[cmap(5), cmap(2), cmap(1)])

    pi1 = data.pivot_table(index = ["Sex"], aggfunc="size")
    plt.pie(pi1.values, labels=pi1.index.values, autopct='%1.1f%%')
    plt.gca().set_aspect("equal")


    travel = "Overseas travel"
    plt.subplot(1,2,2)
    cmap = cm.get_cmap('Set2')
    plt.gca().set_prop_cycle(color=cmap(np.arange(5)))
    plt.title("Overseas Travel")
    data[travel].replace(' ', np.nan, inplace=True)
    data[travel].fillna("Unspecified", inplace=True)
    pi = data.pivot_table(index = [travel], aggfunc="size")
    plt.pie(pi.values, labels=pi.index.values, autopct='%1.1f%%',)
    plt.gca().set_aspect("equal")

    plt.savefig("Pies.png")
    
    ###################################################################
    #   Imports
    ###################################################################
    
    plt.figure()
    pi = data.pivot_table(index = ["Last country before return"], aggfunc="size")
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
