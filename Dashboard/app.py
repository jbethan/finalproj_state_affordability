# %%
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.title('Recently Graduated Data Professional Seeks Affordable Life')

# %%
data = pd.read_csv('https://raw.githubusercontent.com/jbethan/finalproj_state_affordability/main/2023_state_dataset.csv', index_col=None)
data = data.drop(data.columns[0], axis=1)
data.head()

# %%
data = data.rename(columns={"Annual Average Wage" : "All Industry Average Salary"})
data['Total Tax Burden'] = data['Total Tax Burden']/100
data['Property Tax Burden'] = data['Property Tax Burden']/100 
data['Income Tax Burden'] = data['Income Tax Burden']/100
data['Sales Tax Burden'] = data['Sales Tax Burden']/100

# %%
# GROUP 1 PLOT INCOME METRICS

# Graphs
# Salary Comparison by State for Data Analysts

fig1 = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                    shared_yaxes=True, horizontal_spacing=0)

fig1.append_trace(go.Bar(x=data['All Industry Average Salary'],
                     y=data['State'], 
                     text=data["All Industry Average Salary"], #.map('${:,.0f}'.format), 
                     textposition='inside',
                     textfont=dict(color="White"),
                     orientation='h', 
                     width=0.8, 
                     showlegend=False, 
                     marker_color='#363a5b'), 
                     1, 1) # 1,1 represents row 1 column 1 in the plot grid

fig1.append_trace(go.Bar(x=data['Data Analyst Average Salary'],
                     y=data['State'], 
                     text=data["Data Analyst Average Salary"], #.map('${:,.0f}'.format),
                     textposition='inside',
                     textfont=dict(color="White"),
                     orientation='h', 
                     width=0.8, 
                     showlegend=False, 
                     marker_color='#5c7693'), 
                     1, 2) # 1,2 represents row 1 column 2 in the plot grid

fig1.update_xaxes(showticklabels=False,title_text="All Industry Average Salary", row=1, col=1, autorange='reversed')
fig1.update_xaxes(showticklabels=False,title_text="Data Analyst Average Salary", row=1, col=2)
fig1.update_yaxes(autorange="reversed")

fig1.update_layout(title_text="Salary Comparison by State for Data Analysts", 
                  width=800, 
                  height=1200,
                  plot_bgcolor="#F2EBDF")
st.plotly_chart(fig1)

# %%
# Salary Comparison by State for Data Scientists

fig2 = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                    shared_yaxes=True, horizontal_spacing=0)

fig2.append_trace(go.Bar(x=data['All Industry Average Salary'],
                     y=data['State'], 
                     text=data["All Industry Average Salary"], #.map('${:,.0f}'.format), 
                     textposition='inside',
                     textfont=dict(color="White"),
                     orientation='h', 
                     width=0.8, 
                     showlegend=False, 
                     marker_color='#363a5b'), 
                     1, 1)

fig2.append_trace(go.Bar(x=data['Data Scientist Average Salary'],
                     y=data['State'], 
                     text=data["Data Scientist Average Salary"], #.map('${:,.0f}'.format),
                     textposition='inside',
                     textfont=dict(color="White"),
                     orientation='h', 
                     width=0.8, 
                     showlegend=False, 
                     marker_color='#5d8b7c'), 
                     1, 2)

fig2.update_xaxes(showticklabels=False,title_text="All Industry Average Salary", row=1, col=1, autorange='reversed')
fig2.update_xaxes(showticklabels=False,title_text="Data Scientist Average Salary", row=1, col=2)
fig2.update_yaxes(autorange="reversed")

fig2.update_layout(title_text="Salary Comparison by State for Data Scientists", 
                  width=800, 
                  height=1200,
                  plot_bgcolor="#F2EBDF")
fig2.show()

# %%
salary_type_data = pd.melt(data, id_vars=['State'], value_vars=['All Industry Average Salary','Data Analyst Average Salary', 'Data Scientist Average Salary'], 
                         var_name="Salary Group", value_name='Average Salary')
salary_type_data['Salary Group'] = salary_type_data['Salary Group'].str.replace('Average Salary', '')
salary_type_data.head()

# %%
# Average Salary by Job Type
fig3 = px.violin(salary_type_data, 
                 y="Average Salary", 
                 x="Salary Group",
                 color = "Salary Group",
                 color_discrete_sequence= ["#5d8b7c", "#8fb5c9", "#91c0be"],
                 points="all",
                 hover_name = salary_type_data['State'],
                 title = 'Average Salary Distribution by Job Type Across All States')

fig3.update_layout(width=1200, 
                   plot_bgcolor="#F2EBDF")
fig3.show()

