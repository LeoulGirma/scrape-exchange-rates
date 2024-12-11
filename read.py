import requests
from bs4 import BeautifulSoup
import logging

from CurrencyExchange import CurrencyExchange

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_html_and_extract_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    currency_data_list = []

    tables = soup.find_all('table', class_='table exhange_rate w-100 text-sm table-striped border rounded my-3 p-2')
    print(f"Total tables found: {len(tables)}")

    for table in tables:
        bank_name = table.find('th', colspan="10").find('h3').text.strip() if table.find('th', colspan="10") else 'Unknown Bank'
        last_updated = table.find('time').text if table.find('time') else 'Not specified'
        rows = table.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            cols = row.find_all('td')
            currency_exchange = CurrencyExchange(
                bank_name=bank_name,
                code=cols[0].text.strip() if len(cols) > 0 else None,
                name=cols[1].text.strip() if len(cols) > 1 else None,
                last_updated=last_updated,
                buying=cols[2].text.strip() if len(cols) > 2 else None,
                selling=cols[4].text.strip() if len(cols) > 4 else None,
                transaction_buying=cols[6].text.strip() if len(cols) > 6 else None,
                transaction_selling=cols[7].text.strip() if len(cols) > 7 else None
            )
            currency_data_list.append(currency_exchange)

    return currency_data_list

# Specify the path to your HTML file
filepath = 'tables.html'
data = read_html_and_extract_data(filepath)
for entry in data:
    print(entry)
