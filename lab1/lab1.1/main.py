import os
import requests
import csv
from datetime import datetime, timedelta

#путь .py
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

def write_dataset(start_date = datetime(2023, 9, 10), end_date = datetime.now()):
    with open(CURR_DIR + '\dataset.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'USD'])

        current_date = start_date
        while current_date <= end_date:
            url = f'https://www.cbr-xml-daily.ru/archive/{current_date.year}/{current_date.strftime("%m")}/{current_date.strftime("%d")}/daily_json.js'
            
            response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
            if(response.status_code == 200):
                data = response.json()
                today = current_date.strftime('%Y-%m-%d')
                writer.writerow([today, data['Valute']['USD']['Value']])
            
            current_date += timedelta(days=1)

def read_dataset():
    csv_file_path = CURR_DIR + '\dataset.csv'

    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            print(row)

def main():
    write_dataset(start_date = datetime(2023, 8, 30), end_date = datetime.now())
    read_dataset()

if __name__ == "__main__":
    main()