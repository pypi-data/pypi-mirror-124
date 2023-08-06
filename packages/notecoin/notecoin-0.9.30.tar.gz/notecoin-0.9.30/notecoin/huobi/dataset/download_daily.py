from datetime import datetime, timedelta

import pandas as pd
from notecoin.huobi.history.core import ALL_PERIODS, ALL_TYPES, load_daily_all
from notedrive.lanzou import LanZouCloud
from noteodps import opt
from odps import DataFrame
from tqdm import tqdm


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
    def save_file_to_odps(file_path, partition):
        t = opt.get_table("ods_notecoin_huobi_klines_data_d")
        if t.exist_partition(partition):
            print(f'{partition} exist,drop it.')
            return
            t.delete_partition(partition_spec=partition)
        columns = ['symbol', 'id', 'open', 'close', 'low', 'high', 'vol', 'amount']
        dtype = {'symbol': 'str', 'id': 'long', 'open': 'float',
                 'close': 'float', 'low': 'float', 'high': 'float',
                 'vol': 'float', 'amount': 'float'}
        with t.open_writer(partition=partition, create_partition=True) as writer:
            for df in tqdm(pd.read_csv(file_path, header=None, names=columns, dtype=dtype, chunksize=100000)):
                writer.write(df.values.tolist())

    duration = end_date - start_date
    for i in range(duration.days + 1):
        for _type in ALL_TYPES:
            for period in ALL_PERIODS:
                day = end_date - timedelta(days=i)
                file_path = load_daily_all(period=period, _type=_type, date=day)

                partition = f"type='{_type}',period='{period}',ds='{day.strftime('%y%M%d')}'"
                save_file_to_odps(file_path, partition)
                return
