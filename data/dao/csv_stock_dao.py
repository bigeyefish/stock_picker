import os

from config import config
from data.dao.stock_dao import IDataDao


class CsvStockDao(IDataDao):

    def __init__(self) -> None:
        self.base_dir = config.configs['stock_data_dir']
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def __file_path(self, stock_code):
        return os.path.join(self.base_dir, stock_code + '.csv')

    def save(self, stock_code, df):
        file_path = self.__file_path(stock_code)
        if not os.path.exists(file_path):
            df.to_csv(file_path)
        else:
            df.to_csv(file_path, mode='a', header=None)

    def get(self, stock_code):
        pass



