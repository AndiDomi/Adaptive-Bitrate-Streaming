from FetchTime import SyncTime
import time
from BandwidthTesting import *
from Tcp import *
from Encoder_select import Encoder_stream
if __name__ == '__main__':
    print("Starting Server")


    # start the video stream

                            # ip to count the data
    # server = Bandwidth('SERVER', '192.168.11.43', '5000', 1024, '192.168.11.42')
    # server.start()

    server_stream = Encoder_stream('TX2','server','h264', '192.168.11.42')

    while True:
        server_stream.start()