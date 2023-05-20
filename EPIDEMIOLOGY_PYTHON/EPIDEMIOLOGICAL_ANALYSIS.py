
import pandas as pd

# Add the file path where the data is located
file_path = 'https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/EPIDEMIOLOGY_COV19_SHINY/outbreak.csv'

# Load the data into a DataFrame
df = pd.read_csv(file_path)

# Calculate the total number of cases
total_cases = df['Cases'].sum()

# Calculate the total number of deaths
total_deaths = df['Deaths'].sum()

# Calculate the overall case fatality rate
case_fatality_rate = (total_deaths / total_cases) * 100

# Print the results
print('Total Cases: ', total_cases)
print('Total Deaths: ', total_deaths)
print('Case Fatality Rate: ', case_fatality_rate)




