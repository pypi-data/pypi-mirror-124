import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100
import matplotlib.pyplot as plt
from tableone import TableOne, load_dataset
import random
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from collections import Iterable
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
pd.options.mode.chained_assignment = None  # default='warn'


class are_never_implemented:
        
    def are_rule_free_df(self, df, ttt, outcome, reco, ps, ro=1):
        """Compute ARE from a dataset where the rule was never implemented.
        Input:
        - df: pandas dataframe
        - ttt: String for the column corresponding to the Bernouilli variable A for the treatment delivered
        - outcome: String for the column corresponding to the binary or continuous variable Y for the treatment outcome observed
        - reco: String for the column corresponding to the Bernouilli variable r(X) for the treatment recommended
        - ps: String for the column corresponding to the Propensity Scores
        - ro: Numpy array of E(S|X=x) with S Bernouilli variable for use of the rule (stochastic component)

        Returns: (are, S_fraction) tuple of floats
        - are: float
        - S_fraction: float fraction of patients with S=1 (rule used)
        """

        dat = df.copy()
        dat['S'] = np.random.binomial(n=1, p=ro)
        dat['prS'] = ro

        are = dat.apply(lambda row :
                       row[outcome] * (row[ttt] * row[reco] * row['prS'] / row[ps] + (1 - row[reco]) * row['prS'] * (1 - row[reco]) / (1 - row[ps]) -  row['S']) 
                       , axis = 1).mean()

        S_fraction = dat['prS'].mean()

        return are, S_fraction


    def ro_cb(self, df, reco, ps, alpha=.5, **kwargs): #, ros_array=None,
        """ Computes cognitive bias ros (i.e., E(S|X=x) ) from Xs and recomendations and PSs 
        Inputs:
        - df: pandas dataframe
        - reco: String for the column corresponding to the Bernouilli variable r(X) for the treatment recommended
        - ps: String for the column corresponding to the Propensity Scores
        - ros_array: Needs not be provided here
        - alpha: float cognitive bias parameter between zero and one (higher values for higher cognitive bias)

        Returns: ros Numpy array of E(S|X=x)
        """

        return (1 - np.abs(df[reco] - df[ps]) ) ** (.5 * np.log( (alpha+1)/(1-alpha) ) )

    def ro_unif(self, df, alpha=.5, **kwargs): #reco=None, ps=None, ros_array=None, 
        """ Returns uniform implementation ros (i.e., E(S|X=x) ) 
        Inputs:
        - df: pandas dataframe
        - reco: Needs not be provided here
        - ps: Needs not be provided here
        - ros_array: Needs not be provided here
        - alpha: float uniform parameter between zero and one (higher values for higher implementation)

        Returns: ros Numpy array of E(S|X=x) (independant of X here)
        """

        return np.array(len(df)*[alpha])

    def ro_pass_array(self, ros_array, **kwargs):# df=None, reco=None, ps=None, alpha=None):
        """ Returns an array identical to the input. This function is fit to be passed in are_rule_free_boot function with no trouble.
        Inputs:
        - ros_array: Numpy array of ros in the interval [0-1]
        - df: Needs not be provided here
        - reco: Needs not be provided here
        - ps: Needs not be provided here
        - alpha: Needs not be provided here

        Returns: ros Numpy array identical to the input
        """
        return ros_array

    def get_boot_indexes(self, df, n_boot):
        """ For futher bootstrap run, this function returns a list of indexes that sampled with replacement from the indexes of a df
        Inputs:
        - df: pandas dataframe
        - n_boot: int number of sampling with replacement

        Returns: resamples: list of int 
        """
        resamples = []
        for _ in range(n_boot):
            resamples.append([random.randint(0,len(df)-1) for _ in range(len(df))])
        return resamples

    def are_rule_free_boot(self, df, ttt='cabg', outcome='Y', reco='rule_reco', ps_var=['age', 'crcl_log', 'copd', 'lmcad', 'both'], imp_function=None, ros_array=None, alpha=.5, n_boot=10):
        """Get bootstrap estimates for the estimator are_rule_free under a defined implementation scenario
        Input:
        - df: pandas dataframe
        - ttt: String for the column corresponding to the Bernouilli variable A for the treatment delivered
        - outcome: String for the column corresponding to the binary or continuous variable Y for the treatment outcome observed
        - reco: String for the column corresponding to the Bernouilli variable r(X) for the treatment recommended
        - ps_var: List of strings of columns names for propensity score fitting (i.e., covariates)
        - imp_function: function ro_cb or ro_unif the implementation scenario or ro_pass_array if an array of ros is provided
        - ros_array: numpy array of shape (len(df), ) of ros E(S|X=x) in the interval [0-1] if ro_pass_array is used such that any scenario can be implemented
        - alpha: the implementation parameter for the choosen scenario
        - n_boot: int number of bootstrap resamples

        Returns: 
        - boot_estimates: list of float corresponding to the n_boot bootstrat estimations
        - S_fractions list of fraction of patients with S=1
        """
        if imp_function==None:
            imp_function=self.ro_cb

        boot_indexes = self.get_boot_indexes(df, n_boot)
        boot_estimates = []
        ps = 'ps'
        for i in tqdm(range(n_boot)):
            temp_dat = df.iloc[boot_indexes[i]]

            if ros_array is not None:
                ros_array_temp = ros_array[boot_indexes[i]]
            else:
                ros_array_temp = None

            clf = LogisticRegression(random_state=0, max_iter=500).fit(temp_dat[ps_var], temp_dat[ttt])
            temp_dat[ps] = clf.predict_proba(temp_dat[ps_var])[:,1]

            estimate, S_fraction = self.are_rule_free_df(df=temp_dat, ttt=ttt, outcome=outcome, reco=reco, ps=ps, ro=imp_function(ros_array=ros_array_temp, df=temp_dat, reco=reco, ps=ps, alpha=alpha) )
            boot_estimates.append(estimate)
        return boot_estimates, S_fraction
    
    def are_rule_free_boot_per_alpha(self, df, ttt='cabg', outcome='Y', reco='rule_reco', ps_var=['age', 'crcl_log', 'copd', 'lmcad', 'both'], imp_function=None, ros_array=None, n_boot=10, n_alphas=5):
        """Get bootstrap estimates for the estimator are_rule_free under a defined implementation scenario, under a range of mplementation parameter alpha
        Input:
        - df: pandas dataframe
        - ttt: String for the column corresponding to the Bernouilli variable A for the treatment delivered
        - outcome: String for the column corresponding to the binary or continuous variable Y for the treatment outcome observed
        - reco: String for the column corresponding to the Bernouilli variable r(X) for the treatment recommended
        - ps_var: List of strings of columns names for propensity score fitting (i.e., covariates)
        - imp_function: function ro_cb or ro_unif the implementation scenario or ro_pass_array if an array of ros is provided
        - ros_array: numpy array of shape (len(df), ) of ros E(S|X=x) in the interval [0-1] if ro_pass_array is used such that any scenario can be implemented
        - alpha: the implementation parameter for the choosen scenario
        - n_boot: int number of bootstrap resamples
        - n_alphas: int number of implementation parameters to explore for the choosen scenario on a linear scale between zero and 0.9999999999 (singularity at 1)

        Returns: (alphas, boot_estimates_alphas) tuple
        - alphas: numpy array implementation parameters to explored for the choosen scenario (on a linear scale between zero and 0.9999999999 (singularity at 1))
        - boot_estimates_alphas list of list of floats corresponding to the n_boot bootstrat estimations for the n_alphas implementation parameters to explored
        - S_fractions list of fraction of patients with S=1
        """
        
        if imp_function==None:
            imp_function=self.ro_cb
            
        boot_estimates_alphas = []
        S_fractions = []
        alphas = np.linspace(0, 1-10**-10, n_alphas)
        for alpha in alphas:
            are, S_fraction = self.are_rule_free_boot(df=df, ttt=ttt, outcome=outcome, reco=reco, ps_var=ps_var, imp_function=imp_function, ros_array=ros_array, n_boot=n_boot, alpha=alpha)
            boot_estimates_alphas.append(are)
            S_fractions.append(S_fraction)
        return alphas, boot_estimates_alphas, S_fractions

    def boot_ci(self, boot_estimates, risk_a):
        """outputs a list of bootstrap CI from a list of lists of bootstrap estimates"""
        quantiles = np.array([np.nanquantile(boot_estimates[i],[(1-risk_a)/2, (1+risk_a)/2]) for i in range(len(boot_estimates))])
        return quantiles
    
    def confint_are_rule_free_per_alpha(self, df, ttt='cabg', outcome='Y', reco='rule_reco', ps_var=['age', 'crcl_log', 'copd', 'lmcad', 'both'], imp_function=None, ros_array=None, n_boot=10, n_alphas=5, risk_a=.95):
        """Get estimation confidence intervals and fraction of patients with S=1 under a defined implementation scenario for a range of implementation parameter alpha
        Input:
        - df: pandas dataframe
        - ttt: String for the column corresponding to the Bernouilli variable A for the treatment delivered
        - outcome: String for the column corresponding to the binary or continuous variable Y for the treatment outcome observed
        - reco: String for the column corresponding to the Bernouilli variable r(X) for the treatment recommended
        - ps_var: List of strings of columns names for propensity score fitting (i.e., covariates)
        - imp_function: function ro_cb or ro_unif the implementation scenario or ro_pass_array if an array of ros is provided
        - ros_array: numpy array of shape (len(df), ) of ros E(S|X=x) in the interval [0-1] if ro_pass_array is used such that any scenario can be implemented
        - alpha: the implementation parameter for the choosen scenario
        - n_boot: int number of bootstrap resamples
        - n_alphas: int number of implementation parameters to explore for the choosen scenario on a linear scale between zero and 0.9999999999 (singularity at 1)
        - risk_a: float Type I error in the interval [0-1]

        Returns: (alphas, fraction, estimates, conf_ints) tuple
        - alphas: numpy array implementation parameters to explored for the choosen scenario (on a linear scale between zero and 0.9999999999 (singularity at 1))
        - fraction: list of fraction of patients with S=1 corresponding to the n_alphas implementation parameters to explored
        - estimates list of floats estimations corresponding to the n_alphas implementation parameters to explored
        - conf_ints list of list of confidence intervals with type I error risk_a
        """
        
        if imp_function==None:
            imp_function=self.ro_cb
        
        alphas, boot_estimates_alphas, S_fractions = self.are_rule_free_boot_per_alpha(df=df, ttt=ttt, outcome=outcome, reco=reco, ps_var=ps_var, imp_function=imp_function, ros_array=ros_array, n_boot=n_boot, n_alphas=n_alphas)

        fraction = [np.mean(S_fraction) for S_fraction in S_fractions]
        estimates = [np.mean(boot_estimates) for boot_estimates in boot_estimates_alphas]
        conf_ints = self.boot_ci(boot_estimates_alphas, risk_a)


        if len(alphas) == 1:
            plt.hist(boot_estimates_alphas[0], density=True)
        else:
            fig, axs = plt.subplots(len(boot_estimates_alphas), 1, figsize=(5,5*len(alphas)))
            for it, val in enumerate(boot_estimates_alphas):
                axs[it].set_title(r'$\alpha={}$'.format(np.round(alphas[it],2)), fontsize=20)
                axs[it].hist(val, density=True);

        return imp_function, alphas, fraction, estimates, conf_ints
    
    def plot_are_rule_free(self, scenario, alphas, fraction, estimates, conf_ints):
            if scenario.__name__ == 'ro_cb':
                scenario_str = 'Cognitive Biais'
                abv = 'cb'
            elif scenario.__name__ == 'ro_unif':
                scenario_str = 'Uniform Implementation'
                abv = 'unif'
            elif scenario.__name__ == 'ro_pass_array':
                scenario_str = 'User-defined Implementation'
                abv = ''
            elif scenario.__name__ == 'syntax_iHR_ci':
                scenario_str = 'Individual HR Confidence Interval Implementation'
                abv = 'cl'
            else:
                scenario_str = 'Other Implementation'
                abv = ''

            print('Scenario')
            print(scenario_str)
            print('\nAlphas: implementation parameters explored')
            print('{}'.format(np.round(alphas,4)))
            print('\nProportion of patients in whom the rule is used in the given scenario')
            print('{}'.format(np.round(fraction,4)))
            print('\nEstimates of the ARE for the given parameter of the given scenario')
            print('{}'.format(np.round(estimates,4)))
            print('\nConrresponding confidence intervals')
            print('{}'.format(np.round(conf_ints,4)))

            lb = [bound[0] for bound in conf_ints]
            ub = [bound[1] for bound in conf_ints]

            fig, axs = plt.subplots(1, 2, figsize=(10,5))

            fig.suptitle(scenario_str + " Scenario", fontsize=15)
            axs[0].plot([0,1],[0, 0], color= "black", alpha=1, linewidth=.5, linestyle='solid')
            axs[0].plot(alphas, estimates, 'D', color= "#df8f44ff")
            axs[0].fill_between(alphas, lb, ub, color="#df8f44ff", alpha=.1)

            axs[0].set_xlabel(scenario_str + r' Parameter $\alpha$', fontsize=10)

            ylab = r'$\widehat{\Delta}^{stoch}_{\rho_{' + abv + '}}(r)$'

            axs[0].set_ylabel(ylab, fontsize=20)

            axs[0].set_xlim([-.02,1.02])
            axs[1].set_xlim([-.02,1.02])

            axs[1].plot([0,1],[0, 0], color= "black", alpha=1, linewidth=.5, linestyle='solid')
            axs[1].plot(fraction, estimates, 'D', color= "#00a1d5ff")
            axs[1].fill_between(fraction, lb, ub, color="#00a1d5ff", alpha=.1);

            axs[1].set_xlabel('Proportion Of Patients Implementing The Rule', fontsize=10);

            return fig, axs
    
    def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item
                
    def confint_are_rule_free_per_type_I_error(self, df,
                ttt,
                outcome,
                reco,
                ps_var,
                significance_function,
                n_boot=2000, n_type_I_errors=1, risk_a=.95):
    
        scenario = []
        alphas = []
        fraction = []
        estimates = []
        conf_ints = []

        for it, n_type_I_error in enumerate(np.linspace(0, 1, n_type_I_errors)):
            significance_array = significance_function(df, alpha=n_type_I_error)['significance']*1
            scenario_temp, alphas_temp, fraction_temp, estimates_temp, conf_ints_temp = confint_are_rule_free_per_alpha(df=df,
                                        ttt=ttt,
                                        outcome=outcome,
                                        reco=reco,
                                        ps_var=ps_var,
                                        imp_function=ro_pass_array, ros_array = significance_array,
                                        n_boot=n_boot, n_alphas=1, risk_a=risk_a)

            alphas.append(n_type_I_error)
            fraction.append(fraction_temp)
            estimates.append(estimates_temp)
            conf_ints.append(list(flatten(conf_ints_temp)))

        scenario = significance_function

        fraction = list(self.flatten(fraction))
        estimates = list(self.flatten(estimates))
        conf_ints = np.array(conf_ints)

        return scenario, alphas, fraction, estimates, conf_ints