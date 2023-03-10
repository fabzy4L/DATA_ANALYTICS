import numpy as np
import pandas as pd
from pandas import Series, DataFrame

########################################

address = "/Users/f4L/PycharmProjects/Jupyter Notebooks/mtcars.csv"
cars = pd.read_csv(address)
#print(cars.columns)

########################################

cars.columns.edit = ['car_names','mpg','cyl','disp','hp','drat','wt','qsec','vs','am','gear','carb']
del cars['Unnamed: 0']
#print(cars)

########################################
y = cars.groupby(cars['cyl'])
cars_groups = y
print(cars_groups.mean())