#
# %%
# Stacked Salary Comparison
#fig1 = px.scatter(data, x='State', 
#             y=['All Industry Average Salary','Data Analyst Average Salary', 'Data Scientist Average Salary'], 
#             #barmode='stack',
#             size = 'value',
#             labels={'value': 'Average Salary', 'variable': '' },
#             title='Average Salaries for Data Jobs compared to All Industry Average Salary by State')

# Show the plot
#fig1.show()

# %%
#fig1.write_html('Income_Comp.html', full_html=False, include_plotlyjs='cdn')

# %%
# Job Availability to Percentage about Average Income (Scatterplot)
data['Data Analyst Salary Ratio'] = data['Data Analyst Average Salary']/data['All Industry Average Salary'] - 1
data['Data Scientist Salary Ratio'] = data['Data Scientist Average Salary']/data['All Industry Average Salary'] - 1
data.head()

# %%
ratio_data = pd.melt(data, id_vars=['State'], value_vars= ['Data Analyst Salary Ratio','Data Scientist Salary Ratio'],
                    var_name="Job Group", value_name='Job Salary Ratio to Average Salary')
ratio_data['Job Group'] = ratio_data['Job Group'].str.replace('Salary Ratio', '')

job_data = pd.melt(data, id_vars=['State'], value_vars=['Data Analyst Job Count as of 09/14/23','Data Scientist Job Count as of 09/14/23'], 
                         var_name="Job Group", value_name='Job Count as of 09/14/23')
job_data['Job Group'] = job_data['Job Group'].str.replace('Job Count as of 09/14/23', '')

# %%
job_data = job_data.merge(ratio_data, how = "left", on=['State', 'Job Group'])
job_data.head()

# %%
ab_data = pd.read_csv('state_abbr.csv')
job_data = job_data.merge(ab_data, how = "left", on=['State'])
job_data.head()

# %%
fig4 = px.scatter(job_data, x='Job Count as of 09/14/23', 
                  y='Job Salary Ratio to Average Salary', 
                  color = 'Job Group',
                  color_discrete_sequence= ["#4c5d7d", "#74b5ac"],
                  hover_name = job_data['State'],
                  title='Job Count v. Job Salary Ratio to State Average Salary')

fig4.add_hrect(y0=-0.2, y1=0, line_width=0, 
               fillcolor="red", opacity=0.1, 
               annotation = dict(text="Average Job Salary is Below State Average"), 
               annotation_position = "bottom right")

fig4.update_layout(width=800, 
                   plot_bgcolor="#F2EBDF")
# Show the plot
fig4.show()

# ON DASH ADD SLIDER

# %%
# GROUP 2 PLOT RENT METRICS
# Rent v. Apartment Size
data['Cost Per Sq Ft $'] = data['Average Rent']/data['Average Apartment Size']
#data['Cost Per Sq Ft $'] = data['Cost Per Sq Ft $'].map('${:,.02f}'.format)
ab_data = pd.read_csv('state_abbr.csv')
data = data.merge(ab_data, how = "left", on=['State'])
data.head()

# %%
fig5 = px.choropleth(data, 
                    locations='Abbr', 
                    color='Cost Per Sq Ft $',
                    locationmode='USA-states',
                    title='Average Rent v. Apartment Size by State',
                    scope='usa',
                    color_continuous_scale=px.colors.sequential.deep,            
                    hover_name = 'State',
                    hover_data = ['Average Rent','Average Apartment Size'])

#fig5.update_layout(width=1200, 
#                   plot_bgcolor="#F2EBDF")
fig5.show()

# %%
# Rent to Median Salary in State
fig6 = go.Figure()

fig6.add_trace(go.Scatter(
    x=data['Average Rent'],
    y=data['State'],
    marker=dict(color="#363a5b", size=12),
    mode="markers",
    name="Average Monthly Rent"
))

fig6.add_trace(go.Scatter(
    x=data['Data Analyst Monthly Gross Income'],
    y=data['State'],
    marker=dict(color="#679589", size=12),
    mode="markers",
    name="Data Analyst Monthly Gross Income",
))

fig6.add_trace(go.Scatter(
    x=data['Data Scientist Monthly Gross Income'],
    y=data['State'],
    marker=dict(color="#65829e", size=12),
    mode="markers",
    name="Data Scientist Monthly Gross Income",
))

fig6.add_trace(go.Bar(
    x=(data['Average Rent']*3), 
    y=data['State'], 
    orientation = 'h',
    marker=dict(
        color='#363a5b',
        line=dict(color='#363a5b', width=3),
        opacity=0.3),
    name="30% Housing to Income Threshold"
))

fig6.update_layout(title="Average Rent v. Income",
                  xaxis_title="Monthly Amount",
                  yaxis_title="State",
                  height=1200,
                  plot_bgcolor="#F2EBDF"
                  )
fig6.update_yaxes(autorange="reversed")

fig6.show()

