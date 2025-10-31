###############################################################
#Customer Segmentation with RFM
###############################################################
###############################################################
# Business Problem
###############################################################
# FLO wants to segment its customers and determine marketing strategies according to these segments.
# For this purpose, customer behaviors will be defined and groups will be created according to these behavior clusters.

# DUE TO PRIVACY REASONS I CANNOT PROVIDE RELEVANT FLO DATASETS THAT HAVE BEEN USED IN THIS PROJECT
###############################################################
# Dataset Story
###############################################################

# The dataset consists of information obtained from the past shopping behaviors of customers who made their last purchases
# as OmniChannel (shopping both online and offline) in 2020 - 2021.

# master_id: Unique customer number
# order_channel: Which channel of the shopping platform is used (Android, ios, Desktop, Mobile, Offline)
# last_order_channel: Channel where the last purchase was made
# first_order_date: Date of the customer's first purchase
# last_order_date: Date of the customer's last purchase
# last_order_date_online: Date of the customer's last purchase on the online platform
# last_order_date_offline: Date of the customer's last purchase on the offline platform
# order_num_total_ever_online: Total number of purchases made by the customer on the online platform
# order_num_total_ever_offline: Total number of purchases made by the customer offline
# customer_value_total_ever_offline: Total amount paid by the customer in offline purchases
# customer_value_total_ever_online: Total amount paid by the customer in online purchases
# interested_in_categories_12: List of categories the customer shopped in the last 12 months

###############################################################
# TASKS
###############################################################
### *** TASK 1: Data Understanding and Preparation

# 1. Read the flo_data_20K.csv data
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.max_rows', 30)  # Display all rows
pd.set_option('display.float_format', lambda x: '%.3f' % x)  # Set decimal precision for numeric values
pd.set_option('display.width', 1000)  # Increase width for output to fit side by side

df_ = pd.read_csv("/datasets/flo_data_20k.csv")
df = df_.copy()
df.head()

# 2. In the dataset:
# a. First 10 observations
df.head(10)

# b. Variable names
df.columns

# c. Descriptive statistics
df.describe().T

# d. Missing values
df.isnull().sum()

# e. Variable types
df.info()


# 3. Omnichannel customers shop from both online and offline platforms.
# Create new variables for the total number of purchases and spending for each customer.

# Create a new Total Order Number column by adding online and offline order numbers
df['omnichannel_order_num'] = df['order_num_total_ever_online'] + df['order_num_total_ever_offline']

# Create a new Total Spending column by adding online and offline total spending
df['omnichannel_value'] = df['customer_value_total_ever_online'] + df['customer_value_total_ever_offline']


# 4. Examine the variable types. Convert the type of variables expressing date to date.

# Find column names that contain the word 'date'
date_columns = [col for col in df.columns if 'date' in col]

# Loop through each column found and convert its type to 'datetime'
for col in date_columns:
    df[col] = pd.to_datetime(df[col])

df.info()


# 5. Look at the distribution of customer numbers, average number of products purchased, and average spending across shopping channels.

channel_analysis = df.groupby('order_channel').agg({"master_id": "nunique",
                                                    "omnichannel_order_num": "mean",
                                                    "omnichannel_value": "mean",})

channel_analysis.columns = ['Customer Count', 'Average Product Count', 'Average Spending']


# 6. Rank the top 10 customers with the highest revenue.

df.sort_values(by='omnichannel_value', ascending=False).head(10)

# 7. Rank the top 10 customers who placed the most orders.

df.sort_values(by='omnichannel_order_num', ascending=False).head(10)

# 8. Functionalize the data preparation process.

def data_prep(df):
    # Check for null values
    df.isnull().sum()

    # Create omnichannel customer metrics
    df['omnichannel_order_num'] = df['order_num_total_ever_online'] + df['order_num_total_ever_offline']
    df['omnichannel_value'] = df['customer_value_total_ever_online'] + df['customer_value_total_ever_offline']

    # Convert date variables to datetime type
    date_columns = [col for col in df.columns if 'date' in col]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    return df


###############################################################
# TASK 2: Calculating RFM Metrics
###############################################################

