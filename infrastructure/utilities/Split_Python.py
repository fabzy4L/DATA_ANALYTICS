# importing pandas module
import pandas as pd
  
# reading csv file from url
data = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")
 
# dropping null value columns to avoid errors
data.dropna(inplace = True)
 
# new data frame with split value columns
new = data["Name"].str.split(" ", n = 1, expand = True)
 
# making separate first name column from new data frame
data["First Name"]= new[0]
 
# making separate last name column from new data frame
data["Last Name"]= new[1]
 
# Dropping old Name columns
data.drop(columns =["Name"], inplace = True)
 
# df display
data
