import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib
GObject.threads_init()
Gst.init(None)


class T_player_h264:


    def __init__(self):

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)

        # source

        self.udpsrc = Gst.ElementFactory.make('udpsrc')
        self.udpsrc.set_property('port', 5060)

        self.app = Gst.Caps.from_string('application/x-rtp, encoding-name=H264, payload=96')

        self.depay = Gst.ElementFactory.make('rtph264depay', None)

        self.queue = Gst.ElementFactory.make('queue', None)

        self.encoder = Gst.ElementFactory.make('avdec_h264', None)

        self.sink = Gst.ElementFactory.make('xvimagesink', None)
        self.sink.set_property('sync', False)
        self.sink.set_property('async', False)
        # self.sink.set_property('-e')

        self.pipeline.add(self.udpsrc)
        self.pipeline.add(self.depay)
        self.pipeline.add(self.queue)
        self.pipeline.add(self.encoder)
        self.pipeline.add(self.sink)

        # link them together

        self.udpsrc.link_filtered(self.depay, self.app)
        self.depay.link(self.queue)
        self.queue.link(self.encoder)
        self.encoder.link(self.sink)

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())