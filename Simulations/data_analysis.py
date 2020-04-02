import numpy as np
import numpy.random
import scipy.optimize
import matplotlib.pyplot as plt

def monte_carlo_fit(fit_opt, xdata, ydata, sigma=None, sigma_weight_fit=True, iterations=100,  fitter_func=scipy.optimize.curve_fit, mc_type='bootstrap', distribution=numpy.random.randn):
    """Perform estimation of the distribution (confidence intervals) of fitted parameters using monte carlo resampling techniques.
        
        This can be done in 5 ways, configured by the mc_type parameter:
            'bootstrap': Perform a standard bootstrap
                Resampling is performed from a random selection of the given data (with replacement - the same data point can be picked twice).
                
                The data is assumed to be representative of the underlying distribution.
                
            'smooth_bootstrap': Perform a smooth bootstrap
                On top of the resampling as per a normal boostrap, some noise is added to the resampled points. The noise is scaled by the sigma provided (cannot be None).
                
                This attempts to fix the assumption of the standard bootstrap that the sampled data is representative of the underlying distribution, by smoothing it out. This can over-estimate width.
                
            'residual_bootstrap': 
                Resample by generating data from the fitted values, and randomly picked residuals (again with replacement)
            
            'parametric_bootstrap':
                Parametric bootstrap fits a model to the distribution, and uses this model
                to do resampling. This implementation fits the provided model to the data, and then treats the residuals as having a gaussian distribution, from which we resample.
                
            'mc_error_propagation':
                Resampling is performed by adding noise, scaled by the provided sigma.
    
        \param xdata Independant variable where the data is measured. (Array like)
        \param ydata Dependant variable data points (Array like)
        \param sigma Error in dependant variable - used for scaling noise, so for default normal distribution, assume this to be one standard deviation.
        \param iterations Number of resamples.
       
        \param sigma_weight_fit Pass the provided sigmas to the fitter_func for use in fitting. This currently only happens at the initial guess....
        \param mc_type Type of monte carlo estimation
        \param fitter_func Defaults to scipy's curve_fit
        \param fit_opt Options passed to the fitting function (e.g. {'f'=model_function, 'p0'=initial_guesses, 'bounds'=(min, max)}). 'f' is required!!!
            
            
    """

    # Check the parameters
    
    if mc_type not in ['bootstrap', 'smooth_bootstrap', 'residual_bootstrap', 'parametric_bootstrap', 'mc_error_propagation']:
        raise ValueError ('Invalid mc_type parameter')
    
    if (sigma is None) and (mc_type in ['smooth_bootstrap', 'mc_error_propagation']):
        raise ValueError ('Selected mctype requires sigma values, but none provided')
    
    
    if sigma_weight_fit == True:
        fit_sigma=sigma
    else:
        fit_sigma=None
    
    # Initial fit
    
    f = fit_opt['f']
    
    init_popt, _ = fitter_func(xdata=xdata, ydata=ydata, sigma=fit_sigma, **fit_opt)
    
    initial_model = f(xdata, *init_popt)
    initial_residuals = initial_model - ydata
    initial_residual_std = np.std(initial_residuals)
    
    # List of optimal parameters
    popts = [init_popt]
    
    # Sigma for each iteration - This doesn't really make sense for many of the types of resampling, so default to none.
    s=None
    
    # Do iterations
    for it in range(iterations-1):
        
        if mc_type is 'bootstrap':
            ind = numpy.random.randint(0, len(ydata), len(ydata))
            
            x=xdata[ind]
            y=ydata[ind]
            
            if sigma is not None and sigma_weight_fit == True:
                s=sigma[ind]
            
        elif mc_type is 'smooth_bootstrap':
            ind = numpy.random.randint(0, len(ydata), len(ydata))
            
            x=xdata[ind]
            y=ydata[ind] + sigma[ind] * distribution(len(ydata))
            
        elif mc_type is 'residual_bootstrap':
            ind = numpy.random.randint(0, len(ydata), len(ydata))
            
            x=xdata
            y=initial_model + initial_residuals[ind]
            
            if sigma is not None and sigma_weight_fit == True:
                s=sigma

        elif mc_type is 'parametric_bootstrap':
            x=xdata
            y=ydata + initial_residual_std * numpy.random.randn(len(ydata))
        
        elif mc_type is 'mc_error_propagation':
            x=xdata
            y=ydata + sigma * distribution(len(ydata))
        
        popt, _ = fitter_func(xdata=x, ydata=y, sigma=s, **fit_opt)
        popts.append(popt)
    
    
    # Do analysis
    
    popts = np.array(popts)
    
    mean = np.mean(popts, axis=0)
    low = np.percentile(popts, 2.5, axis=0)
    high = np.percentile(popts, 97.5, axis=0)
    std = np.std(popts, axis=0)
    
    return mean, low, high, std, popts

def convergence_plots(popts):
    
    std=[]
    mean=[]
    low=[]
    high=[]
    
    x=range(2,len(popts))
    
    for step in x:
        mean.append(np.mean(popts[:step, :], axis=0))
        low.append(np.percentile(popts[:step, :], 2.5, axis=0))
        high.append(np.percentile(popts[:step, :], 97.5, axis=0))
        std.append(np.std(popts[:step, :], axis=0))
        
    std = np.array(std)
    mean = np.array(mean)
    high = np.array(high)
    low = np.array(low)
    
    nParams = std.shape[1]
    for i in range(nParams):
        plt.subplot(nParams, 1, i+1)
        plt.fill_between(x, mean[:,i] - std[:,i], mean[:,i] + std[:,i], alpha=0.2)
        plt.plot(x, mean[:,i])
        plt.plot(x, low[:,i])
        plt.plot(x, high[:,i])
    
if __name__ == "__main__":
    # Run some tests

    f = lambda x, a1, a2, a3: a1*x**2 + a2*np.sin(x) + a3

    x = (np.random.rand(100)-0.5) * 10
    y = f(x, 0.2, 1, 3) + np.random.randn(len(x))*2
    s = 2 * np.ones(x.size)

    plt.plot(x,y, '.')

    mean, low, high, std, popt = monte_carlo_fit({'f':f, 'p0':[0.15, 0.9, 3.3]}, x, y, sigma=s, mc_type='bootstrap')


    xf = np.linspace(-5,5,100)

    for row in popt:
        plt.plot(xf, f(xf, *row), 'k', alpha=0.1)

    plt.plot(xf, f(xf, *mean))
    plt.plot(xf, f(xf, *high))
    plt.plot(xf, f(xf, *low))

    plt.figure()
    convergence_plots(popt)

    plt.show()
