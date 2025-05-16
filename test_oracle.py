from scipy.stats import mannwhitneyu

def OPO_UTest(exp_samps, test_samps, threshold=0.05):
    
    '''
        This provides a test result by a Mann–Whitney U test, a kind of widely applied
        nonparametric statistical test of the null hypothesis

        Input variables:
            + expSamps:  [list / array]   
                         the samples following the expected probability distribution of the
                         tested quantum program
            + testSamps: [list / array]
                         the actual measurement results of the tested quantum program
            + threshold: [float]
                         the p-value that determines whether to reject the null hypothesis,
                         where the default value is 0.05
        
        Output variable: the test result ('pass' or 'fail')
    '''
    
    exp_samps = list(exp_samps)
    test_samps = list(test_samps)

    _, p_value = mannwhitneyu(exp_samps, test_samps)
    if p_value > threshold:
        return 'pass'
    else:
        return 'fail'
