import requests
import csv
from datetime import datetime

url = 'https://www.cbr-xml-daily.ru/latest.js'
response = requests.get(url)
data = response.json()

today = datetime.now().strftime('%Y-%m-%d')

with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'USD', 'EUR'])
    writer.writerow([today, 
                     data['rates']['USD'], 
                     data['rates']['EUR']])