from FetchTime import SyncTime
from EncoderTest import *
from Tcp import *
from BandwidthTesting import *
if __name__ == '__main__':

    #print("Starting Client")
    #SyncTime.fetch_time_from_server()
    #print(SyncTime.get_time_now())

    # todo get the ip of the other board
    #print("Starting stream at minimum bitrate")

    # todo get the ip of the other board
    #encoder = Encoder("tx2", "server", "h264", "192.168.11.57", 5555)
    #encoder.start()
    #encoder.get_bitrate()

    # test_tcp_client= TcpProt('',3333,1024)
    # test_tcp_client.start(0)
    # print("The client just sent")
    # message = ''
    # flag = ''
    # #message = "andi"
    # #flag = "domi"
    # print(flag,message)
    # test_tcp_client.send_msg(flag,message)



    client = Bandwidth('0','192.168.11.40','5000',1)
    client.start()


