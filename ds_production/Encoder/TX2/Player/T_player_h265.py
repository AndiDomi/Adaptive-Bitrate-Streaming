import gi
from gi.repository import GObject, Gst
from gi.repository import GLib


class T_player_h265:


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

        self.app = Gst.Caps.from_string('application/x-rtp, encoding-name=H266, payload=96')

        self.depay = Gst.ElementFactory.make('rtph265depay', None)

        self.parse = Gst.ElementFactory.make('h265parse')

        self.queue = Gst.ElementFactory.make('queue', None)

        self.encoder = Gst.ElementFactory.make('omxh265dec', None)

        self.sink = Gst.ElementFactory.make('nvoverlay', None)
        self.sink.set_property('sync', False)
        self.sink.set_property('async', False)
        # self.sink.set_property('-e')

        self.pipeline.add(self.udpsrc)
        self.pipeline.add(self.depay)
        self.pipeline.add(self.parse)
        self.pipeline.add(self.queue)
        self.pipeline.add(self.encoder)
        self.pipeline.add(self.sink)

        # link them together

        self.udpsrc.link_filtered(self.depay, self.app)
        self.depay.link(self.parse)
        self.parse.link(self.queue)
        self.queue.link(self.encoder)
        self.encoder.link(self.sink)