# Analysis date: 2 days after the date of the last purchase in the dataset
df["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)
type(today_date)


# Step 1: Define Recency, Frequency and Monetary.
# Recency: The time elapsed from the customer's last purchase to the analysis date. The lower the recency value, the more "recent" and valuable the customer is.
# Frequency: The total number of purchases made by the customer in a given time period. The higher the frequency value, the more "loyal" and valuable the customer is.
# Monetary: The total amount spent by the customer in a given time period. The higher the monetary value, the more "profitable" and valuable the customer is.

# Create a new rfm dataframe with customer_id, recency, frequency and monetary values

# Total number of rows in the dataset
total_rows = len(df)
# Number of unique customers in the dataset
unique_customers = df['master_id'].nunique()

total_rows == unique_customers

# Since each row represents a unique customer, there is no need to use group by

# Step 2: Calculate Recency, Frequency and Monetary metrics for each customer.
# Step 3: Assign the metrics you calculated to a variable named rfm.
# Step 4: Change the names of the metrics you created to recency, frequency and monetary.

rfm = pd.DataFrame()
rfm['customer_id'] = df['master_id']
rfm['recency'] = (today_date - df['last_order_date']).dt.days
rfm['frequency'] = df['omnichannel_order_num']
rfm['monetary'] = df['omnichannel_value']

rfm.describe().T

rfm = rfm[rfm["monetary"] > 0]
rfm.head()

rfm_sirali_recency = rfm.sort_values(by="recency", ascending=True)
print(rfm_sirali_recency.head())

###############################################################
# TASK 3: Calculating RF Score
###############################################################

# Step 1: Convert Recency, Frequency and Monetary metrics to scores between 1-5 with the help of qcut.
# Step 2: Save these scores as recency_score, frequency_score and monetary_score.

# qcut function sorts from smallest to largest, divides into quartile values as many as we want
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

# rank(method="first") assigns the first one it sees to the first class, avoiding errors
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])


# Step 3: Express recency_score and frequency_score as a single variable and save it as RF_SCORE.

rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

###############################################################
# TASK 4: Defining RF Scores as Segments
###############################################################
# Define segments and convert RF_SCORE to segments using the defined seg_map to make the created RFM scores more explainable

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)


# Describe the segments
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

rfm[rfm["segment"] == "need_attention"].head()
rfm[rfm["segment"] == "hibernating"].head()
rfm[rfm["segment"] == "champions"].head()


###############################################################
# TASK 5: Time for Action!
###############################################################
# Step 1. Examine the recency, frequency and monetary averages of the segments.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# 2. Find customers in the relevant profile for 2 cases with the help of RFM analysis and save the customer ids to csv.

# a. FLO is adding a new women's shoe brand. The product prices of the brand are above the general customer preferences. For this reason,
# it is desired to communicate specifically with customers in the profile who will be interested in the promotion and product sales of the brand.
# It is planned that these customers should be loyal and shopping from the women's category. Save the customer id numbers to a csv file
# as new_brand_target_customer_id.csv.

# Merge segment and category data, customer_id in rfm = master_id in df
merged_df = pd.merge(rfm,
                     df[['master_id', 'interested_in_categories_12']],
                     left_on='customer_id',
                     right_on='master_id',
                     how='inner')


# Pandas by default keeps columns with different names
# Delete master_id from merged_df to keep it clean
merged_df = merged_df.drop(columns='master_id')



# Loyal customers as "champions" and "loyal_customers"
# Filter those in these segments who also shop from the women's category

target_customers_df = merged_df[
    (merged_df['segment'].isin(['champions', 'loyal_customers'])) &
    (merged_df['interested_in_categories_12'].str.contains("KADIN"))
]
# Select customer ids
target_customer_ids = target_customers_df['customer_id']


# Save as csv file
target_customer_ids.to_csv('yeni_marka_hedef_müşteri_id.csv', index=False)


# b. A discount of close to 40% is planned for Men's and Children's products. It is desired to specifically target customers who are interested
# in these categories, who were good customers in the past but have not shopped for a long time, and newly arrived customers regarding this discount.
# Save the ids of customers in the appropriate profile to a csv file as discount_target_customer_ids.csv.

# Good customers in the past but haven't shopped for a long time: cant_loose, at_risk, about_to_sleep
# Newly arrived customers: new_customers

target_segments = ["cant_loose", "at_risk", "about_to_sleep", "new_customers"]

# Identify customers in the appropriate profile
discount_target_df = merged_df[
    (merged_df['segment'].isin(target_segments)) &
    (merged_df['interested_in_categories_12'].str.contains("ERKEK|COCUK"))  # Men's or Children's
]

# Select customer ids
discount_target_ids = discount_target_df['customer_id']

# Save to csv file
discount_target_ids.to_csv('indirim_hedef_müşteri_ids.csv', index=False)