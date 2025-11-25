from scipy.stats import mannwhitneyu
import numpy as np
from typing import Literal

def OPO_UTest(
    exp_samps: list | np.ndarray, 
    test_samps: list | np.ndarray, 
    threshold: float=0.05
) -> Literal["pass", "fail"]:
    """
    Perform a Mann–Whitney U test to compare two independent samples.
    
    The Mann–Whitney U test is a nonparametric statistical test used to assess 
    whether two independent samples come from the same distribution, i.e., it 
    tests the null hypothesis that the distributions of both samples are equal.

    Parameters
    ----------
    exp_samps : list or array-like
        Samples generated according to the expected probability distribution
        of the quantum program under test.
    test_samps : list or array-like
        Actual measurement results obtained from the tested quantum program.
    threshold : float, optional, default=0.05
        Significance level (p-value) for rejecting the null hypothesis. 
        If the p-value from the test is greater than this threshold, the 
        null hypothesis is not rejected.

    Returns
    -------
    str
        'pass' if the test does not reject the null hypothesis (p-value > threshold),
        'fail' if the test rejects the null hypothesis (p-value <= threshold).
 
    """
    
    # Ensure the inputs are in list format for the statistical test
    exp_samps = list(exp_samps)
    test_samps = list(test_samps)

    # Perform the Mann–Whitney U test
    # Returns U statistic (ignored here) and the two-sided p-value
    _, p_value = mannwhitneyu(exp_samps, test_samps)

    # Compare p-value against the significance threshold
    if p_value > threshold:
        # If p-value is greater than threshold, distributions are not significantly different
        return 'pass'
    else:
        # If p-value is less than or equal to threshold, distributions differ significantly
        return 'fail'



if __name__ == "__main__":
    """
    Unit testing for OPO_UTest.
    Run:
        python mycode/utils/test_oracle.py
    """

    # ----------------------------
    # Test inputs
    # ----------------------------

    def test_input_pass_case():
        """
        Generate two similar distributions that should 'pass' the test.
        """
        np.random.seed(42)
        exp_samps = np.random.normal(loc=0, scale=1, size=100)
        test_samps = np.random.normal(loc=0, scale=1, size=100)
        return exp_samps, test_samps

    def test_input_fail_case():
        """
        Generate two different distributions that should 'fail' the test.
        """
        np.random.seed(42)
        exp_samps = np.random.normal(loc=0, scale=1, size=100)
        test_samps = np.random.normal(loc=1, scale=1, size=100)
        return exp_samps, test_samps

    # ----------------------------
    # Unit tests
    # ----------------------------

    def unit_test_pass_case(input_tuple, threshold=0.05):
        exp_samps, test_samps = input_tuple
        result = OPO_UTest(exp_samps, test_samps, threshold)
        assert result == 'pass', f"Expected 'pass', got {result}"

    def unit_test_fail_case(input_tuple, threshold=0.05):
        exp_samps, test_samps = input_tuple
        result = OPO_UTest(exp_samps, test_samps, threshold)
        assert result == 'fail', f"Expected 'fail', got {result}"
 

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {"input": test_input_pass_case, "function": unit_test_pass_case},
        "1": {"input": test_input_fail_case, "function": unit_test_fail_case}
    }

    for test_id, execution_dict in executed_test.items():
        print(f"\nExecuting test_id={test_id}:")
        test_input_val = execution_dict["input"]()
        try:
            execution_dict["function"](test_input_val)
            if "manual" in execution_dict["function"].__name__:
                print("need manual check")
            else:
                print("pass")
        except AssertionError as e:
            print("fail")
            raise