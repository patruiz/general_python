import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

filepath = r"C:\Users\pr19556\OneDrive - Applied Medical\Desktop\fuck.csv"

df = pd.read_csv(filepath)
df_clean = df.replace([np.inf, -np.inf], np.nan).dropna()

# Create the figure and histograms
plt.figure(figsize=(10, 6))

# Plot the histogram for 'High Cav'
count, bins, ignored = plt.hist(df_clean['High Cav'], bins=10, alpha=0.5, label='High Cav', color='blue', edgecolor='black', density=True)

# Fit a normal distribution to the 'High Cav' data
mu_high, std_high = norm.fit(df_clean['High Cav'])
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p_high = norm.pdf(x, mu_high, std_high)
plt.plot(x, p_high, 'blue', linewidth=2, label=f'High Cav Normal Curve ($\mu={mu_high:.2f}, \sigma={std_high:.2f}$)')

# Plot the histogram for 'Single Cav'
count, bins, ignored = plt.hist(df['Single Cav'], bins=10, alpha=0.5, label='Single Cav', color='green', edgecolor='black', density=True)

# Fit a normal distribution to the 'Single Cav' data
mu_single, std_single = norm.fit(df_clean['Single Cav'])
p_single = norm.pdf(x, mu_single, std_single)
plt.plot(x, p_single, 'green', linewidth=2, label=f'Single Cav Normal Curve ($\mu={mu_single:.2f}, \sigma={std_single:.2f}$)')

# Add labels and title
plt.xlabel('Values')
plt.ylabel('Density')
plt.title('Jaw Force Normal Distribution - High Cav vs Single Cav')

# Add legend
plt.legend(loc='upper right')

# Show the plot
plt.show()