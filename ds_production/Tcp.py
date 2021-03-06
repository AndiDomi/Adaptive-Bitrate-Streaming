import socket
import time

class TcpProt():

    # class variables
    TCP_IP = None
    TCP_PORT = None
    BUFFER_SIZE = None
    server_socket = None
    player_socket = None
    address = None
    conn = None

    # constructor to initialize the class variables
    def __init__(self, other_tcp_ip, other_port, buffersize):

        # address of the client
        self.TCP_IP = other_tcp_ip
        self.TCP_PORT = other_port
        self.BUFFER_SIZE = buffersize  # Normally 64, less for faster response

    # start the socket connection
    def start(self, server_or_player):

        # if its server
        if server_or_player == 1:
            try:
                print("Server connecting")
                self.TCP_IP=''
                self.address = (self.TCP_IP, self.TCP_PORT)
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                self.server_socket.bind(self.address)
                self.server_socket.listen(5)
                print("Listening for client . . .")
                #global conn
                self.conn, self.address = self.server_socket.accept()
                print("Connected to client at ", self.address)

            except:
                print ("Connection Failed, Retrying..")
                time.sleep(3)
                self.start(1)
        # if its player
        else:

            try:  # Cant get it to make connection after retrying
                self.player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.player_socket_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.player_socket.connect((self.TCP_IP, self.TCP_PORT))


            except :
                print ("Connection Failed, Retrying..")
                time.sleep(3)
                self.start(0)

    def get_msg(self):
        try:
            get_msg = self.conn.recv(self.BUFFER_SIZE).decode('utf-8')
            if(not get_msg):
                print("we couldnt get the message, lets think what to do")
                self.start(1)

            else:
                return get_msg
        except:
            print("dead")



    def send_msg(self,message):
        message = str(message)
        try:
            self.player_socket.send(message.encode('utf-8'))
        except:
            self.start(0)
            self.player_socket.send(message.encode('utf-8'))
