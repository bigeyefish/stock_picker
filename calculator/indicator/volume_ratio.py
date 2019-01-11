"""
-*- coding: utf-8 -*-
@Author  : bigeyefish
@Time    : 2019/1/11 14:40
@File    : amplitude.py
@describe: 量比指标
"""
from calculator.indicator.indicator import Indicator


class VolumeRatio(Indicator):

    def get_required_col(self):
        return {'vol'}

    def calc(self, df):
        if self.validate_col(df):
            return df.assign(vol_ratio=df['vol'].div(df[::-1]['vol'].rolling(5).mean().shift(1)))
        return df

volume_ratio_calculator = VolumeRatio()
