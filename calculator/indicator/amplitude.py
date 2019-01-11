"""
-*- coding: utf-8 -*-
@Author  : bigeyefish
@Time    : 2019/1/11 14:40
@File    : amplitude.py
@describe: 振幅指标
"""
from calculator.indicator.indicator import Indicator


class Amplitude(Indicator):

    def get_required_col(self):
        return {'high', 'low', 'pre_close'}

    def calc(self, df):
        if self.validate_col(df):
            df['amplitude'] = (df['high'] - df['low']).div(df['pre_close']) * 100
        return df
amplitude_calculator = Amplitude()