# %%
# GROUP 3 PLOT HOME OWNER METRICS
# Down Payment Percentage of Annual Income (Percentage bar chart)

# %%
# Monthly House Payment to Median Income
# Color Heat Index
fig7 = px.scatter(data, x='All Industry Average Salary', 
             y='Monthly House Payment', 
             size = 'Monthly House Payment',
             color = data['Median House Price'],
             color_continuous_scale=px.colors.sequential.Aggrnyl,
             hover_data = ['State'],
             labels={'value': 'Monthly House Payment', 'All Industry Average Salary': 'Average Salary by State (All Industries)' },
             title='Average Salary v. Monthly House Payment')
# Show the plot
fig7.update_layout(width=800, 
                   plot_bgcolor="#F2EBDF")
fig7.show()

# %%
# Down Payment v Salary
fig8 = go.Figure()
fig8.add_trace(go.Bar(
    x=data['State'], 
    y=data['Down Payment']/data['All Industry Average Salary']*100,
    text=data['Down Payment'], #.map('${:,.0f}'.format), 
    textposition='outside',
    textfont=dict(color="White"),
    marker_color="#363a5b",
    width=0.8,
    hovertext=data['Down Payment'],
    name="Down Payment"
    ))

fig8.add_trace(go.Bar(
    x=data['State'], 
    y=100-(data['Down Payment']/data['All Industry Average Salary']*100),
    text=data["All Industry Average Salary"], #.map('${:,.0f}'.format), 
    textposition='inside',
    textfont=dict(color="White"),
    marker_color="#5d8b7c",
    width=0.8,
    hovertext=data['All Industry Average Salary'],
    name="Average Salary (All Industries)"
    ))

fig8.add_hline(y=20, line_color="red")

fig8.update_layout(barmode='stack', 
                   title_text='Percentage of 1 Year\'s Salary Needed for Down Payment',
                   xaxis_title="State",
                   yaxis_title="Percentage %",
                   height=600,
                   width=1200,
                   plot_bgcolor="#F2EBDF"
                   )
fig8.update_xaxes(tickangle=60)
fig8.show()

# %%
# Median Income by Field needed to Afford Monthly Housing Payment

# %%
# GROUP 4 PLOT TAX BURDEN METRICS
# Paycheck-to-Paycheck Tax Burden (Income v Sales)
tax_data = pd.DataFrame(data, columns=["State", "Abbr", "Data Analyst Monthly Gross Income","Data Analyst Monthly Tax Adjusted Income",
                                       "Data Scientist Monthly Gross Income","Data Scientist Monthly Tax Adjusted Income", "Monthly Mortgage Cost", 
                                       "Total Tax Burden","Property Tax Burden","Income Tax Burden","Sales Tax Burden"])
tax_data.head()

# %%
da_rent_tax = pd.DataFrame(tax_data, columns=["State", "Abbr", "Data Analyst Monthly Gross Income","Data Analyst Monthly Tax Adjusted Income",
                                              "Monthly Mortgage Cost", "Total Tax Burden","Property Tax Burden","Income Tax Burden","Sales Tax Burden"])

da_rent_tax['State Income Tax Cost'] = da_rent_tax['Data Analyst Monthly Gross Income'] * da_rent_tax['Income Tax Burden']/100
da_rent_tax['State Sales Tax Cost'] = da_rent_tax['Data Analyst Monthly Tax Adjusted Income'] * da_rent_tax['Sales Tax Burden']/100
da_rent_tax.head()

# %%
da_own_tax = pd.DataFrame(tax_data, columns=["State", "Abbr", "Data Analyst Monthly Gross Income","Data Analyst Monthly Tax Adjusted Income",
                                              "Monthly Mortgage Cost", "Total Tax Burden","Property Tax Burden","Income Tax Burden","Sales Tax Burden"])

da_own_tax['State Income Tax Cost'] = da_own_tax['Data Analyst Monthly Gross Income'] * da_own_tax['Income Tax Burden']/100
da_own_tax['State Property Tax Cost'] = da_own_tax['Monthly Mortgage Cost'] * da_own_tax['Property Tax Burden']/100
da_own_tax['State Sales Tax Cost'] = (da_own_tax['Data Analyst Monthly Tax Adjusted Income']-da_own_tax['Monthly Mortgage Cost'] ) * da_own_tax['Sales Tax Burden']/100
da_own_tax.head()

# %%
ds_rent_tax = pd.DataFrame(tax_data, columns=["State", "Abbr", "Data Scientist Monthly Gross Income","Data Scientist Monthly Tax Adjusted Income", 
                                              "Monthly Mortgage Cost", "Total Tax Burden","Property Tax Burden","Income Tax Burden","Sales Tax Burden"])
