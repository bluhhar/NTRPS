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
                print(f'Ошибка: Файл {file} не содержит необходимых полей')
        return df

    def rewrite_dates(self, df: pd.DataFrame, start_date: datetime) -> pd.DataFrame:
        df['date'] = [start_date + pd.DateOffset(days=i) for i in range(len(df))]
        return df

    def save_new_dataset(self, df: pd.DataFrame, file_to_save: str, index_custom: bool = False) -> None:
        df.to_csv(file_to_save, index=index_custom)