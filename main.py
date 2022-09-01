#Main program to do everything
import pandas as pd
import numpy as np

#Load Epoch data
data_main = pd.read_csv("raw-data/Parameter, Compute and Data Trends in Machine Learning - NOTABLE ML SYSTEMS.csv")

#Load funding data
sheet_id = '1BiracEUOUOGI7QcmNHyg1YYKSar2xBpeCHYzABye-ZA'
data_funding = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                   sheet_id +
                   '/export?gid=0&format=csv',
                   # Set first column as rownames in data frame
                   index_col=0
                  )

#Drop data from 2017 or earlier
data_main = data_main[data_main['Year'] >= 2018]

#merge data
data_main = data_main.merge(data_funding,
                            on="Organization(s)",
                            how="outer")  # Outer merge keeps data that is in either


print("Program successfully completed")