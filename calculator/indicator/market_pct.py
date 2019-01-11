"""
-*- coding: utf-8 -*-
@Author  : bigeyefish
@Time    : 2019/1/11 14:40
@describe: 大盘涨跌幅指标
"""
from calculator.indicator.indicator import Indicator


class MarketPct(Indicator):

    def get_required_col(self):
        return {}

    def calc(self, df, **kwargs):
        print(kwargs)
        print('.............')
        # histo_record['sz_pct_change'] = self.sh_index['pct_chg']
        return df

market_pct_calculator = MarketPct()
