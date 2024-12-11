import requests
from bs4 import BeautifulSoup
import logging
import random
from CurrencyExchange import CurrencyExchange


# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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

    def run(self):
        html = self.fetch_data()
        if html:
            data = self.parse_html(html)
            logging.info("Data scraping and parsing completed successfully.")
            print(data)
        else:
            logging.info("Failed to retrieve data.")

# Usage
url = 'https://banksethiopia.com/ethiopian-birr-exchange-rate/'  # Replace with the actual URL you are scraping
scraper = CurrencyScraper(url)
scraper.run()
