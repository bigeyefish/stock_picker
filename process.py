import tushare as ts
import pandas as pd
from pandas import DataFrame
import datetime
import time
from util.const import Const
from util.redis_conn import redisUtil
from config.config import configs

class Process:

    def __init__(self) -> None:
        self.start_date = (datetime.date.today() - datetime.timedelta(days=configs['init_stock_days'])).strftime('%Y%m%d')
        ts.set_token('e9002771412a9735ddc9d24529386ef4e2b9c4adf80751cd60c27829')
        self.pro = ts.pro_api()
        self.sh_index = None

    def run(self, stock_dao):

        # 查询沪深所有股票
        stock_list = self.pro.stock_basic(list_status='L')
        for ts_code in stock_list['ts_code']:
            last_update = redisUtil.r.zscore(Const.KEY_STOCK_UPDATE.value, ts_code)
            if not last_update:
                result = self.__get_multi_data(ts_code)
                if result:
                    stock_dao.save(stock_dao, result)
                    redisUtil.r.zadd(Const.KEY_STOCK_UPDATE.value, stock_dao, int(self.start_date))
                time.sleep(0.1)

    def __get_multi_data(self, ts_code):
        print('get stock [%s] data after %s' % (ts_code, self.start_date))
        try:
            # 获取大盘数据
            if not self.sh_index:
                self.sh_index = self.pro.index_daily(ts_code='000001.SH', start_date=self.start_date, end_date='').set_index('trade_date')

            # 获取股票历史行情
            histo_record = ts.pro_bar(ts_code, pro_api=self.pro, start_date=self.start_date, end_date='', ma=[5, 10, 20], adj='qfq')
            # 计算量比
            histo_record = histo_record.assign(
                volume_ratio=histo_record['vol'].div(histo_record[::-1]['vol'].rolling(5).mean().shift(1)))
            # 计算振幅
            histo_record['amplitude'] = (histo_record['high'] - histo_record['low']).div(histo_record['pre_close']) * 100
            # 叠加大盘
            histo_record['sz_pct_change'] = self.sh_index['pct_chg']
            return histo_record

        #     try:
        #         last_ten = histo_record.head(10)
        #         last_five = histo_record.head(5)
        #         # 缩量、小振幅、多头 数量 、连续缩量下跌
        #         less_volume = last_ten[
        #             (last_ten['volume_ratio'] < 1) | (last_ten['sz_pct_change'] > 2) | (last_ten['sz_pct_change'] < -2)]
        #         less_amplitude = last_ten[(last_ten['amplitude'] < 3)]
        #         long_position = last_ten[(last_ten['ma5'] > last_ten['ma10']) & (last_ten['ma10'] > last_ten['ma20'])]
        #         less_volume_fall = last_five[
        #             (last_five['vol'] < last_five.shift(-1)['vol']) & (last_five['close'] <= last_five['pre_close'])]
        #
        #         # 过滤掉一些不符合条件的
        #         # 5天内有振幅超过5的不要，小振幅或者缩量的天数小于6的不要
        #         # 5天最高价格和最低价格相减不超过3%
        #         price_rate = (last_five['high'].max() - last_five['low'].min()) / last_five['low'].min()
        #         if len(last_five[last_five['amplitude'] > 5]) or len(less_volume) < 6 or len(
        #                 less_amplitude) < 6 or price_rate > 3:
        #             continue
        #
        #         result[ts_code] = [len(less_volume), len(less_amplitude), len(long_position), len(less_volume_fall)]
        #         time.sleep(0.01)
        #         if len(result) % 100 == 0:
        #             print('has analysed %d' % len(result))
        #
        #         if test_count and len(result) == test_count:
        #             break;
        #
        except Exception as e:
            print(e)
            return None


