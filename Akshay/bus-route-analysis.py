# Code to analyse bus routes
# by Akshay Pal

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import csv files into dataframes
obc_weekday = pd.read_csv('obc-weekday.csv')
obc_weekend = pd.read_csv('obc-weekend.csv')
sc_weekday = pd.read_csv('stagecoach-weekday.csv')
sc_weekend = pd.read_csv('stagecoach-weekend.csv')
tt_weekday = pd.read_csv('thames-travel-weekday.csv')
tt_weekend = pd.read_csv('thames-travel-weekend.csv')
shared_weekday = pd.read_csv('shared-weekday.csv')          # These routes are shared by OBC and stagecoach
shared_weekend = pd.read_csv('shared-weekend.csv')

# create lists of dataframes
weekday_dfs_list = [obc_weekday, sc_weekday, tt_weekday, shared_weekday]
weekend_dfs_list = [obc_weekend, sc_weekend, tt_weekend, shared_weekend]

# FUEL USAGE
# calculate fuel usage in gallons
for i in weekday_dfs_list:
    i['Daily Fuel Usage (gallons)'] = i.apply(lambda row: row["Daily Total Distance (miles)"]/row["MPG rating"], axis=1)

for j in weekend_dfs_list:
    j['Daily Fuel Usage (gallons)'] = j.apply(lambda row: row["Daily Total Distance (miles)"]/row["MPG rating"], axis=1)

# sum fuel usage for each company per week (weekday*5 + weekend*2) 
obc_total_fuel_usage = obc_weekday['Daily Fuel Usage (gallons)'].sum()*5 + obc_weekend['Daily Fuel Usage (gallons)'].sum()*2
sc_total_fuel_usage = sc_weekday['Daily Fuel Usage (gallons)'].sum()*5 + sc_weekend['Daily Fuel Usage (gallons)'].sum()*2
tt_total_fuel_usage = tt_weekday['Daily Fuel Usage (gallons)'].sum()*5 + tt_weekend['Daily Fuel Usage (gallons)'].sum()*2
shared_total_fuel_usage = shared_weekday['Daily Fuel Usage (gallons)'].sum()*5 + shared_weekend['Daily Fuel Usage (gallons)'].sum()*2

# create data and dataframe for companies
companies_data = {'Companies': ['OBC', 'Stagecoach', 'Thames Travel', 'Shared'], 'Weekly Fuel Usage': [obc_total_fuel_usage, sc_total_fuel_usage, tt_total_fuel_usage, shared_total_fuel_usage]}
companies_df = pd.DataFrame(data=companies_data)
# divide it by 1000 so graph is neater, unit is now thousands of gallons
companies_df['Weekly Fuel Usage'] = companies_df['Weekly Fuel Usage']*0.001 

# EMISSIONS
# 2.68 kg CO2 released per litre of diesel burnt
# 1 uk gallon = 4.55 litre 
# therefore 12.2 kg (4.55*2.68) CO2 released per uk gallon of diesel burnt

companies_df['Weekly Emissions'] = companies_df.apply(lambda row: row['Weekly Fuel Usage']*12.2, axis=1) # emissions in thousands of kgs

# energy equivalence and hydrogen requirement
# E = V*rho*eta where rho = energy density and eta = drivetrain efficiency

diesel_rho = 175 # MJ/gallon
diesel_eta = 0.41

h2_rho = 12.6 # MJ/gallon
h2_eta = 0.6
h2_mass_density = 23 # kg/m^3

# calculate weekly energy usage in MJ
companies_df['Weekly Energy Usage'] = companies_df.apply(lambda row: row['Weekly Fuel Usage']*diesel_rho*diesel_eta, axis=1)

# calculate weekly hydrogen requirement in thousands of kgs
companies_df['Weekly Hydrogen Requirement'] = companies_df.apply(lambda row: (row['Weekly Energy Usage']/(h2_rho*h2_eta))*h2_mass_density, axis=1)

# plot fuel usage and emissions
ax = companies_df.plot.bar(x='Companies', y='Weekly Fuel Usage', rot=0, color='#95c22b', legend=False)
ax2 = companies_df.plot.bar(x='Companies', y='Weekly Emissions', rot=0, color='#95c22b', secondary_y=True, ax=ax, legend=False)
ax.set_ylabel('Fuel Usage (thousands of gallons)')
ax2.set_ylabel('CO2 Emissions (thousands of kgs)')
plt.xlabel('Service Provider')
plt.title('Weekly fuel usage and emissions for different Oxfordshire bus networks')
plt.show()

# plot hydrogen requirement 
companies_df.plot.bar(x='Companies', y='Weekly Hydrogen Requirement', rot=0, color='#95c22b', legend=False)
plt.ylabel('Hydrogen requirement (thousands of kgs)')
plt.xlabel('Service Provider')
plt.title('Weekly hydrogen requirement for different Oxfordshire bus networks')
plt.show()

# calculate total hydrogen requirement from all providers (think the unit is thousands of kgs)
total_h2_required = companies_df['Weekly Hydrogen Requirement'].sum()
print(companies_df['Weekly Hydrogen Requirement'])
print(total_h2_required)












