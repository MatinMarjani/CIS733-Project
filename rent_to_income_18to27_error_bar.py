import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = 'Inflation_Adjusted_Data.csv'
df = pd.read_csv(file_path)
generation_column = 'GENERATION'
ownership_column = 'OWNERSHP_2'
housing_value_column = 'HOUSING_VALUE_adjusted'  # Monthly rent
income_column = 'INCTOT_adjusted'  # Annual income
age_column = 'AGE'
df = df[(df[age_column] >= 18) & (df[age_column] <= 27)]
renters = df[(df[ownership_column] == 0) & (df[income_column] > 1000)]
renters['monthly_income'] = renters[income_column] / 12
renters['rent_to_income_ratio'] = (renters[housing_value_column] / renters['monthly_income']) * 100
renters = renters[renters['rent_to_income_ratio'] <= 100]

# Group by generation and calculate the average Rent-to-Income Ratio and standard error
rent_to_income_stats = renters.groupby(generation_column)['rent_to_income_ratio'].agg(['mean', 'sem']).reindex(
    ['Baby Boomers', 'Generation X', 'Millennials', 'Generation Z'], fill_value=np.nan
)

average_ratios = rent_to_income_stats['mean'].tolist()
error_bars = rent_to_income_stats['sem'].tolist()

plt.figure(figsize=(10, 6))
bars = plt.bar(rent_to_income_stats.index, average_ratios, yerr=error_bars, capsize=5, 
               color='skyblue', alpha=0.8, error_kw=dict(ecolor='black', elinewidth=1.5))
for i, (ratio, error) in enumerate(zip(average_ratios, error_bars)):
    if not np.isnan(ratio):
        plt.text(i, ratio + error + 1, f"{ratio:.1f}%", ha='center', fontsize=10)
plt.title('Average Rent-to-Income Ratio by Generation (Ages 18–27, Renters Only)', fontsize=16)
plt.xlabel('Generation', fontsize=14)
plt.ylabel('Average Rent-to-Income Ratio (%)', fontsize=14)
y_max = max(filter(lambda x: not np.isnan(x), average_ratios)) + max(filter(lambda x: not np.isnan(x), error_bars)) + 10
plt.ylim(0, y_max)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()