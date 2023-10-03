import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as mpl
import seaborn as sns
print(np.log(1))


#pd.read_excel('myfile.xlsx',sheet_name='Sheet1', index_col=None, na_values=['NA']) pd.read_stata('myfile.dta')
#pd.read_sas('myfile.sas7bdat')
#pd.read_hdf('myfile.h5','df')

#df.dtypes gives you the type of data:
#
# df.method()               - description
# head( [n] ), tail( [n] )  - first/last n rows
# describe()                - generate descriptive statistics (for numeric columns only)
# max(), min()              - return max/min values for all numeric columns
# mean(), median()          - return mean/median values for all numeric columns
# std()                     - standard deviation
# sample([n])               - returns a random sample of the data frame
# dropna()                  - drop all the records with missing values



#Group data using rank
df_rank = df.groupby(['rank'])
#Calculate mean value for each numeric column per each group
df_rank.mean()

#Calculate mean salary for each professor rank:
df_sub = df[ df['salary'] > 120000 ]