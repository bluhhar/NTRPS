import os
import requests
import re
import csv
import pandas as pd
import xml.etree.ElementTree as ET

import currency_handler as cur_h
import directory_handler as dir_h
import dataset_handler as dat_h
import images_handler as img_h

from bs4 import BeautifulSoup
from datetime import datetime

CURR_DIR = dir_h.set_current_dir()

IMAGES_FIELDS = ['date', 'file_name', 'url']
CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']
TEXT_FIELDS = ['date', ]

def merge_data_with_date(file_csv_x: str = 'X.csv', file_csv_y: str = 'Y.csv') -> pd.DataFrame:
    if not os.path.exists(file_csv_x) or not os.path.exists(file_csv_y):
        return 'Ошибка: файла не существуют'

    df_x = pd.read_csv(file_csv_x)
    df_y = pd.read_csv(file_csv_y)

    if 'date' not in df_x.columns or df_x.shape[1] != 1:
        return 'Ошибка: Файл X.csv не содержит поле date'

    merged_df = pd.merge(df_x, df_y, on='date', how='inner')

    return merged_df

def check_dataset(df: pd.DataFrame, required_fields: list) -> bool:
    for field in required_fields:
        if field not in df.columns:
            return False
    return True

def create_dataset_from_files(files: list, fields: list) -> pd.DataFrame:
    df = pd.DataFrame()
    for file in files:
        data = pd.read_csv(file)
        if check_dataset(data, fields):
            data['date'] = pd.to_datetime(data['date'])
            df = df._append(data, ignore_index=True)
        else:
            print(f'Ошибка: Файл {file} не содержит необходимых полей')
    return df

def rewrite_dates(df: pd.DataFrame, start_date: datetime) -> pd.DataFrame:
    df['date'] = [start_date + pd.DateOffset(days=i) for i in range(len(df))]
    return df

def save_new_dataset(df: pd.DataFrame, file_to_save: str, index_custom: bool = False) -> None:
    df.to_csv(file_to_save, index=index_custom)

def print_csv_dir_tree(dir: str, file_extension: str = '.csv', tab: str = '') -> None:
    print(tab + os.path.basename(dir) + '/')
    tab += '    '
    for path in sorted(os.listdir(dir)):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path) and full_path.endswith(file_extension):
            print(tab + os.path.basename(full_path))
        elif os.path.isdir(full_path):
            print_csv_dir_tree(full_path, file_extension, tab)

def separation_date_by_data(df: pd.DataFrame) -> None:
    df_date = df['date']
    df_data = df.drop('date', axis=1)

    df_date.to_csv(CURR_DIR + '/csv/csv_date_by_data/X.csv', index=False)
    df_data.to_csv(CURR_DIR + '/csv/csv_date_by_data/Y.csv', index=False)

def separation_by_years(df: pd.DataFrame) -> None:
    df['date'] = pd.to_datetime(df['date'])

    for year, group in df.groupby(df['date'].dt.year):
        start_date = group['date'].min().strftime('%Y%m%d')
        end_date = group['date'].max().strftime('%Y%m%d')
        filename = f'{start_date}_{end_date}.csv'
        group.to_csv(CURR_DIR + '/csv/csv_years/' + filename, index=False)

def separation_by_weeks(df: pd.DataFrame) -> None:
    df['date'] = pd.to_datetime(df['date'])

    for (year, week), group in df.groupby([df['date'].dt.isocalendar().year, df['date'].dt.isocalendar().week]):
        start_date = group['date'].min().strftime('%Y%m%d')
        end_date = group['date'].max().strftime('%Y%m%d')
        filename = f'{start_date}_{end_date}.csv'
        group.to_csv(CURR_DIR + '/csv/csv_weeks/' + filename, index=False)
    
def get_data_from_date(df: pd.DataFrame, date: datetime) -> None | pd.DataFrame:
    data = df[df['date'] == date]
    if data.empty:
        return None
    else:
        return data.drop(columns=['date'])

def next(df: pd.DataFrame, index: int) -> None | tuple[str]:
    if index < len(df):
        #return tuple(df.loc[index, ['date', 'file_name', 'url']]) #возвращает строки по меткам
        return tuple(df.iloc[index]) #возвращает строки по целочисленным значениям
    return None

class DataIterator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.df):
            result = tuple(self.df.iloc[self.counter])
            self.counter += 1
            return result
        else:
            raise StopIteration
        
def test_images():
    handler = img_h.ImagesHandler(CURR_DIR)
    handler.download_images('grey bear', 10, False)
    handler.download_images('blue bear', 1, True)

    #df = create_dataset_from_files([CURR_DIR + '/datasets/images/black bear_dataset.csv'], IMAGES_FIELDS)
    #print(df)
    #rewrite_dates(df, datetime(2023, 1, 1))
    #print(df)

    #df = create_dataset_from_files([CURR_DIR + '/datasets/images/test_weeks_dataset.csv'], IMAGES_FIELDS) #CURR_DIR + '/csv/brown bear_dataset.csv'
    #separation_date_by_data(df)
    #separation_by_years(df)
    #separation_by_weeks(df)

    #print('---Получение данных по определенной дате---')
    #print(get_data_from_date(df, datetime(2023, 1, 24)))

    #print('---Работа next()---')
    #for index in range(0, len(df)):
    #    print(next(df, index))

    #print('---Работа итератора---')
    #iterator = DataIterator(df)
    #for item in iterator:
    #    print(item)

def test_currency():
    handler = cur_h.CurrencyHandler(CURR_DIR)
    handler.get_currency_dataset('EUR', '01/01/1991', '31/12/2023') #USD

    #df = create_dataset_from_files([CURR_DIR + '/datasets/currency/EUR_19910101_20231231.csv'], CURRENCY_FIELDS)
    #separation_date_by_data(df)
    #separation_by_years(df)
    #separation_by_weeks(df)

    #print('---Получение данных по определенной дате---')
    #print(get_data_from_date(df, datetime(2023, 1, 24)))

    #print('---Работа next()---')
    #for index in range(0, len(df)):
    #    print(next(df, index))

    #print('---Работа итератора---')
    #iterator = DataIterator(df)
    #for item in iterator:
    #    print(item)

def check_repos():
    dir_h.check_repository(CURR_DIR, 'datasets')
    dir_h.check_repository(CURR_DIR, 'csv')
    dir_h.check_repository(CURR_DIR, 'csv/csv_date_by_data')
    dir_h.check_repository(CURR_DIR, 'csv/csv_years')
    dir_h.check_repository(CURR_DIR, 'csv/csv_weeks')
    dir_h.check_repository(CURR_DIR, 'datasets/images')
    dir_h.check_repository(CURR_DIR, 'datasets/currency')

    #csv_files = print_csv_files_in_dir([CURR_DIR + '/datasets/images', CURR_DIR + '/datasets/currency'])
    #for file in csv_files:
    #  print(file)

    #print_csv_dir_tree(CURR_DIR + '/datasets')

def main():
    check_repos()
    test_images()
    #test_currency()

if __name__ == '__main__':
    main()