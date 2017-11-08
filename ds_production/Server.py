from FetchTime import SyncTime
import time
from BandwidthTesting import *
from Tcp import *
if __name__ == '__main__':
    print ("Starting Server")


    # test_tcp_server= TcpProt('',3333,1024)
    # test_tcp_server.start(1)
    # print("The server just received")
    # print(test_tcp_server.get_msg())



    server = Bandwidth('1','192.168.11.47','5000',1)
    server.start()
