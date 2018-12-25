import os
from data.stock_dao import IDataDao
from config import config


class CsvStockDao(IDataDao):

    def __init__(self) -> None:
        self.base_dir = config.configs['stock_data_dir']

    def __file_path(self, stock_code):
        return os.path.join(self.base_dir, stock_code + '.cvs')

    def save(self, stock_code, df):
        file_path = self.__file_path(stock_code)
        if os.path.exists(file_path):
            df.to_csv(file_path)
        else:
            df.to_csv(file_path, mode='a', header=None)

    def get(self, stock_code):
        pass



