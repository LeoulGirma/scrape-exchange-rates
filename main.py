# main.py

import sqlite3
from currency_scraper import CurrencyScraper  # Assuming your scraping class is in currency_scraper.py
from datetime import datetime, timedelta

# Import the database setup function
from db_setup import create_database

# conn = sqlite3.connect('currency_exchange.db')
def save_data_to_database(data, conn):
    c = conn.cursor()
    # print(data)
    # Insert data into the database
    for item in data:
        # print(item)
        c.execute('''
            INSERT INTO currency_data (bank_name, code, name, last_updated, buying, selling, transaction_buying, transaction_selling)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item['bank_name'], item['code'], item['name'], item['last_updated'], item['buying'], item['selling'], item['transaction_buying'], item['transaction_selling']))

    conn.commit()
    print("Data saved to database successfully.")
    # conn.close()

def read_and_print_data(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM currency_data"
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        print("Data retrieved from the database:")
        for row in records:
            print(row)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_latest_update_date(conn):
    """Retrieve the most recent update date from the database."""
    cursor = conn.cursor()
    query = "SELECT MAX(last_updated) FROM currency_data"
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result[0]:
            # Since the dates are stored as 'YYYY-MM-DD', no conversion is necessary if you just want the date string
            return datetime.strptime(result[0], "%Y-%m-%d").date()
        return None
    except Exception as e:
        print(f"An error occurred while fetching the latest update date: {e}")
        return None

def main():
    conn = sqlite3.connect('currency_exchange.db')
    # Ensure the database is set up
    create_database()

    latest_date = get_latest_update_date(conn)
    print(latest_date)
    today = datetime.now().date()

    if latest_date and latest_date >= today:
        print("Data is up-to-date. No need to scrape today.")
        return

    # URL to scrape
    url = 'https://banksethiopia.com/ethiopian-birr-exchange-rate/'
    scraper = CurrencyScraper(url)
    data = scraper.run()

    if data:
        save_data_to_database(data,conn)

    # Now read and print to confirm it's all saved correctly
    # read_and_print_data(conn)

    conn.close()


    
if __name__ == "__main__":
    main()
