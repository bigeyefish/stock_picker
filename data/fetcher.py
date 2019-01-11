import tushare as ts
import datetime
from config.config import configs


class Fetch:
    def __init__(self) -> None:
        self.start_date = (datetime.date.today() - datetime.timedelta(days=configs['init_stock_days'])).strftime(
            '%Y%m%d')
        ts.set_token('e9002771412a9735ddc9d24529386ef4e2b9c4adf80751cd60c27829')
        self.pro = ts.pro_api()
        self.sh_index = None

    # 获取单只股票的历史数据
    def get_multi_data(self, ts_code):
        print('get stock [%s] data since %s' % (ts_code, self.start_date))
        try:
            # 获取大盘数据
            if self.sh_index is None:
                self.sh_index = self.pro.index_daily(ts_code='000001.SH', start_date=self.start_date,
                                                     end_date='').set_index('trade_date')

            # 获取股票历史行情
            histo_record = ts.pro_bar(ts_code=ts_code, pro_api=self.pro, start_date=self.start_date, adj='qfq', factors=['tor', 'vr'])
            # 叠加大盘
            histo_record['sz_pct_change'] = self.sh_index['pct_chg']
            return histo_record
        except Exception as e:
            print(e)
            return None

    # 查询沪深股票列表
    def get_stock_list(self):
        return self.pro.stock_basic(list_status='L')

fetch = Fetch()
