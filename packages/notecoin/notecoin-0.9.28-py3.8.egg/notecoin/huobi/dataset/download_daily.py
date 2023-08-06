from datetime import datetime, timedelta

import pandas as pd
from notecoin.huobi.history.core import ALL_PERIODS, ALL_TYPES, load_daily_all
from notedrive.lanzou import LanZouCloud
from noteodps import opt
from odps import DataFrame


def save_to_lanzou():
    downer = LanZouCloud()
    downer.ignore_limits()
    downer.login_by_cookie()
    start_date = datetime(2021, 5, 3)
    end_date = datetime(2021, 5, 31)
    duration = end_date - start_date
    for i in range(duration.days + 1):
        day = end_date - timedelta(days=i)
        file_path = load_daily_all(period='1min', date=day)
        downer.upload_file(file_path, folder_id='3359096')


def save_to_odps(start_date=datetime(2021, 5, 3), end_date=datetime(2021, 5, 31)):
    duration = end_date - start_date
    for i in range(duration.days + 1):
        for _type in ALL_TYPES:
            for period in ALL_PERIODS:
                day = end_date - timedelta(days=i)
                file_path = load_daily_all(period=period, _type=_type, date=day)
                print(opt.list_tables())
                print(file_path)
                df = DataFrame(pd.read_csv(file_path))
                df.persist("ods_notecoin_huobi_klines_data_d",
                           partition=f"ds={day.strftime('%y%M%d')},type={_type},period={period}")
                return


# save_to_odps()
file_path='/root/workspace/tmp/coin/daily/klines_spot_1min-20210531.csv'
df = DataFrame(pd.read_csv(file_path))
df.persist("ods_notecoin_huobi_klines_data_d",
           partition=f"ds=20211025,type=tt,period=1min")
