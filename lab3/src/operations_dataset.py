import pandas as pd

from datetime import datetime

class DatasetOperations:
    def __init__(self, curr_dir):
        self.CURR_DIR = curr_dir

    def separation_date_by_data(self, df: pd.DataFrame) -> None:
        df_date = df['date']
        df_data = df.drop('date', axis=1)

        df_date.to_csv(self.CURR_DIR + '/csv/csv_date_by_data/X.csv', index=False)
        df_data.to_csv(self.CURR_DIR + '/csv/csv_date_by_data/Y.csv', index=False)

    def separation_by_years(self, df: pd.DataFrame) -> None:
        df['date'] = pd.to_datetime(df['date'])

        for year, group in df.groupby(df['date'].dt.year):
            start_date = group['date'].min().strftime('%Y%m%d')
            end_date = group['date'].max().strftime('%Y%m%d')
            filename = f'{start_date}_{end_date}.csv'
            group.to_csv(self.CURR_DIR + '/csv/csv_years/' + filename, index=False)

    def separation_by_weeks(self, df: pd.DataFrame) -> None:
        df['date'] = pd.to_datetime(df['date'])

        for (year, week), group in df.groupby([df['date'].dt.isocalendar().year, df['date'].dt.isocalendar().week]):
            start_date = group['date'].min().strftime('%Y%m%d')
            end_date = group['date'].max().strftime('%Y%m%d')
            filename = f'{start_date}_{end_date}.csv'
            group.to_csv(self.CURR_DIR + '/csv/csv_weeks/' + filename, index=False)
        
    def get_data_from_date(self, df: pd.DataFrame, date: datetime) -> None | pd.DataFrame:
        data = df[df['date'] == date]
        if data.empty:
            return None
        else:
            return data.drop(columns=['date'])

    def next(self, df: pd.DataFrame, index: int) -> None | tuple[str]:
        if index < len(df):
            return tuple(df.iloc[index])
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