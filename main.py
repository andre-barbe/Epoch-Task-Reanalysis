#Main program to do everything
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

#merge data
data_main = data_main.merge(data_funding,
                            on="Organization(s)",
                            how="outer")  # Outer merge keeps data that is in either


#Create Graph 1: orga cats over time
#Create new data set
data_grouped_org_catagory=data_main
data_grouped_org_catagory=data_main.groupby(['Organization Categorization', 'Year']).count().reset_index()

#Every entry has a Publication date so I use this as the count variable
data_grouped_org_catagory['Quantity'] = data_grouped_org_catagory['Publication date']

print("Test")

#Resahpe data to wide
#https://stackoverflow.com/questions/22798934/pandas-long-to-wide-reshape-by-two-variables
data_grouped_org_catagory=data_grouped_org_catagory.pivot(index='Year',
                                                          columns=['Organization Categorization'],
                                                          values='Quantity')

#Fill with zero for years-catagory paris that have no entries at all
data_grouped_org_catagory = data_grouped_org_catagory.fillna(0)

#Create graph 1:
# See https://pandas.pydata.org/docs/getting_started/intro_tutorials/04_plotting.html
data_grouped_org_catagory.plot.line()

#Save graph 1
plt.savefig('graphs/fig_org_cat_over_time.png')

print("Test")


#Create graph 2:
#Create a new dataset
data_top_companies=data_main

#Drop data from 2017 or earlier
data_top_companies = data_top_companies[data_main['Year'] >= 2018]

#Create new column with names
#for locationhttps://stackoverflow.com/questions/49161120/pandas-python-set-value-of-one-column-based-on-value-in-another-column
#for isna https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html
#turn all not top to "not top"
data_top_companies.loc[data_top_companies['Employees'].isna(),['Organization']]='Not top'
#retain name for top companies
#data_top_companies.loc[~data_top_companies['Employees'].isna(),['Organization']]=data_top_companies['Organization(s)']
data_top_companies.loc[~data_top_companies['Employees'].isna(),['Organization']]='Top'

#Create quantity variable
data_top_companies=data_top_companies.groupby(['Organization', 'Year']).count().reset_index()
#Every entry has a Publication date so I use this as the count variable
data_top_companies['Quantity'] = data_top_companies['Publication date']

#Resahpe data to wide
#https://stackoverflow.com/questions/22798934/pandas-long-to-wide-reshape-by-two-variables
data_top_companies=data_top_companies.pivot(index='Year',
                                                          columns=['Organization'],
                                                          values='Quantity'
                                            )



#Fill with zero for years-catagory paris that have no entries at all
data_top_companies = data_top_companies.fillna(0)

#Create graph 2
data_top_companies.plot.bar()

#Save graph 2
plt.savefig('graphs/fig_top_companies_over_time.png')



#Create graph 3: employees vs count
#Create a new dataset
data_top_employees=data_main

#Drop data from 2017 or earlier
data_top_employees = data_top_employees[data_main['Year'] >= 2018]

#Drop if don't have employee data
data_top_employees = data_top_employees[~data_main['Employees'].isna()]

print("Test")


#Collapse data to just one for each org
data_top_employees=data_top_employees.groupby(['Organization(s)']).count().reset_index()

#Create quantity variable
#Every entry has a Publication date so I use this as the count variable
data_top_employees['Quantity'] = data_top_employees['Publication date']

print("Test")


#Drop all columns but quantity and org
#https://stackoverflow.com/questions/45846189/how-to-delete-all-columns-in-dataframe-except-certain-ones
data_top_employees = data_top_employees.loc[:, data_top_employees.columns.intersection(['Quantity','Organization(s)'])]


#merge data
data_top_employees = data_top_employees.merge(data_funding,
                            on="Organization(s)",
                            how="outer")  # Outer merge keeps data that is in either

print("Program successfully completed")


#Turn employees into number variable
#https://www.geeksforgeeks.org/how-to-convert-categorical-variable-to-numeric-in-pandas/
#https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
data_top_employees['Employees']= pd.to_numeric(
    data_top_employees['Employees'],
    errors='coerce')

#https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
#drop if missing employees or quantity
data_top_employees = data_top_employees.dropna(subset=['Employees','Quantity'])

#Create ax
#https://stackoverflow.com/questions/29568110/how-to-use-ax-with-pandas-and-matplotlib
#fig,ax=plt.subplots()

#Create graph
#https://stackoverflow.com/questions/41635448/how-can-i-draw-scatter-trend-line-on-matplot-python-pandas

#define x and y
x=data_top_employees['Employees']
y=data_top_employees['Quantity']

#Create scatter plot
plt.scatter(x, y)

#Calculate line
z = np.polyfit(x, y, 1)

#https://numpy.org/doc/stable/reference/generated/numpy.poly1d.html
p = np.poly1d(z)

#Draw line
plt.plot(x,
         p(x),
        #Keyword arguments
         # See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
         "r--")

plt.show()

#Save graph
plt.savefig('graphs/fig_employees_vs_count.png')


print("Program successfully completed")
