#!/usr/bin/env python
# coding: utf-8

# # About Dataset

# Context

# 
# E-commerce has become a new channel to support businesses development. Through e-commerce, businesses can get access and establish a wider market presence by providing cheaper and more efficient distribution channels for their products or services. E-commerce has also changed the way people shop and consume products and services. Many people are turning to their computers or smart devices to order goods, which can easily be delivered to their homes.

# Content

# 
# This is a sales transaction data set of UK-based e-commerce (online retail) for one year. This London-based shop has been selling gifts and homewares for adults and children through the website since 2007. Their customers come from all over the world and usually make direct purchases for themselves. There are also small businesses that buy in bulk and sell to other customers through retail outlet channels.

# The data set contains 500K + rows and 8 columns. The following is the description of each column.

# 1.TransactionNo (categorical): a six-digit unique number that defines each transaction. The letter “C” in the code indicates a cancellation.

# 2.Date (numeric): the date when each transaction was generated.

# 3.ProductNo (categorical): a five or six-digit unique character used to identify a specific product.
# 

# 4.Product (categorical): product/item name.
# 

# 5.Price (numeric): the price of each product per unit in pound sterling (£).
# 

# 6.Quantity (numeric): the quantity of each product per transaction. Negative values related to cancelled transactions.
# 

# 7.CustomerNo (categorical): a five-digit unique number that defines each customer.
# 

# 8.Country (categorical): name of the country where the customer resides.
# 

# # Question

# 1.How was the sales trend over the months?

# 2.What are the most frequently purchased products?
# 

# 3.How many products does the customer purchase in each transaction?
# 

# 4.What are the most profitable segment customers?
# 

# 5.Based on your findings, what strategy could you recommend to the business to gain more profit?
# 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from matplotlib.ticker import FuncFormatter
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df = pd.read_csv('Sales Transaction v.4a.csv')


# In[3]:


df.head()


# # Preprocessing the Data

# In[4]:


#checking the no of columns & rows of the data
df.shape


# In[5]:


df.info()


# In[70]:


#no of duplicates
df.duplicated().sum()


# In[7]:


df[df.duplicated(subset=['TransactionNo','ProductName','ProductNo'])].head()


# In[8]:


#removing duplicates
non_dup = df[~df.duplicated()]


# In[9]:


non_dup.shape


# In[10]:


#converting the date object to datetime format for easy analysis
df['Date']=pd.to_datetime(df['Date'])


# In[11]:


df['Month'] = df['Date'].dt.month 


# In[12]:


df.head()


# In[13]:


#Extracting year column from date column
df['Year'] = df['Date'].dt.year


# In[72]:


df['Year'].nunique()


# In[15]:


df['Year'].value_counts()


# In[16]:


df.tail()


# In[17]:


#Checking for null values
df.isnull().sum()


# In[18]:


#dropping duplicates
df.dropna(inplace=True)


# In[19]:


df.isnull().sum()


# In[20]:


#rename columns for better understanding
df=df.rename(columns={'TransactionNo':'Transaction_id','ProductNo':'Product_id','CustomerNo':'Customer_id',
                   'Country':'Customer_Country','Date':'Transaction_Date','Year':'Transaction_Year',
                   'Month':'Transaction_Month'})


# In[21]:


df.head()


# In[22]:


df['Customer_Country'].unique()


# In[23]:


df['Quantity'].min()


# In[24]:


#Dropping negative values
df=df[~df['Quantity']<0]


# In[25]:


df['Quantity'].min()


# In[26]:


#Creating Sales Total column based on units of products bought and price
df['Sales_Total'] = df['Quantity'] * df['Price']


# In[27]:


df.head()


# In[28]:


df.describe()


# # Exploratory Data Analysis

# # The Most Expensive Product in the Store

# In[29]:


most_expensive_product_name = df['ProductName'][df['Price'].idxmax()]
most_expensive_price = df['Price'].max()

print("The most expensive product is '{}' with a price of ${:.2f}".format(most_expensive_product_name, most_expensive_price))


# # The Chepeast Product in the store

# In[30]:


The_cheapest_product_name = df['ProductName'][df['Price'].idxmin()]
The_chepeast_price = df['Price'].min()
print("The Chepeast product is '{}' with a price of ${:.2f}".format(The_cheapest_product_name, The_chepeast_price))


# In[31]:


df.head()


# # 1.How was the sales trend over the months?

# In[32]:


sns.countplot(x=df['Transaction_Month'],color='blue')
plt.title('Sales Trend Over the Months')
plt.ylabel('Sales Count')
plt.xlabel('Month')
plt.show()


# # 2.What are the most frequently purchased products?

# In[33]:


#selecting the products based on quantitiy and sorting them accordingly
top_purchased_products = df.groupby(['ProductName'])['Quantity'].sum().reset_index()


# In[34]:


#then sorting them in descending order for the top 10 most frequently purchased
top_purchased_products = top_purchased_products.sort_values(by=['Quantity'],ascending= False)


