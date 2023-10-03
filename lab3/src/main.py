import os
import requests
import re
import csv
import pandas as pd
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from datetime import datetime

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGES_FIELDS = ['date', 'file_name', 'url']
CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']
TEXT_FIELDS = ['date', ]

def check_repository(dir: str, name: str) -> None:
    dataset_directory = os.path.join(dir, name)
    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory)
    return dataset_directory

def write_csv_file(path: str, data: list) -> None:
    mode = 'w' if not os.path.exists(path) else 'a'
    with open(path, mode, newline='') as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerow(data)

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

        with open(CURR_DIR + f'/datasets/currency/ids_currency.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['id', 'num_code', 'char_code', 'currency_name'])
            for row in data:
                csv_writer.writerow(row)

def get_currency_id(file_path: str, char_code: str) -> str:
    df = pd.read_csv(file_path)
    currency_id = df[df['char_code'] == char_code]['id'].values[0]
    return currency_id

def write_currency_dataset(name_currency:str, start_date: str, end_date: str) -> None:
    id_currency = get_currency_id(CURR_DIR + '/datasets/currency/ids_currency.csv', name_currency)
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
            with open(CURR_DIR + f'/datasets/currency/{name_currency}_{start_date}_{end_date}.csv', 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['date', 'nominal', 'value', 'vunitRate'])
                for row in data:
                    csv_writer.writerow(row)
        else:
            print('Ошибка: Дата указана неверно!')
    else:
        print('Ошибка: Код валюты не найден!')

def parser_url(url: str) -> str:
    pattern = r'img_url=([^&]+)&text='
    match = re.search(pattern, url)

    if match:
        img_url_encoded = match.group(1)
        img_url_decoded = img_url_encoded.replace('%2F', '/').replace('%3A', ':')
        return img_url_decoded
    else:
        print('Ошибка: Ссылка после img_url не найдена в URL')

def calc_pages(num_images: int) -> int:
    return num_images // 30 + (num_images % 30 > 0) if num_images > 30 else 1

def get_html_tags(mini_images: bool) -> tuple[str, str, str]:
    if mini_images:
        return 'img', 'serp-item__thumb', 'src'
    else:
        return 'a', 'serp-item__link', 'href'

def download_image(url: str, save_path: str) -> bool:
    try:
        response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, stream=True)
        if(response.status_code == 200):
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
        else:
            print(f'Ошибка: Не удалось загрузить изображение: {url}')
            return False
    except Exception as e:
        print(f'Ошибка при загрузке изображения: {url}')
        return False
    
def download_images(query: str, num_images: int, mini_images: bool = False) -> None:
    pages = calc_pages(num_images)
    class_folder = check_repository(CURR_DIR, f'datasets/images/{query}')

    downloaded_count = 0

    base_url = 'https:'

    csv_file_path = CURR_DIR + '/datasets/images/' + f'{query}_dataset.csv'
    write_csv_file(csv_file_path, IMAGES_FIELDS)
    tag, tag_class, tag_source = get_html_tags(mini_images)
    #а вот это чтобы без движков было, грузим странички
    for page in range(0, pages):
        search_url = f'https://yandex.ru/images/search?text={query}&p={page}'

        #сделал с with для автоматического закрытия соединения
        with requests.get(search_url, headers={'User-Agent':'Mozilla/5.0'}) as response:
            soup = BeautifulSoup(response.text, 'html.parser')

            for a in soup.find_all(tag, class_=tag_class):
                img_url = a[tag_source]
                # получаем полный URL изображения
                if mini_images and not img_url.startswith('http'):
                    img_url = base_url + img_url
                elif img_url.startswith('/images'):
                    img_url = parser_url(img_url)

                #csv_image_filename = image_filename
                image_filename = f'{downloaded_count:04d}.jpg'
                image_path = os.path.join(class_folder, image_filename)
                if(download_image(img_url, image_path)):
                    downloaded_count += 1
                    print(f'Загружено изображений для {query}: {downloaded_count}/{num_images}')

                    write_csv_file(csv_file_path, [datetime.now().strftime('%Y-%m-%d'), image_filename, img_url])

                if(downloaded_count >= num_images):
                    break

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
        #FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
        #df = df.append(data, ignore_index=True) --> менять на df = df.append(data)
        #df = pd.concat(df_list, ignore_index=True) добавлять в данную строчку (просто раскомменитить)
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
    #download_images('grey bear', 10, False)
    #download_images('blue bear', 1, True)

    #df = create_dataset_from_files([CURR_DIR + '/datasets/images/black bear_dataset.csv'], IMAGES_FIELDS)
    #print(df)
    #rewrite_dates(df, datetime(2023, 1, 1))
    #print(df)

    df = create_dataset_from_files([CURR_DIR + '/datasets/images/test_weeks_dataset.csv'], IMAGES_FIELDS) #CURR_DIR + '/csv/brown bear_dataset.csv'
    #separation_date_by_data(df)
    #separation_by_years(df)
    #separation_by_weeks(df)

    #print('---Получение данных по определенной дате---')
    #print(get_data_from_date(df, datetime(2023, 1, 24)))

    print('---Работа next()---')
    for index in range(0, len(df)):
        print(next(df, index))

    print('---Работа итератора---')
    iterator = DataIterator(df)
    for item in iterator:
        print(item)

def test_currency():
    get_ids_of_currency()
    write_currency_dataset('EUR', '01/01/1991', '31/12/2023') #USD

    df = create_dataset_from_files([CURR_DIR + '/datasets/currency/EUR_19910101_20231231.csv'], CURRENCY_FIELDS)
    separation_date_by_data(df)
    separation_by_years(df)
    separation_by_weeks(df)

    print('---Получение данных по определенной дате---')
    print(get_data_from_date(df, datetime(2023, 1, 24)))

    print('---Работа next()---')
    for index in range(0, len(df)):
        print(next(df, index))

    print('---Работа итератора---')
    iterator = DataIterator(df)
    for item in iterator:
        print(item)

def check_repos():
    check_repository(CURR_DIR, 'datasets')
    check_repository(CURR_DIR, 'csv')
    check_repository(CURR_DIR, 'csv/csv_date_by_data')
    check_repository(CURR_DIR, 'csv/csv_years')
    check_repository(CURR_DIR, 'csv/csv_weeks')
    check_repository(CURR_DIR, 'datasets/images')
    check_repository(CURR_DIR, 'datasets/currency')

    #csv_files = print_csv_files_in_dir([CURR_DIR + '/datasets/images', CURR_DIR + '/datasets/currency'])
    #for file in csv_files:
    #  print(file)

    #print_csv_dir_tree(CURR_DIR + '/datasets')

def main():
    #check_repos()
    #test_images()
    test_currency()

if __name__ == '__main__':
    main()