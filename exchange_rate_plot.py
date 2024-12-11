# import matplotlib.pyplot as plt
# import pandas as pd
# import json

# # Load the JSON data from a file
# with open('exchange_rates.json') as file:
#     data = json.load(file)

# df = pd.DataFrame(data)

# # Normalize bank names by removing unnecessary suffixes and standardizing case
# df['bank_name'] = df['bank_name'].str.strip().str.lower().str.replace(' exchange rate', '', regex=False)

# # Aggregate data by taking the mean of duplicates
# df = df.groupby(['code', 'bank_name']).agg({
#     'buying': 'mean',  # Adjust this if you want to use a different aggregation method
#     'last_updated': 'max'  # Assumes you might want the most recent update
# }).reset_index()

# # Pivot data for better visualization
# pivot_df = df.pivot(index='code', columns='bank_name', values='buying')

# # Plotting
# fig, ax = plt.subplots(figsize=(20, 10))
# pivot_df.plot(kind='bar', ax=ax)
# plt.title('Buying Rates of Different Currencies Across Banks')
# plt.xlabel('Currency')
# plt.ylabel('Buying Rate')
# plt.xticks(rotation=90)  # Rotate for better readability
# plt.yticks(fontsize=12)
# plt.legend(title='Bank Name', fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()  # Adjust layout to make room for the legend
# plt.show()

import matplotlib.pyplot as plt
import pandas as pd
import json

# Load the JSON data from a file
with open('exchange_rates.json') as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Aggregate data by taking the mean of duplicates
df = df.groupby(['code', 'bank_name']).agg({
    'buying': 'mean',  # Adjust this if you want to use a different aggregation method
    'last_updated': 'max'  # Assumes you might want the most recent update
}).reset_index()

# Pivot data for better visualization
pivot_df = df.pivot(index='code', columns='bank_name', values='buying')

# Plotting
ax = pivot_df.plot(kind='bar', figsize=(12, 6))
plt.title('Buying Rates of Different Currencies Across Banks')
plt.xlabel('Currency')
plt.ylabel('Buying Rate')
plt.xticks(rotation=0)
plt.legend(title='Bank Name', fontsize=10, labelspacing=1.5)
plt.show()
