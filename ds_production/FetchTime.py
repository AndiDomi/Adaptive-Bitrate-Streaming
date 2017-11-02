# this file should be run every 30 min
import os
from datetime import datetime,timedelta
import ntplib
import time


class SyncTime(object):

    # Take time form server
    @staticmethod
    def fetch_time_from_server():
        try:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            os.system('date ' + time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time)))
            print("Online Time synchronized")
        except:
            print('Could not sync with server.')
            time.sleep(1)
            print('Retrying..')
            SyncTime.fetch_time_from_server()


    @staticmethod
    def get_time_now():
        time_start = datetime.now() + timedelta(0, 3)
        return time_start