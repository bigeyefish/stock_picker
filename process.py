from pandas import DataFrame
import pandas as pd
import time

from calculator.indicator.amplitude import amplitude_calculator
from calculator.indicator.market_pct import market_pct_calculator
from util.const import Const
from util.redis_conn import redisUtil
from data.fetcher import fetch


class Process:

    def run(self, stock_dao):
        stock_last_update = redisUtil.r.zrange(Const.KEY_STOCK_UPDATE.value, 0, -1, withscores=True)
        stock_update_dict = dict(stock_last_update)
        # 判断数据是否需要更新
        # 查询沪深所有股票
        stock_list = fetch.get_stock_list()
        for ts_code in stock_list['ts_code']:
            print(ts_code)
            if ts_code not in stock_update_dict:
                result = fetch.get_multi_data(ts_code)
                # 叠加指标
                result = amplitude_calculator.calc(result)
                result = market_pct_calculator.calc(result, market=ts_code.split('.')[1])

                if result is not None:
                    stock_dao.save(ts_code, result.sort_index())
                    # redisUtil.r.zadd(Const.KEY_STOCK_UPDATE.value, {ts_code: int(result.iloc[[0]].index[0])})
                else:
                    print('there is no data of code %s' % ts_code)
                time.sleep(0.1)

            break


        # try:
        #         last_ten = histo_record.head(10)
        #         last_five = histo_record.head(5)
        #         # 缩量、小振幅、多头 数量 、连续缩量下跌git status

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

