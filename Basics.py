
#  Project to help me clean data and do further complex
#  analysis for practise

# In[39]:

import pandas as pd
import numpy as np

autos = pd.read_csv('autos.csv', encoding = 'Latin-1')

# In[40]:

autos.head
autos.info()

#   Observations:
# 
# - 20 columns, most are strings
# - Some columns missing rows (null values)
# - Some columns are the wrong datatype

# In[41]:

autos.head

# In[42]:

autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'num_photos', 'postal_code',
       'last_seen']
autos.columns

#  Current Edits
# 
# - Changed some column names to make it more accurate and short
# - Changed column names from camelcase to snakecase

# In[43]:

autos.describe(include = 'all')

#  Observations
# 
# - Almost all values in 'Seller' & 'Offer type' columns are the same
# - No. of photos column seems to have no values 

# In[44]:

print(autos['price'].unique())

# In[45]:

autos["price"] = (autos["price"]
                          .str.replace("$","")
                          .str.replace(",","")
                          .astype(int)
                          )

# In[46]:

autos = autos.drop(['seller','offer_type','num_photos'], axis = 1)

# In[47]:

autos["odometer"] = (autos["odometer"]
                             .str.replace("km","")
                             .str.replace(",","")
                             .astype(int)
                             )

# In[49]:

autos = autos.rename({'odometer':'odometer_km'}, axis = 1)

# In[51]:

autos['odometer_km'].value_counts()

# In[52]:

autos['price'].describe()

# In[53]:

autos['price'].value_counts().head()

#  Obervations
# 
# - Max price is 100,000,000 USD which seems unlikely
# - 1421 values with O as price

# In[54]:

autos["price"].value_counts().sort_index(ascending=True).head(15)

# Observations
# 
# -Since Ebay is an auction site, there could be legitimate li
#  stings starting at $1.
# 
# -However, it is very unlikely that listings could over $350,000.
#  So we should limit the price range to stay in between
# 

# In[55]:

autos[autos['price'].between(1,350000)]
autos.head(20)

# In[56]:

autos['registration_year'].describe()

# In[57]:

autos = autos[autos["registration_year"].between(1900,2016)]
autos["registration_year"].value_counts(normalize=True).head(10)

#   Observations
# 
# - Latest car registration date was 9999
# - Earliest was 1000
# - So restricted data to cars registered between 1900 & 2016
# 

# In[58]:

brand_counts = autos['brand'].value_counts(normalize = True)
print(brand_counts)

# In[59]:

common_brands = brand_counts[brand_counts > 0.05].index
print(common_brands)

# In[60]:


brand_highest_prices = {}

for brand in common_brands:
    
    is_brand = autos['brand'] == brand
    
    brand_rows = autos[is_brand]
    
    top_prices = brand_rows.sort_values('price', ascending = False).iloc[0]
    
    price = top_prices['price']
    
    brand_highest_prices[brand] = price

print(brand_highest_prices)

# Normalized data to pick the most common brands that are listed on Ebay.
# Then, created a dictionary that shows the highest price 
# listed for each common brand.
# 

# In[61]:

brand_mean_prices = {}

for brand in common_brands:
    
    is_brand = autos[autos['brand'] == brand]
    price = is_brand['price'].mean()
    
    brand_mean_prices[brand] = int(price)

print(brand_mean_prices)

# In[62]:

brand_mean_mileage = {}

for brand in common_brands:
    is_brand = autos[autos['brand'] == brand]
    mean_mileage = is_brand['odometer_km'].mean()
    
    brand_mean_mileage[brand] = int(mean_mileage)
    
print(brand_mean_mileage)

# In[73]:

bmm = pd.Series(brand_mean_mileage)
bmp = pd.Series(brand_mean_prices)
print(bmp)

# In[69]:

brand_mean = pd.DataFrame(bmm, columns = ['mean_mileage'])
brand_mean

# In[81]:

brand_mean['mean_price'] = bmp
brand_mean.drop(['bmp'], axis = 1)

# Created DF 'brand_mean' to compare the 2 columns together.
# 
#  Observations:
# 
# - Mileage on the cars listed on the website does not vary as much as prices do
