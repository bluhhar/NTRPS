import os
import pandas as pd

from datetime import datetime

class DatasetHandler:
    def check_dataset(self, df: pd.DataFrame, required_fields: list) -> bool:
        for field in required_fields:
            if field not in df.columns:
                return False
        return True

    def create_dataset_from_files(self, files: list, fields: list) -> pd.DataFrame:
        df = pd.DataFrame()
        for file in files:
            data = pd.read_csv(file)
            if self.check_dataset(data, fields):
                data['date'] = pd.to_datetime(data['date'])
                df = df._append(data, ignore_index=True)
            else:
                raise Exception(f'Ошибка: Файл {file} не содержит необходимых полей')
                #print(f'Ошибка: Файл {file} не содержит необходимых полей')
        return df
    
    def create_dataset(self, files: list) -> pd.DataFrame:
        df = pd.DataFrame()
        for file in files:
            data = pd.read_csv(file)
            data['date'] = pd.to_datetime(data['date'])
            df = df._append(data, ignore_index=True)
        return df

    def rewrite_dates(self, df: pd.DataFrame, start_date: datetime) -> pd.DataFrame:
        df['date'] = [start_date + pd.DateOffset(days=i) for i in range(len(df))]
        return df

    def save_new_dataset(self, df: pd.DataFrame, file_to_save: str, index_custom: bool = False) -> None:
        df.to_csv(file_to_save, index=index_custom)

    def merge_data_with_date(self, file_csv_x: str = 'X.csv', file_csv_y: str = 'Y.csv') -> pd.DataFrame:
        if not os.path.exists(file_csv_x) or not os.path.exists(file_csv_y):
            #return 'Ошибка: файла не существуют'
            raise Exception('Ошибка: файла не существуют')

        df_x = pd.read_csv(file_csv_x)
        df_y = pd.read_csv(file_csv_y)

        if 'date' not in df_x.columns or df_x.shape[1] != 1:
            #return 'Ошибка: Файл X.csv не содержит поле date'
            raise Exception('Ошибка: Файл X.csv не содержит поле date')


        merged_df = pd.merge(df_x, df_y, on='date', how='inner')

        return merged_df