# # Top 10 Highest Frequently Purchased Products

# In[35]:


top_purchased_products.head(10)


# # A visual representation of Top 10 Highest Frequently Purchased Products

# In[36]:


plt.figure(figsize=(10, 6))
sns.barplot(x='Quantity', y='ProductName', data=top_purchased_products.head(10), palette='tab10')
plt.xlabel('Quantity')
plt.ylabel('ProductName')
plt.title('Top 10 Highest Frequently Purchased Products')
plt.show()


# From the result above, the most frequently purchased product is 'Paper Craft Little Birdie' with a Quantity of 80995 

# In[37]:


words=df['ProductName']
words = " ".join(df['ProductName'])


# In[38]:


wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


# # 3.How many products does the customer purchase in each transaction?

# In[39]:


avg_products_per_trans = round(df['Quantity'].mean())
print(f"The average Number of Products Purchased Per Transaction : {avg_products_per_trans}")


# In[40]:


df.groupby('Customer_id')['Sales_Total'].sum()


# In[41]:


df.head()


# # 4 What are the most profitable segment customers?

# In[42]:


profit_per_segment=df.groupby('Customer_Country')['Sales_Total'].sum().reset_index()
profit_per_segment = profit_per_segment.sort_values(by='Sales_Total',ascending=False).head(10)


# In[43]:


profit_per_segment.head()


# In[44]:


def format_millions(value, _):
    return f'{value/1e6:.2f}M'


# ## A visual Representation of top 10 most Profitable segments

# In[45]:


# Visualization
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Customer_Country', y='Sales_Total', data=profit_per_segment, color="blue")
ax.yaxis.set_major_formatter(FuncFormatter(format_millions))
for p in ax.patches:
    height = p.get_height()
    ax.annotate(format_millions(height, None), (p.get_x() + p.get_width() / 2., height), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.title('Top 10 Most Profit per Country Segments')
plt.xticks(rotation=45)
plt.show()


# United Kingdom stands out as the top perfoming country in terms of sales with a Total sales of Over 50M 

# # Top 10 Least Performing Segments 

# In[46]:


#Top 10 Least Profitable Segments
Bottom_10_selling_Regions = df.groupby('Customer_Country')['Sales_Total'].sum().reset_index()
Bottom_10_selling_Regions = Bottom_10_selling_Regions.sort_values(by='Sales_Total').head(10)
Bottom_10_selling_Regions.head(10)


# In[47]:


# Visualization
plt.figure(figsize=(12, 6))
ax = sns.barplot(x='Customer_Country', y='Sales_Total', data=Bottom_10_selling_Regions, color='red')
plt.xlabel('Customer_Country')
plt.ylabel('Sales_Total')
plt.title('Top 10 Least Profitable Country Segments')
plt.xticks(rotation=45)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', fontsize=11, color='black', xytext=(0, 5), textcoords='offset points')
plt.show()


# From the result,Saudi Arabia is the least performing Country with sales of 969.50

# In[48]:


#Transaction ids with the highest purchased Products
total_purchase_Per_transation = df.groupby('Transaction_id')['Quantity'].sum().reset_index()


# In[49]:


top_10=total_purchase_Per_transation.sort_values(by='Quantity',ascending=False).head(10)
top_10.head()


# In[50]:


# Visualization
plt.figure(figsize=(10, 6))
sns.barplot(data=top_10, x='Transaction_id', y='Quantity', palette='viridis')
plt.xlabel('Transaction_id')
plt.ylabel('Number of Purchased Products')
plt.title('Top 10 Transactions by Total Number of Purchased Products')
plt.xticks(rotation=45)
plt.show()


# # Customers with the highest number of transactions

# In[51]:


Top_10_customers = df.groupby('Customer_id')['Transaction_id'].nunique().reset_index()


# In[52]:


top_customers=Top_10_customers.sort_values(by='Transaction_id',ascending=False).head(10)


# In[53]:


top_customers.head(10)


# In[54]:


# Visualization
plt.figure(figsize=(10, 6))
sns.barplot(x='Customer_id', y='Transaction_id', data=top_customers, palette='magma')
plt.title('Top 10 Customers with the Most Transactions')
plt.xlabel('Customer_id')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=45)
plt.show()


# From the result above, customer with the highest number of Transactions is identified with id 12748.0 with a total
# of 207 transactions

# # 5.Based on your findings, what strategy could you recommend to the business to gain more profit?
# 

# 1.Data Driven Decisions : Utilise Data analytics in order to understand trends and customer preferences

# 2.Optimized sales Timing: Concetrate marketing efforts during the months of increased sales
# Do promotions on months with the least sales

# 3.Explore new Markets especially in less profitable regions

# 4.Discount and Promotions :To Stragically simulate demand, introduce sales discounts and promotions

# 5.Product Diversification : To encourage additional purchase,introduce related products 

# 6.Cost control : Streamline Operations and  negotiate supplier deals to reduce costs

# 7.Stock the unavailable products that make customers cancel their orders 

# In[ ]:




