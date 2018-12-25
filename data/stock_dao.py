from abc import ABCMeta, abstractmethod


class IDataDao(metaclass=ABCMeta):

    @abstractmethod
    def save(self, stock_code, df):
        pass

    @abstractmethod
    def get(self, stock_code):
        pass


