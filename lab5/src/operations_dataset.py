import pandas as pd
import io
import matplotlib.pyplot as plt

from datetime import datetime

class DatasetOperations:
    """
    Класс предназначен для выполнения различных операций с датасетами.

    Атрибуты
    -----------
    CURR_DIR : str
        Текущий рабочий каталог.

    Методы
    -------
    __init__(self, curr_dir: str)
        Инициализирует объект класса DatasetOperations.
    """
    def __init__(self, curr_dir):
        self.CURR_DIR = curr_dir

    def separation_date_by_data(self, df: pd.DataFrame) -> None:
        df_date = pd.to_datetime(df['date'])
        df_data = df.drop('date', axis = 1)

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
    
    def info_of_dataset(self, df: pd.DataFrame) -> str:
        buf = io.StringIO()
        df.info(buf=buf)
        return buf.getvalue()
    
    def rename_columns(self, s: str) -> str:
        return ''.join(['_' + i.lower() if i.isupper() else i for i in s]).lstrip('_')
    
    def check_null_fields(self, df: pd.DataFrame) -> str:
        return str(df.isnull().sum())
    
    def fill_null_fieds(self, df: pd.DataFrame) -> None:
        df.ffill(inplace=True)
        df.bfill(inplace=True)

    def add_median_mean(self, df: pd.DataFrame) -> None:
        median_value = df['vunit_rate'].median()
        mean_value = df['vunit_rate'].mean()

        df['deviation_from_median'] = df['vunit_rate'] - median_value
        df['deviation_from_mean'] = df['vunit_rate'] - mean_value

    def describe_dataset(self, df: pd.DataFrame) -> str:
        return str(df[['vunit_rate', 'deviation_from_median', 'deviation_from_mean']].describe())
    
    def show_deviation_graph(self, df: pd.DataFrame) -> None:
        plt.figure(figsize=(12, 6))
        plt.boxplot([df['vunit_rate'], df['deviation_from_median'], df['deviation_from_mean']], labels=['vunit_rate', 'deviation_from_median', 'deviation_from_mean'])
        plt.title('График vunit_rate и отклонений')
        plt.show()

    def show_date_graph(self, df: pd.DataFrame) -> None:
        df['date'] = pd.to_datetime(df['date'])

        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['vunit_rate'])

        plt.title('Изменение курса за весь период')
        plt.xlabel('Дата')
        plt.ylabel('Курс')

        plt.show()
    
    def plot_rate(self, df: pd.DataFrame, title: str) -> None:
        median_value = df['vunit_rate'].median()
        mean_value = df['vunit_rate'].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['vunit_rate'], label='Курс')
        plt.axhline(median_value, color='r', linestyle='--', label='Медиана')
        plt.axhline(mean_value, color='g', linestyle=':', label='Среднее значение')

        plt.title(title)
        plt.xlabel('Дата')
        plt.ylabel('Курс')
        plt.legend()

        plt.show()

    def plot_rate_month(self, df: pd.DataFrame, month: int) -> None:
        df_month = df[df['date'].dt.month == month]
        self.plot_rate(df_month, f'Изменение курса за {month} месяц')

    def plot_rate_year(self, df: pd.DataFrame, year: int) -> None:
        df_year = df[df['date'].dt.year == year]
        self.plot_rate(df_year, f'Изменение курса за {year} год')

    def plot_rate_year_month(self, df: pd.DataFrame, year: int, month: int) -> None:
        df_year_month = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]
        self.plot_rate(df_year_month, f'Изменение курса за {month} месяц в {year} год')
    
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