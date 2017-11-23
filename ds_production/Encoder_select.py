import gi
from gi.repository import GObject, Gst
from gi.repository import GLib

from Encoder.RPI.Player.R_player_h264 import R_player_h264
from Encoder.TX2.Player.T_player_h264 import T_player_h264

from Encoder.TX2.Player.T_player_h265 import T_player_h265

from Encoder.TX2.Server.T_server_h264 import T_server_h264
from Encoder.TX2.Server.T_server_h265 import T_server_h265

gi.require_version('Gst', '1.0')

class Encoder_stream():

    BOARD = None
    ENCODER_PROTOCOL = None
    PLAYER_OR_SERVER = None
    STREAM_IP = None
    SERVER_BITRATE_OBJ = None

    def __init__(self, board, player_or_server, encoder_protocol, stream_ip):

        self.BOARD = board
        self.PLAYER_OR_SERVER = player_or_server
        self.ENCODER_PROTOCOL = encoder_protocol
        self.STREAM_IP = stream_ip



        # if the board is a raspberry pi
        if self.BOARD == "RPI":

            # the encoder protocol is h264
            if self.ENCODER_PROTOCOL == "h264":

                # and its a player
                if self.PLAYER_OR_SERVER == "player":
                    print("Initializing player for RPI on H264 protocol")
                    r_player_h264= R_player_h264()

                # if its a server
                elif self.PLAYER_OR_SERVER == "server":
                    print("Initializing player for RPI on H264 protocol")



            # encoder protocol is h265
            elif self.ENCODER_PROTOCOL == "h264":

                # its a player
                if self.PLAYER_OR_SERVER == "player":
                    print("Initializing player for RPI on H265 protocol")

                # its a server
                elif self.PLAYER_OR_SERVER == "server":
                    print("Initializing server for RPI on H264 protocol")

        # if the board is a tx2
        elif self.BOARD == "TX2":
            # the encoder protocol is h264
            if self.ENCODER_PROTOCOL == "h264":
                # and its a player
                if self.PLAYER_OR_SERVER == "player":
                    print("Initializing player for TX2 on H264 protocol")
                    tx2_player_h264=T_player_h264()

                # if its a server
                elif self.PLAYER_OR_SERVER == "server":
                    print("Initializing server for TX2 on H264 protocol")
                    tx2_server_h264 = T_server_h264(self.STREAM_IP)
                    self.SERVER_BITRATE_OBJ=tx2_server_h264

            # encoder protocol is h265
            elif self.ENCODER_PROTOCOL == "h265":
                # its a player
                if self.PLAYER_OR_SERVER == "player":
                    print("Initializing player for TX2 on H265 protocol")
                    tx2_player_h264 = T_player_h265()

                # its a server
                elif self.PLAYER_OR_SERVER=="server":
                    print("Initializing server for TX2 on H265 protocol")
                    tx2_server_h265 = T_server_h265(self.STREAM_IP)
                    self.SERVER_BITRATE_OBJ = tx2_server_h265

    def set_bitrate(self,bitrate):
        self.SERVER_BITRATE_OBJ.set_bitrate(bitrate)

    def get_bitrate(self):
        print ("get bitrate")
        get_Bitrate = self.SERVER_BITRATE_OBJ.get_bitrate()
        return get_Bitrate

    def start(self):
        self.SERVER_BITRATE_OBJ.start()

