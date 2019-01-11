"""
-*- coding: utf-8 -*-
@Author  : bigeyefish
@Time    : 2019/1/11 14:42
@describe: 指标计算接口
"""
from abc import ABCMeta, abstractmethod


class Indicator(metaclass=ABCMeta):

    @abstractmethod
    def get_required_col(self):
        pass

    @abstractmethod
    def calc(self, df):
        pass

    def validate_col(self, df):
        if not self.get_required_col().issubset(df.columns):
            print('计算振幅指标缺少相关列')
            return False
        return True
