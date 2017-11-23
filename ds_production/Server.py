from FetchTime import SyncTime
import time
from BandwidthTesting import *
from Tcp import *

if __name__ == '__main__':
    print("Starting Server")

                            # ip to count the data
    server = Bandwidth('SERVER', '192.168.11.43', '5000', 1024, '192.168.11.42')
    server.start()
