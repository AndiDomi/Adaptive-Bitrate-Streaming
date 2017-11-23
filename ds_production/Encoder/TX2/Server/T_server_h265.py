import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib
GObject.threads_init()
Gst.init(None)


class T_server_h265:


    def __init__(self, stream_ip):

        self.STREAM_IP=stream_ip

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)

        # source
        self.src = Gst.ElementFactory.make('nvcamerasrc', None)
        self.src.set_property('fpsRange', "60 60")
        self.src.set_property('intent', 3)

        # video
        self.srccaps = Gst.Caps.from_string(
            "video/x-raw(memory:NVMM), width=(int)600, height=(int)600, format=(string)I420, framerate=(fraction)60/1")

        # conversion
        self.conversion = Gst.ElementFactory.make('nvvidconv', None)
        self.conversion.set_property('flip-method', 6)

        # encoder
        self.encoder = Gst.ElementFactory.make('omxh265enc', None)
        # self.encoder.set_property('low-latency', 1)
        self.encoder.set_property('control-rate', 2)
        self.encoder.set_property('bitrate', 1000)
        print(self.encoder.get_property('bitrate'))

        # stream
        self.stream = Gst.Caps.from_string("video/x-h265, stream-format=(string)byte-stream")
        self.rtp = Gst.ElementFactory.make('rtph265pay', None)
        self.parse = Gst.ElementFactory.make('h265parse', None)
        self.udp = Gst.ElementFactory.make('udpsink', None)
        self.udp.set_property('host', self.STREAM_IP)
        self.udp.set_property('port', 5060)
        self.udp.set_property('auto-multicast', False)

        # Add elements to the pipeline
        self.pipeline.add(self.src)
        self.pipeline.add(self.conversion)
        self.pipeline.add(self.encoder)
        self.pipeline.add(self.parse)
        self.pipeline.add(self.rtp)
        self.pipeline.add(self.udp)

        # link them together
        self.src.link_filtered(self.conversion, self.srccaps)
        self.conversion.link_filtered(self.encoder, self.srccaps)
        self.encoder.link_filtered(self.parse, self.stream)
        self.parse.link(self.rtp)
        self.rtp.link(self.udp)


    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


    def set_bitrate(self,bitrate):
        print("set bitrate")
        while(True):
            self.encoder.set_property('bitrate', bitrate)

    def get_bitrate(self):
        print ("get bitrate")
        gBitrate = self.encoder.get_property('bitrate')
        return gBitrate

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)