import pandas as pd
import os

# Merging 12 months of data into a single file #
# df = pd.read_csv("D:/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv")

# files = [file for file in os.listdir("D:/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data")]
# all_months_data = pd.DataFrame()

# for file in files:
#     df = pd.read_csv("D:/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/"+file)
#     all_months_data = pd.concat([all_months_data, df])

# print(all_months_data.head())
# all_months_data.to_csv("all_data.csv",index = False)

# Read the updated data frame
all_data = pd.read_csv("all_data.csv")
#print(all_data.head())

#Cleaning the data
#Drop NaN rows
nan_df = all_data[all_data.isna().any(axis=1)]
#print(nan_df.head())
all_data = all_data.dropna(how='all')

all_data = all_data[all_data['Order Date'].str[0:2]!='Or']
#print(all_data.head())

# Convert columns to the correct type
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) 
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

#Augment data with additional columns

# Adding the Month column
all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
#print(all_data.head())

# Adding a sales column
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
#print(all_data.head())

# Adding a city column
# .apply() method
#all_data['Name'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[1])
#print(all_data.head())

def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]

#all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x)+ ' '+get_state(x))
# By using concepts of f strings
all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")


# What was the best month for sales? How much was earned in that month?
#print(all_data.groupby('Month').sum())

import matplotlib.pyplot as plt
# months = range(1,13)
# results = all_data.groupby('Month').sum()
# plt.bar(months, results['Sales'])
# plt.xticks(months)
# plt.ylabel('Sales in USD')
# plt.xlabel('Month number')
# #plt.show()

# What US city has highest number of sales?

results1 = all_data.groupby('City').sum()
#print(results1)
# months = range(1,13)
# #cities = all_data['City'].unique()
# cities = [city for city,df in all_data.groupby('City')]
# plt.bar(cities, results1['Sales'])
# plt.xticks(cities,rotation = 'vertical',size =8 )
# plt.ylabel('Sales in USD')
# plt.xlabel('City')
#plt.show()

## What time should we display advertisements to maximize liklehood of customer's buying product?

# #Converting string to date time format
# all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
# #print(all_data.head())
# all_data['Hour'] = all_data['Order Date'].dt.hour
# #print(all_data['Hour'])
# all_data['Minute'] = all_data['Order Date'].dt.minute

# hours = [hour for hour,df in all_data.groupby('Hour')]
# plt.plot(hours,all_data.groupby(['Hour']).count())
# plt.xticks(hours)
# plt.ylabel('Number of Orders')
# plt.xlabel('Hour')
# plt.grid()
# plt.show()

# Recommendation is around 11am or 7pm

# What products are most ofetn sold together
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']= df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
#print(df['Grouped'])
df = df[['Order ID','Grouped']].drop_duplicates()
#print(df)

from itertools import combinations
from collections import Counter

count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
#print(count.most_common(10))

# What product sold the most? Why do you think it sold the most?

product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product,df in product_group]

plt.bar(products,quantity_ordered)
plt.xlabel('Product Name')
plt.ylabel('Quantity Ordered')
plt.xticks(products,rotation = 'vertical',size =8 )
plt.show()

# AAA,AA batteries are cheap. Now seeing the correlation between the costs of each product

prices= all_data.groupby('Product').mean()['Price Each']

# Overlaying the prices on previous graph
# Adding a secondary ylabel
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products,quantity_ordered,color = 'g')
ax2.plot(products,prices,'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color = 'g')
ax2.set_ylabel('Price',color = 'b')
ax1.set_xticklabels(products,rotation = 'vertical',size =8)
plt.show()
























