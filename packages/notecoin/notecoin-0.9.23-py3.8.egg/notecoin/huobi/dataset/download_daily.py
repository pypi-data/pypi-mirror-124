from datetime import datetime, timedelta

from notecoin.huobi.history.core import load_daily_all
from notedrive.lanzou import LanZouCloud


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

def save_to_odps():
    pass
