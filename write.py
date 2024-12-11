import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def save_html(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f'HTML file saved as {filename}')

def scrape_to_file(url, output_file):
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    table_html = "<html><head><title>Scraped Tables</title></head><body>"
    divs = soup.find_all('div', class_='px-2 border rounded my-3')
    for div in divs:
        tables = div.find_all('table')
        for table in tables:
            table_html += str(table)
    table_html += "</body></html>"
    save_html(table_html, output_file)

# Example usage
url = "https://banksethiopia.com/ethiopian-birr-exchange-rate/"
output_file = 'tables.html'
scrape_to_file(url, output_file)
