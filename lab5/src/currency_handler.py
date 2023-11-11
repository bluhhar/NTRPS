import requests
import csv
import pandas as pd
import xml.etree.ElementTree as ET

from datetime import datetime

class CurrencyHandler:
    def __init__(self, curr_dir):
        self.CURR_DIR = curr_dir
        self.currency_ids = self.get_ids_of_currency()

    def get_currency_id(self, char_code: str) -> str:
        currency_id = self.currency_ids[self.currency_ids['char_code'] == char_code]['id'].values[0]
        return currency_id

    def get_ids_of_currency(self) -> pd.DataFrame:
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

            df = pd.DataFrame(data, columns=['id', 'num_code', 'char_code', 'currency_name'])
            return df

    def get_currency_dataset(self, name_currency:str, start_date: str, end_date: str) -> None:
        id_currency = self.get_currency_id(name_currency)
        if id_currency:
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
                with open(self.CURR_DIR + f'/datasets/currency/{name_currency}_{start_date}_{end_date}.csv', 'w', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(['date', 'nominal', 'value', 'vunitRate'])
                    for row in data:
                        csv_writer.writerow(row)
            else:
                print('Ошибка: Дата указана неверно!')
        else:
            print('Ошибка: Код валюты не найден!')