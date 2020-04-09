# A simple SIRD model. With some numbers based on COVID

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

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
    y0=[1.0, 1e-7, 0, 0], t_max = 400, t_points = 2000):

    def sird_dot (y, t):
        [s, i, r, d] = y
        
        dydt = [
            -s*i*beta,
            s*i*beta - gamma * i - delta * i,
            gamma * i,
            delta * i
            ]
        return dydt


    t = np.linspace(0,t_max, t_points)
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
        plt.plot(t, y_lots[i], alpha = 0.3)

    # Overlay it on top again. Need it at the start to get the legend right
    plt.gca().set_prop_cycle(None)
    plt.plot(t, y_lots[1])

    plt.xlabel("Time [days]")
    plt.ylabel("Fraction of population")
    plt.title("SIRD Model")
    plt.legend(["Susceptable", "Infected", "Recovered", "Dead"])

    plt.savefig("SmallBubble.png")
    
def model_analysis_plots():
    
    # Things to investigate:
    # Duration of infection (fwhm)
    # Total Population infected
    # Peak Infection

    x = np.linspace(1, 3, 70)
    y = np.linspace(1,15, 70)
    
    # do_sird( beta=infetion_rate / recovery_time, gamma=1.0/recovery_time, delta=0, y0=[1.0, 1e-7, 0, 0], t_max = 1000, t_points = 1000):

    fwhm = []
    max_infection = []
    total_infection = []

    xv, yv = np.meshgrid(x, y)
    for i in range(len(x)):
        for j in range(len(y)):
            # treat xv[j,i], yv[j,i]
            t, sird = do_sird( beta=xv[j,i]/yv[j,i], gamma=1./yv[j,i], delta=0, y0=[1.0, 1e-4, 0, 0], t_max=3000, t_points=3000)
            
            infected = sird[:,1]
            
            r = sird[:,2]
            
            peak = np.max(infected)

            ti = r[-1]

            duration = np.sum(infected > (peak/2))
            if infected[-1] > (peak/2):
                duration = float('NaN')

            if infected[-1] == peak:
                duration = float('NaN')
                peak = float('NaN')
                ti = float('NaN')
            
            fwhm.append(duration)
            max_infection.append(peak)
            
            total_infection.append(ti)
                

    fwhm = np.array(fwhm).reshape(len(y), len(x)).T
    max_infection = np.array(max_infection).reshape(len(y), len(x)).T
    total_infection = np.array(total_infection).reshape(len(y), len(x)).T

    def my_im_plot(x,y,z, *args, **kwargs):
        dx = (x[0,1]-x[0,0])/2.
        dy = (y[1,0]-y[0,0])/2.
        extent = (x[0,0]-dx, x[0,-1]+dx, y[-1,0]-dy, y[0,0]+dy)
        im = plt.imshow(z, extent=extent, aspect='auto')
        plt.colorbar(im)
        
    plt.figure(figsize=(8,12))
    plt.subplot(3,2,1)
    my_im_plot(xv,yv,fwhm, 'Days')
    plt.xlabel("Infection Rate")
    plt.ylabel("Recovery Time")
    plt.title("Infection Duration (FWHM)")
   
    plt.subplot(3,2,3)
    my_im_plot(xv,yv,max_infection)
    plt.xlabel("Infection Rate")
    plt.ylabel("Recovery Time")
    plt.title("Peak infected population")

    plt.subplot(3,2,5)
    my_im_plot(xv,yv,total_infection)
    plt.xlabel("Infection Rate")
    plt.ylabel("Recovery Time")
    plt.title("Total population infected")
    
    idy = 20
    plt.subplot(3,2,2)
    colour = 'tab:blue'
    plt.plot(x, fwhm[idy, :], color=colour)
    plt.xlabel("Infection Rate (Recovery Time = %.1f days)" % y[idy], color=colour)
    plt.gca().tick_params(axis='x', labelcolor=colour)
    plt.ylabel("Infection Duration [Days]")
    
    ax2 = plt.twiny()
    idx = 20
    colour = 'tab:red'
    ax2.plot(y, fwhm[:, idx], color=colour)
    ax2.set_xlabel("Recovery Time (Infection Rate = %.1f days)" % x[idx], color=colour)
    ax2.tick_params(axis='x', labelcolor=colour)
    
    

    plt.subplot(3,2,4)
    plt.plot(x, max_infection[len(y)/2, :])
    plt.xlabel("Infection Rate")
    plt.ylabel("Population Fraction")
    plt.title("Peak infected population")

    plt.subplot(3,2,6)
    plt.plot(x, total_infection[len(y)/2, :])
    plt.xlabel("Infection Rate")
    plt.ylabel("Population Fraction")
    plt.title("Total population infected")
    plt.tight_layout()

    plt.savefig("ModelProperties.png")
    
if __name__ == "__main__":
    #do_simple()
    #MC_variance()
    #small_bubbles()
    model_analysis_plots()
    
    
    plt.show()
