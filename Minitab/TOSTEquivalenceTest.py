import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class TOSTEquivalenceTest:
    def __init__(self, test_data, reference_data, lower_bound, upper_bound, alpha=0.05, assume_equal_variances=False):
        self.test_data = pd.to_numeric(test_data, errors='coerce').dropna()
        self.reference_data = pd.to_numeric(reference_data, errors='coerce').dropna()
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.alpha = alpha
        self.assume_equal_variances = assume_equal_variances
        self._validate_data()

    def _validate_data(self):
        if len(self.test_data) == 0 or len(self.reference_data) == 0:
            raise ValueError("Test data or reference data has no valid entries.")

    def calculate_means_and_std(self):
        self.mean_test = np.mean(self.test_data)
        self.mean_ref = np.mean(self.reference_data)
        self.std_test = np.std(self.test_data, ddof=1)
        self.std_ref = np.std(self.reference_data, ddof=1)
        self.n_test = len(self.test_data)
        self.n_ref = len(self.reference_data)

    def calculate_difference(self):
        # Difference (D)
        self.mean_diff = self.mean_test - self.mean_ref

    def calculate_standard_error(self):
        # Standard error (SE)
        if self.assume_equal_variances:
            # Pooled standard deviation
            sp = np.sqrt(((self.n_test - 1) * self.std_test**2 + (self.n_ref - 1) * self.std_ref**2) / (self.n_test + self.n_ref - 2))
            self.se_diff = sp * np.sqrt(1 / self.n_test + 1 / self.n_ref)
        else:
            self.se_diff = np.sqrt((self.std_test**2 / self.n_test) + (self.std_ref**2 / self.n_ref))

    def calculate_degrees_of_freedom(self):
        # Degrees of freedom (DF)
        if self.assume_equal_variances:
            self.df = self.n_test + self.n_ref - 2
        else:
            numerator = ((self.std_test**2 / self.n_test) + (self.std_ref**2 / self.n_ref))**2
            denominator = ((self.std_test**2 / self.n_test)**2 / (self.n_test - 1)) + ((self.std_ref**2 / self.n_ref)**2 / (self.n_ref - 1))
            self.df = np.floor(numerator / denominator)

    def calculate_t_values(self):
        # Calculate T-values as per Minitab's method
        self.t_lower = (self.mean_diff - self.lower_bound) / self.se_diff  # Lower bound test
        self.t_upper = (self.mean_diff - self.upper_bound) / self.se_diff  # Upper bound test

    def calculate_p_values(self):
        # P-value for the lower bound: using the left tail
        self.p_lower = stats.t.cdf(self.t_lower, self.df)

        # P-value for the upper bound: using the right tail
        self.p_upper = 1 - stats.t.cdf(self.t_upper, self.df)

    def perform_test(self):
        self.calculate_means_and_std()
        self.calculate_difference()
        self.calculate_standard_error()
        self.calculate_degrees_of_freedom()
        self.calculate_t_values()
        self.calculate_p_values()

        # Print the results
        print(f"Test Mean: {round(self.mean_test, 3)}")
        print(f"Reference Mean: {round(self.mean_ref, 3)}")
        print(f"Mean Difference: {round(self.mean_diff, 3)}")
        print(f"Standard Error of the Difference: {round(self.se_diff, 3)}")
        print(f"Degrees of Freedom: {int(self.df)}")
        print(f"Lower Bound T-value: {round(self.t_lower, 3)}")
        print(f"Upper Bound T-value: {round(self.t_upper, 3)}")
        print(f"Lower Bound P-value: {self.p_lower}")
        print(f"Upper Bound P-value: {self.p_upper}")

        # Check if both p-values are less than alpha for equivalence (Minitab-like TOST)
        if self.p_lower < self.alpha and self.p_upper < self.alpha:
            print("Conclusion: The means are equivalent.")
        else:
            print("Conclusion: The means are not equivalent.")

    def generate_plots(self):
        # Plotting results to visualize the data
        ci_lower = self.mean_diff - stats.t.ppf(1 - self.alpha / 2, self.df) * self.se_diff
        ci_upper = self.mean_diff + stats.t.ppf(1 - self.alpha / 2, self.df) * self.se_diff

        # Create subplots
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))

        # 1. Equivalence Plot with Confidence Interval
        axs[0, 0].errorbar([0], [self.mean_diff], yerr=[[self.mean_diff - ci_lower], [ci_upper - self.mean_diff]], fmt='o', capsize=5, label='Mean Difference CI')
        axs[0, 0].axhline(self.lower_bound, color='red', linestyle='--', label=f'Lower Bound: {self.lower_bound}')
        axs[0, 0].axhline(self.upper_bound, color='blue', linestyle='--', label=f'Upper Bound: {self.upper_bound}')
        axs[0, 0].set_title('Equivalence Plot')
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        # 2. Histogram of Test and Reference Data
        axs[0, 1].hist(self.test_data, alpha=0.5, label='Test Data', color='blue', bins=7)
        axs[0, 1].hist(self.reference_data, alpha=0.5, label='Reference Data', color='green', bins=7)
        axs[0, 1].set_title('Histogram of Test and Reference Data')
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        # 3. Individual Value Plot for Test and Reference data
        axs[1, 0].scatter(np.ones(len(self.test_data)), self.test_data, label='Test Data', color='blue', alpha=0.7)
        axs[1, 0].scatter(np.ones(len(self.reference_data)) + 1, self.reference_data, label='Reference Data', color='green', alpha=0.7)
        axs[1, 0].axhline(self.mean_test, color='blue', linestyle='--', label=f'Test Mean: {self.mean_test:.2f}')
        axs[1, 0].axhline(self.mean_ref, color='green', linestyle='--', label=f'Ref Mean: {self.mean_ref:.2f}')
        axs[1, 0].set_xticks([1, 2])
        axs[1, 0].set_xticklabels(['Test Data', 'Reference Data'])
        axs[1, 0].set_title('Individual Value Plot')
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        # 4. Boxplot of Test and Reference Data
        axs[1, 1].boxplot([self.test_data, self.reference_data], labels=['Test Data', 'Reference Data'])
        axs[1, 1].set_title('Boxplot of Test and Reference Data')
        axs[1, 1].grid(True)

        # Adjust the layout
        plt.tight_layout()
        plt.show()