ds_rent_tax['State Income Tax Cost'] = ds_rent_tax['Data Scientist Monthly Gross Income'] * ds_rent_tax['Income Tax Burden']/100
ds_rent_tax['State Sales Tax Cost'] = ds_rent_tax['Data Scientist Monthly Tax Adjusted Income'] * ds_rent_tax['Sales Tax Burden']/100
ds_rent_tax.head()

# %%
ds_own_tax = pd.DataFrame(tax_data, columns=["State", "Abbr", "Data Scientist Monthly Gross Income","Data Scientist Monthly Tax Adjusted Income",
                                              "Monthly Mortgage Cost", "Total Tax Burden","Property Tax Burden","Income Tax Burden","Sales Tax Burden"])

ds_own_tax['State Income Tax Cost'] = ds_own_tax['Data Scientist Monthly Gross Income'] * ds_own_tax['Income Tax Burden']/100
ds_own_tax['State Property Tax Cost'] = ds_own_tax['Monthly Mortgage Cost'] * ds_own_tax['Property Tax Burden']/100
ds_own_tax['State Sales Tax Cost'] = (ds_own_tax['Data Scientist Monthly Tax Adjusted Income']-ds_own_tax['Monthly Mortgage Cost'] ) * ds_own_tax['Sales Tax Burden']/100
ds_own_tax.head()


# %%
da_rent_tax = pd.melt(da_rent_tax, id_vars=['State', 'Abbr'], value_vars=['State Sales Tax Cost', 'State Income Tax Cost'], 
                         var_name="Tax Type", value_name='Tax Cost')
da_rent_tax.head()

# %%
da_own_tax = pd.melt(da_own_tax, id_vars=['State', 'Abbr'], value_vars=['State Sales Tax Cost', 'State Income Tax Cost', 'State Property Tax Cost'], 
                         var_name="Tax Type", value_name='Tax Cost')
ds_rent_tax = pd.melt(ds_rent_tax, id_vars=['State', 'Abbr'], value_vars=['State Sales Tax Cost', 'State Income Tax Cost'], 
                         var_name="Tax Type", value_name='Tax Cost')
ds_own_tax = pd.melt(ds_own_tax, id_vars=['State', 'Abbr'], value_vars=['State Sales Tax Cost', 'State Income Tax Cost', 'State Property Tax Cost'], 
                         var_name="Tax Type", value_name='Tax Cost')

# %%
# Data Analyst Monthly Tax Burden (Renter)

fig9 = px.bar_polar(da_rent_tax, r="Tax Cost", theta="Abbr",
                   color="Tax Type", 
                   hover_data=["Tax Type"],
                   color_discrete_sequence= ["#4c5d7d", "#74b5ac"])

fig9.update_polars(bgcolor="#F2EBDF"),
fig9.update_layout(
    title = "Tax Burden (Data Analyst - Renter)",
    polar = dict(
        radialaxis = dict(showticklabels=False),
        angularaxis = dict(showticklabels=True)), 
)

fig9.show()

# %%
# Data Analyst Monthly Tax Burden (Home Owner)
fig10 = px.bar_polar(da_own_tax, r="Tax Cost", theta="Abbr",
                   color="Tax Type", 
                   hover_data=["Tax Type"],
                   color_discrete_sequence= ["#4c5d7d", "#74b5ac", "#cff1f9"])

fig10.update_polars(bgcolor="#F2EBDF"),
fig10.update_layout(
    title = "Tax Burden (Data Analyst - Home Owner)",
    polar = dict(
        radialaxis = dict(showticklabels=False),
        angularaxis = dict(showticklabels=True)
    ),  
)

fig10.show()

# %%
# Data Scientist Monthly Tax Burden (Renter)
fig11 = px.bar_polar(ds_rent_tax, r="Tax Cost", theta="Abbr",
                   color="Tax Type", 
                   hover_data=["Tax Type"],
                   color_discrete_sequence= ["#4c5d7d", "#74b5ac"])

fig11.update_polars(bgcolor="#F2EBDF"),
fig11.update_layout(
    title = "Tax Burden (Data Scientist - Renter)",
    polar = dict(
        radialaxis = dict(showticklabels=False),
        angularaxis = dict(showticklabels=True)
    ),  
)

fig11.show()

# %%
# Data Scientist Monthly Tax Burden (Home Owner)
fig12 = px.bar_polar(ds_own_tax, r="Tax Cost", theta="Abbr",
                   color="Tax Type", 
                   hover_data=["Tax Type"],
                  color_discrete_sequence= ["#4c5d7d", "#74b5ac", "#cff1f9"])

fig12.update_polars(bgcolor="#F2EBDF"),
fig12.update_layout(
    title = "Tax Burden (Data Scientist - Home Owner)",
    polar = dict(
        radialaxis = dict(showticklabels=False),
        angularaxis = dict(showticklabels=True)
    ),  
)

fig12.show()