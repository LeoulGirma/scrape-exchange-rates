import json
import logging
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CurrencyExchange:
    def __init__(self, bank_name, code, name, last_updated, buying=None, selling=None, transaction_buying=None, transaction_selling=None):
        self.bank_name = bank_name
        self.code = code
        self.name = name
        self.last_updated = last_updated
        self.buying = buying
        self.selling = selling
        self.transaction_buying = transaction_buying
        self.transaction_selling = transaction_selling

    def to_dict(self):
        return {
            "bank_name": self.bank_name,
            "code": self.code,
            "name": self.name,
            "last_updated": self.last_updated,
            "buying": self.buying,
            "selling": self.selling,
            "transaction_buying": self.transaction_buying,
            "transaction_selling": self.transaction_selling
        }

class CurrencyScraper:
    def __init__(self, url):
        self.url = url
        # List of user agents for rotation to simulate requests from different browsers
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
        ]

    def fetch_data(self):
        headers = {'User-Agent': random.choice(self.user_agents)}
        try:
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()  # Raises a HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        currency_data_list = []
                                             #  table exhange_rate w-100 text-sm table-striped rounded my-3 p-2                          
        tables = soup.find_all('table', class_='table exhange_rate w-100 text-sm table-striped rounded my-3 p-2')
        logging.info(f"Total tables found: {len(tables)}")

        for table in tables:
            bank_name = table.find('th', colspan="10").find('h3').text.strip() if table.find('th', colspan="10") else 'Unknown Bank'
            rows = table.find_all('tr')[1:]  # Skip the header row
            last_updated_text = table.find('time').text if table.find('time') else 'Not specified'

             # Only attempt to convert date if it's not 'Not specified'
            if last_updated_text != 'Not specified':
                try:
                    date_obj = datetime.strptime(last_updated_text, "%a, %d %B, %Y")
                    last_updated = date_obj.strftime("%Y-%m-%d")
                except ValueError as e:
                    print(f"Date conversion error: {e}")
                    last_updated = 'Conversion Error'
            else:
                last_updated = ''
            
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
                currency_data_list.append(currency_exchange.to_dict())

        return currency_data_list

    def run(self):
        html = self.fetch_data()
        if html:
            data = self.parse_html(html)
            logging.info("Data scraping and parsing completed successfully.")
            return data
            # print(json.dumps(data, indent=4))  # Print formatted JSON
        else:
            logging.info("Failed to retrieve data.")
            return "Failed to retrieve data."

# Usage
# url = 'https://banksethiopia.com/ethiopian-birr-exchange-rate/'
# scraper = CurrencyScraper(url)
# scraper.run()
