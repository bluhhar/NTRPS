import currency_handler as cur_h
import images_handler as img_h

from dataset_handler import DatasetHandler
from directory_handler import DirectoryHandler as dir_h
from operations_dataset import DatasetOperations, DataIterator
from datetime import datetime

CURR_DIR = dir_h.set_current_dir()

IMAGES_FIELDS = ['date', 'file_name', 'url', 'path']
CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']
TEXT_FIELDS = ['date', ]
        
def test_images():
    handler = img_h.ImagesHandler(CURR_DIR)
    #handler.download_images('Иллидан Ярость Бури', 61, False)
    handler.download_images('Arthas Wrath of the Lich King', 61, True)

    #dat_h = DatasetHandler()
    #df = dat_h.create_dataset_from_files([CURR_DIR + '/datasets/images/Иллидан Ярость Бури_dataset.csv'], IMAGES_FIELDS)
    #print(df)
    #dat_h.rewrite_dates(df, datetime(2023, 1, 1))
    #print(df)

    #dataset_operations = DatasetOperations(CURR_DIR)
    #df = dat_h.create_dataset_from_files([CURR_DIR + '/datasets/images/test_weeks_dataset.csv'], IMAGES_FIELDS) #CURR_DIR + '/csv/brown bear_dataset.csv'
    #dataset_operations.separation_date_by_data(df)
    #dataset_operations.separation_by_years(df)
    #dataset_operations.separation_by_weeks(df)

    #print('---Получение данных по определенной дате---')
    #print(dataset_operations.get_data_from_date(df, datetime(2023, 1, 24)))

    #print('---Работа next()---')
    #for index in range(0, len(df)):
    #    print(dataset_operations.next(df, index))

    #print('---Работа итератора---')
    #iterator = DataIterator(df)
    #for item in iterator:
    #    print(item)

def test_currency():
    #handler = cur_h.CurrencyHandler(CURR_DIR)
    #handler.get_currency_dataset('USD', '01/01/1991', '31/12/2023') #USD

    dat_h = DatasetHandler()
    df = dat_h.create_dataset_from_files([CURR_DIR + '/datasets/currency/EUR_19910101_20231231.csv'], CURRENCY_FIELDS)

    dataset_operations = DatasetOperations(CURR_DIR)
    dataset_operations.separation_date_by_data(df)
    #dataset_operations.separation_by_years(df)
    #dataset_operations.separation_by_weeks(df)

    print('---Получение данных по определенной дате---')
    print(dataset_operations.get_data_from_date(df, datetime(2023, 1, 24)))

    #print('---Работа next()---')
    #for index in range(0, len(df)):
    #    print(dataset_operations.next(df, index))

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
    #test_images()
    test_currency()

if __name__ == '__main__':
    main()