import requests
import csv
from datetime import datetime

url = 'https://www.cbr-xml-daily.ru/archive/2023/09/13/daily_json.js'
response = requests.get(url)
data = response.json()

today = datetime.now()

with open('dataset.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'USD', 'EUR'])
    writer.writerow([today, 
                     data['Valute']['USD']['Value']])