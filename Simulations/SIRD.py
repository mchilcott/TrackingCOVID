# A simple SIRD model. With some numbers based on COVID

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt

recovery_time = 14.0 # days
infetion_rate = 2.5 # people infected per infectous person - This is the basic reproduction number
death_rate = 0.025 # Fraction of infected that die

beta = infetion_rate / recovery_time
gamma = 1.0/recovery_time
delta = death_rate / recovery_time

def do_sird(
    beta = infetion_rate / recovery_time,
    gamma = 1.0/recovery_time,
    delta = death_rate / recovery_time,
    y0=[1.0, 1e-7, 0, 0], t_max = 400):

    def sird_dot (y, t):
        [s, i, r, d] = y
        
        dydt = [
            -s*i*beta,
            s*i*beta - gamma * i - delta * i,
            gamma * i,
            delta * i
            ]
        return dydt


    t = np.linspace(0,t_max, 2000)
    y = scipy.integrate.odeint(sird_dot, y0, t)
    
    return t,y


def do_simple():
    t,y = do_sird()
    plt.figure()
    plt.plot(t,y)
    plt.xlabel("Time [days]")
    plt.ylabel("Fraction of population")
    plt.title("SIRD Model")
    plt.legend(["Susceptable", "Infected", "Recovered", "Dead"])
    plt.savefig("SingleRun.png")

def MC_variance():
    def dither(value, length = 100, error = 0.1):
        return value + np.random.randn(length) * value * error

    plt.figure()

    samples = 100
    recovery_time = dither(14.0, samples) # days
    infetion_rate = dither(2.5, samples) # people infected per infectous person - This is the basic reproduction number
    death_rate = dither(0.025, samples) # Fraction of infected that die

    y_lots = []

    for i in range(samples):
        t,y = do_sird(
                infetion_rate[i] / recovery_time[i],
                1.0/recovery_time[i],
                death_rate[i] / recovery_time[i]
            )
        y_lots.append(y)

    y_lots = np.array(y_lots)

    upper = np.max(y_lots, axis=0)
    lower = np.min(y_lots, axis=0)
    mean  = np.mean(y_lots, axis=0)

    plt.plot(t, mean)
    for i in range(4):
        plt.fill_between(t, upper[:,i], lower[:,i], alpha=0.1)
        
    for i in range(samples):
        # reset colours
        plt.gca().set_prop_cycle(None)
        plt.plot(t, y_lots[i], alpha = 0.1)

    # Overlay it on top again. Need it at the start to get the legend right
    plt.gca().set_prop_cycle(None)
    plt.plot(t, mean)

    plt.xlabel("Time [days]")
    plt.ylabel("Fraction of population")
    plt.title("SIRD Model")
    plt.legend(["Susceptable", "Infected", "Recovered", "Dead"])

    plt.savefig("MCSIRD.png")

def small_bubbles():
    plt.figure()
    y_lots = []
    
    num_in_bubble = range(2,8)
    
    for i in num_in_bubble:
        t,y = do_sird(y0 = [1 - 1.0/i, 1.0/i, 0, 0], t_max=10*7)
        y_lots.append(y)

    y_lots = np.array(y_lots)


    plt.plot(t, y_lots[1])

    for i in range(len(num_in_bubble)):
        # reset colours
        plt.gca().set_prop_cycle(None)
        plt.plot(t, y_lots[i], alpha = 0.1)

    # Overlay it on top again. Need it at the start to get the legend right
    plt.gca().set_prop_cycle(None)
    plt.plot(t, y_lots[1])

    plt.xlabel("Time [days]")
    plt.ylabel("Fraction of population")
    plt.title("SIRD Model")
    plt.legend(["Susceptable", "Infected", "Recovered", "Dead"])

    plt.savefig("SmallBubble.png")
    


if __name__ == "__main__":
    do_simple()
    MC_variance()
    small_bubbles()
    plt.show()
