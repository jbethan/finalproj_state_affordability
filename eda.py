# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# %%
data = pd.read_csv('https://raw.githubusercontent.com/jbethan/finalproj_state_affordability/main/2023_state_dataset.csv', index_col=None)
data = data.drop(data.columns[0], axis=1)
data.head()

# %%
# GROUP 1 PLOT INCOME METRICS

# Graphs
# Median Data Job Salaries to Median Salary in State
# Creating a plot
fig1 = px.bar(data, x='State', 
             y=['Data Analyst Average Salary', 'Data Scientist Average Salary'], 
             barmode='group',
             labels={'value': 'Average Salary', 'variable': '', 'Data Analyst Average Salary': 'Data Analysts', 'Data Scientist Average Salary': 'Data Scientists' },
             title='Average Salaries for Data Jobs compared to All Industry Average Salary by State')

# Show the plot
fig1.show()

# %%
# 25% Percentile Data Salary to Median Salary in State

# GROUP 2 PLOT RENT METRICS

# Graphs
# Rent to Median Salary in State

# Rent 25% Percentile Data Job Salary

# GROUP 3 PLOT HOME OWNER METRICS

# Graphs
# Down Payment Percentage of Annual Income

# Monthly House Payment to Median Income

# Median Income by Field needed to Afford Monthly Housing Payment

# GROUP 4 PLOT TAX BURDEN METRICS

# Graphs
# Paycheck-to-Paycheck Tax Burden (Income v Sales)

# Home Ownership Tax Burden (Property)

# 20-30-50 Rule



data["Monthly Difference"] = data['Monthly Tax Adjusted Income']- data['Monthly Housing Payments']
data.head()

# %%
data.plot(x='State', y=['Monthly Housing Payments','Monthly Tax Adjusted Income'], kind = 'line', color = ['Blue', 'green'])
plt.xlabel ('State')
plt.ylabel ('Cost')
plt.title ('Monthly Adjusted Income v. Housing Payments')
plt.show ()
# %%
# Save figure
plt.savefig("income_housing.png", dpi = 300)
# %%
