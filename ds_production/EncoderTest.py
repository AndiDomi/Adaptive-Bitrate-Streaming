#!/usr/bin/env python3


import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib

GObject.threads_init()
Gst.init(None)

class Encoder():

    BOARD = None
    ENCODER_PROTOCOL = None
    PLAYER_OR_SERVER = None
    STREAM_IP = None
    STREAM_PORT = None

    def __init__(self, board, player_or_server, encoder_protocol, stream_ip, stream_port):

        self.BOARD = board
        self.PLAYER_OR_SERVER = player_or_server
        self.ENCODER_PROTOCOL = encoder_protocol
        self.STREAM_IP = stream_ip
        self.STREAM_PORT = stream_port

        # if the board is a raspberry pi
        if board == "rpi":
            print ("Initializing gstreamer for rpi")

            # the encoder protocol is h264
            if self.ENCODER_PROTOCOL == "h264":
                print ("protocol selected " + self.ENCODER_PROTOCOL)

                # and its a player
                if self.ENCODER_PROTOCOL == "player":
                    print ("Initializing player")

                    self.pipeline = Gst.Pipeline()

                    # Create bus to get events from GStreamer pipeline
                    self.bus = self.pipeline.get_bus()
                    self.bus.add_signal_watch()
                    self.bus.connect('message::error', self.on_error)

                    # source
                    self.src = Gst.ElementFactory.make('nvcamerasrc', None)
                    self.src.set_property('fpsRange', "30 30")
                    self.src.set_property('intent', 3)

                    # video
                    # self.srccaps = Gst.Caps.from_string(
                    # "video/x-raw(memory:NVMM), width=(int)800, height=(int)800, format=(string)I420, framerate=(fraction)30/1")
                    self.srccaps = Gst.Caps.from_string(
                        "video/x-raw(memory:NVMM), width=(int)300, height=(int)300, format=(string)I420, framerate=(fraction)30/1")

                    # conversion
                    self.conversion = Gst.ElementFactory.make('nvvidconv', None)
                    self.conversion.set_property('flip-method', 6)

                    # encoder
                    self.encoder = Gst.ElementFactory.make('omxh264enc', None)
                    # self.encoder.set_property('low-latency', 1)
                    self.encoder.set_property('control-rate', 2)
                    self.encoder.set_property('bitrate', 40000)
                    print(self.encoder.get_property('bitrate'))

                    # stream
                    self.stream = Gst.Caps.from_string("video/x-h264, stream-format=(string)byte-stream")
                    self.rtp = Gst.ElementFactory.make('rtph264pay', None)
                    # self.rtp.set_property('mtu',100)
                    # self.rtpjitter=Gst.ElementFactory.make('rtpjitterbuffer')

                    self.parse = Gst.ElementFactory.make('h264parse', None)
                    self.udp = Gst.ElementFactory.make('udpsink', None)
                    self.udp.set_property('host', self.STREAM_IP)
                    self.udp.set_property('port', self.STREAM_PORT)
                    self.udp.set_property('auto-multicast', False)
                    # todo test this, if this needs to be caps or elementfactory
                    self.text = Gst.ElementFactory.make('textoverlay', None)
                    self.text.set_property('text', 'whats my purpose')

                    # Add elements to the pipeline
                    self.pipeline.add(self.src)
                    self.pipeline.add(self.conversion)
                    self.pipeline.add(self.encoder)
                    self.pipeline.add(self.parse)
                    self.pipeline.add(self.rtp)
                    self.pipeline.add(self.udp)
                    # self.pipeline.add(self.rtpjitter)

                    # todo check where to put this
                    # self.pipeline.add(self.text)
                    # we add the text overlay here

                    # link them together
                    self.src.link_filtered(self.conversion, self.srccaps)
                    self.conversion.link_filtered(self.encoder, self.srccaps)
                    self.encoder.link_filtered(self.parse, self.stream)
                    self.parse.link(self.rtp)

                    self.rtp.link(self.udp)

                # if its a server
                else:
                    print ("initializing server")

            # encoder protocol is h265
            else:
                print ("protocol selected " + encoder_protocol)

                # its a player
                if player_or_server == "player":
                    print ("initializing player")

                # its a server
                else:
                    print ("initializing server")

        # if the board is a tx2
        else:
            print ("initializing gstreamer for tx2")

            # the encoder protocol is h264
            if encoder_protocol == "h264":
                print ("protocol selected " + encoder_protocol)

                # and its a player
                if player_or_server == "player":
                    print ("initializing player")

                # if its a server
                else:
                    print ("initializing server")

                    # Create GStreamer pipeline
                    self.pipeline = Gst.Pipeline()

                    # Create bus to get events from GStreamer pipeline
                    self.bus = self.pipeline.get_bus()
                    self.bus.add_signal_watch()
                    self.bus.connect('message::error', self.on_error)

                    # source
                    self.src = Gst.ElementFactory.make('nvcamerasrc', None)
                    self.src.set_property('fpsRange', "30 30")
                    self.src.set_property('intent', 3)

                    # video
                    # self.srccaps = Gst.Caps.from_string(
                    # "video/x-raw(memory:NVMM), width=(int)800, height=(int)800, format=(string)I420, framerate=(fraction)30/1")
                    self.srccaps = Gst.Caps.from_string(
                        "video/x-raw(memory:NVMM), width=(int)300, height=(int)300, format=(string)I420, framerate=(fraction)30/1")

                    # conversion
                    self.conversion = Gst.ElementFactory.make('nvvidconv', None)
                    self.conversion.set_property('flip-method', 6)

                    # encoder
                    self.encoder = Gst.ElementFactory.make('omxh264enc', None)
                    # self.encoder.set_property('low-latency', 1)
                    self.encoder.set_property('control-rate', 2)
                    self.encoder.set_property('bitrate', 40000)
                    print(self.encoder.get_property('bitrate'))

                    # stream
                    self.stream = Gst.Caps.from_string("video/x-h264, stream-format=(string)byte-stream")
                    self.rtp = Gst.ElementFactory.make('rtph264pay', None)
                    # self.rtp.set_property('mtu',100)
                    # self.rtpjitter=Gst.ElementFactory.make('rtpjitterbuffer')

                    self.parse = Gst.ElementFactory.make('h264parse', None)
                    self.udp = Gst.ElementFactory.make('udpsink', None)
                    self.udp.set_property('host', self.STREAM_IP)
                    self.udp.set_property('port', self.STREAM_PORT)
                    self.udp.set_property('auto-multicast', False)
                    # todo test this, if this needs to be caps or elementfactory
                    self.text = Gst.ElementFactory.make('textoverlay', None)
                    self.text.set_property('text', 'whats my purpose')

                    # Add elements to the pipeline
                    self.pipeline.add(self.src)
                    self.pipeline.add(self.conversion)
                    self.pipeline.add(self.encoder)
                    self.pipeline.add(self.parse)
                    self.pipeline.add(self.rtp)
                    self.pipeline.add(self.udp)
                    # self.pipeline.add(self.rtpjitter)

                    # todo check where to put this
                    # self.pipeline.add(self.text)
                    # we add the text overlay here

                    # link them together
                    self.src.link_filtered(self.conversion, self.srccaps)
                    self.conversion.link_filtered(self.encoder, self.srccaps)
                    self.encoder.link_filtered(self.parse, self.stream)
                    self.parse.link(self.rtp)

                    self.rtp.link(self.udp)

            # encoder protocol is h265
            else:
                print ("protocol selected " + encoder_protocol)

                # its a player
                if player_or_server == "player":
                    print ("initializing player")

                # its a server
                else:
                    print ("initializing server")


    def start(self):
        print ("start encoder")
        while(True):
            self.pipeline.set_state(Gst.State.PLAYING)


    def set_bitrate(self,bitrate):
        print ("set bitrate")
        self.encoder.set_property('bitrate', bitrate)

    def get_bitrate(self):
        print ("get bitrate")
        gBitrate = self.encoder.get_property('bitrate')
        return gBitrate

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


