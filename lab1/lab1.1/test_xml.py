import os
import requests
import csv
import xml.etree.ElementTree as ET

from datetime import datetime

#путь .py
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

def get_ids_of_currency() -> None:
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    if(response.status_code == 200):
        xml_page = ET.fromstring(response.content)
        
        data = []
        for tag in xml_page.findall('Valute'):
            id = tag.get('ID')
            num_code = tag.find('NumCode').text
            char_code = tag.find('CharCode').text
            currency_name = tag.find('Name').text
            
            data.append([id, num_code, char_code, currency_name])
        
        with open(CURR_DIR + f'\ids_currency.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['id', 'num_code', 'char_code', 'currency_name'])
            for row in data:
                csv_writer.writerow(row)

def write_dataset(name_currency:str, id_currency: str, start_date: str, end_date: str) -> None:
    url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={end_date}&VAL_NM_RQ={id_currency}"
    response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    #в отличии от json надо проверить всего лишь раз что страница существует, на ней и так будут все курсы валюты
    if(response.status_code == 200):
        xml_page = ET.fromstring(response.content)
        
        data = []
        for tag in xml_page.findall('Record'):
            date = datetime.strptime(tag.get('Date'), '%d.%m.%Y').strftime('%Y-%m-%d')
            nominal = tag.find('Nominal').text
            value = tag.find('Value').text.replace(',', '.')
            vunit_Rate = tag.find('VunitRate').text.replace(',', '.')
            
            data.append([date, nominal, value, vunit_Rate])
    
        start_date = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y%m%d')
        end_date= datetime.strptime(end_date, '%d/%m/%Y').strftime('%Y%m%d')
        with open(CURR_DIR + f'\{name_currency}_{start_date}_{end_date}.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['date', 'nominal', 'value', 'unitRate'])
            for row in data:
                csv_writer.writerow(row)
    else:
        print('Ошибка: Валюта или дата указаны неверно!')

def main():
    get_ids_of_currency()
    write_dataset('USD', 'R01235', '01/01/1991', '31/12/2023') #USD

if __name__ == '__main__':
    main()
