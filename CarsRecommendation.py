#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import the Libraries :
import numpy as np 
import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns 
from sklearn.utils import shuffle 
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix , classification_report
from sklearn.model_selection import cross_val_score , GridSearchCV


# # Data loading :

# In[2]:


# Load the dataset
data = pd.read_csv(r"C:\Users\Dhrumil\Downloads\CARS_1.csv")

# Explore the dataset
print(data.info())
data[1:10]


# # Name vehicles :

# In[3]:


cnt_pro =data['car_name'].value_counts()  [:50]
plt.figure(figsize=(6,4))
sns.barplot(x = cnt_pro.index, y = cnt_pro.values, alpha=0.8)
plt.ylabel('Number of Data', fontsize=12)
plt.xlabel('name', fontsize=9)
plt.xticks(rotation=90)
plt.show()


# # Filter based on inputs :

# ## Fuel Type 

# In[4]:


cnt_pro = data['fuel_type'].value_counts()
plt.figure(figsize=(6,4))
sns.barplot( x = cnt_pro.index,   y = cnt_pro.values, alpha=0.8)
plt.ylabel('Number of Data', fontsize=12)
plt.xlabel('owner', fontsize=12)
plt.xticks(rotation=80)
plt.show();


# # Transmission type :

# In[5]:


cnt_pro = data['transmission_type'].value_counts()
plt.figure(figsize=(6,4))
sns.barplot( x = cnt_pro.index,  y = cnt_pro.values, alpha=0.8)
plt.ylabel('Number of seller_type', fontsize=12)
plt.xlabel('seller_type', fontsize=12)
plt.xticks(rotation=80)
plt.show();


# # Body Type : 

# In[6]:


cnt_pro = data['body_type'].value_counts()
plt.figure(figsize=(6,4))
sns.barplot( x = cnt_pro.index,  y = cnt_pro.values, alpha=0.8)
plt.ylabel(' number of data ', fontsize=12)
plt.xlabel('body_type', fontsize=12)
plt.xticks(rotation=80)
plt.show()


# # Starting Price of vehicles : 

# In[7]:


top_sell = data.sort_values(by='starting_price', ascending=False)
figure = plt.figure(figsize=(10,6))
sns.barplot(y=top_sell.body_type , x= top_sell.starting_price)
plt.xticks()
plt.xlabel('Starting Price ')
plt.ylabel('body_type')
plt.title('The selling price of car')
plt.show()


# # selling Car by seating_capacity :

# In[8]:


top_sell = data.sort_values(by='seating_capacity', ascending=True)[:30]
figure = plt.figure(figsize=(10,6))
sns.barplot(y=top_sell.body_type, x=top_sell.seating_capacity)
plt.xticks()
plt.xlabel('Seating_capacity')
plt.ylabel('Body_type')
plt.title('The selling Car by Seating Capacity')
plt.show()


# ## 5 things you need to know before buying a vehicle. 
# ## Besides paying attention to financial, if you want buy car you need to know about the car like:
# 
# ### 1.  Fuel Type 
# 
# ###  2. Body Type
# 
# ###  3. Transmission Type
# 
# ###  4 . Seating Capacity
# 
# ### 5 . Starting - Ending Price 
# 
# 

# # Content based Filtering :

# In[16]:


# importing laibrery for content based filtering :
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity


# # Filter based on user inputs :

# In[17]:


# load the data :
user_data = pd.read_csv(r'C:\Users\Dhrumil\Downloads\CARS_1.csv')

# Recommendation function
def recommend_cars(user_input, num_recommendations=5):
    # Create a copy of the dataset to filter
    filtered_data = user_data.copy()
    
    # For Fuel:
    if 'fuel_type' in user_input and user_input['fuel_type']:
        filtered_data = filtered_data[filtered_data['fuel_type'] == user_input['fuel_type']]
    
    # For Transmission Type:
    if 'transmission_type' in user_input and user_input['transmission_type']:
        filtered_data = filtered_data[filtered_data['transmission_type'] == user_input['transmission_type']]
        
    # For Body Type:
    if 'body_type' in user_input and user_input['body_type']:
        filtered_data = filtered_data[filtered_data['body_type'] == user_input['body_type']]
        
    # For Seating Capacity:
    if 'seating_capacity' in user_input and user_input['seating_capacity']:
        filtered_data = filtered_data[filtered_data['seating_capacity'] == user_input['seating_capacity']]
        
    # For Starting Price-Ending Price:
    if 'starting_price' in user_input and 'ending_price' in user_input and user_input['starting_price'] and user_input['ending_price']:
        filtered_data = filtered_data[
            (filtered_data['starting_price'] >= user_input['starting_price']) & 
            (filtered_data['ending_price'] <= user_input['ending_price'])
        ]

    # If no cars match the filters, return an empty DataFrame
    if filtered_data.empty:
        return pd.DataFrame(columns=user_data.columns)
    
    # Select features to calculate similarities
    features = filtered_data[['starting_price', 'ending_price', 'rating', 'max_torque_nm', 'max_power_bhp']]
    
    # Compute cosine similarity between cars based on the selected features
    similarities = cosine_similarity(features)
    
    # Use the first entry in the filtered data to find similar cars
    car_index = filtered_data.index[0]
    similar_indices = similarities[car_index].argsort()[-num_recommendations-1:-1][::-1]
    
    # Get the recommended cars based on similarity indices
    recommended_cars = filtered_data.iloc[similar_indices]
    return recommended_cars

# Example user input with optional fields
user_input = {
    'fuel_type': 'Petrol',
    'transmission_type': 'Automatic',
    'starting_price': 500000,
    'ending_price': 1500000,
    'body_type': 'SUV',
    'seating_capacity': 5
}

# Get recommendations
recommendations = recommend_cars(user_input)
print(recommendations)

