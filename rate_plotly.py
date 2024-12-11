import plotly.express as px
import pandas as pd
import json

# Load and prepare data as before
with open('exchange_rates.json') as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Normalize and aggregate data
df['bank_name'] = df['bank_name'].str.strip().str.lower().replace({'exchange rate': '', ' bank': ''}, regex=True).str.title()
df = df.groupby(['code', 'bank_name']).agg({'buying': 'mean'}).reset_index()

# Sort and remove duplicates
df = df.drop_duplicates(subset=['code', 'bank_name'])

# Create an interactive bar chart
fig = px.bar(df, x='code', y='buying', color='bank_name', title='Buying Rates of Different Currencies Across Banks',
             labels={'buying': 'Buying Rate', 'code': 'Currency'},
             hover_data={'bank_name': True})

# Update layout and add checkboxes for multiple selections
fig.update_layout(
    updatemenus=[
        dict(
            type='dropdown',
            direction='down',
            active=0,
            buttons=list([
                dict(label='All Banks', method='update',
                     args=[{'visible': [True] * len(df)}],
                     ),
                *[dict(label=bank, method='update',
                       args=[{'visible': [df['bank_name'].eq(bank).tolist()]}])
                  for bank in sorted(df['bank_name'].unique())]
            ]),
            x=0.95,  # Moves it towards the right end of the graph
            xanchor='right',  # Anchors it by the right edge
            y=1.15,
            yanchor='top'
        ),
        dict(
            type='dropdown',
            direction='down',
            active=0,
            buttons=list([
                dict(label='All Currencies', method='update',
                     args=[{'visible': [True] * len(df)}],
                     ),
                *[dict(label=currency, method='update',
                       args=[{'visible': [df['code'].eq(currency).tolist()]}])
                  for currency in sorted(df['code'].unique())]
            ]),
            x=0.95,  # Consistent positioning for both dropdowns
            xanchor='right',  # Anchors it by the right edge
            y=1.05,  # Adjust vertical spacing between dropdowns
            yanchor='top'
        )
    ]
)

fig.show()
