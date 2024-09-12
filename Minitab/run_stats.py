import os
import pandas as pd 
from TOSTEquivalenceTest import TOSTEquivalenceTest

os.system('cls')

df = pd.read_csv(r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Golden Jaw Force Fixture\Testing\2024\MD AFG\EQ_Prod\EQ_Data.csv")
ref_data = df['Ref D_02']
test_data = df['Test D_02']

print(ref_data, flush = True)
print(test_data, flush = True)
# test_data = pd.Series([5.6, 5.8, 5.7, 5.9, 6.0])
# reference_data = pd.Series([5.5, 5.6, 5.7, 5.8, 5.9])

# With equal variances assumed
# tost_test_equal_var = TOSTEquivalenceTest(test_data, reference_data, lower_bound=-0.1, upper_bound=0.1, assume_equal_variances=True)
# tost_test_equal_var.perform_test()
# tost_test_equal_var.generate_plots()

# Without equal variances assumed (default)
tost_test_unequal_var = TOSTEquivalenceTest(test_data, ref_data, lower_bound = -0.26, upper_bound = 0.26, assume_equal_variances = False)
tost_test_unequal_var.perform_test()
# tost_test_unequal_var.generate_plots()

swag = input('swag it up: ')
os.system('pause')