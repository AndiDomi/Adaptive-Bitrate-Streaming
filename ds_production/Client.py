
from Encoder_select import Encoder_stream
if __name__ == '__main__':


    server_stream = Encoder_stream('TX2','player','h265', '192.168.11.43')

    while True:
        server_stream.start()