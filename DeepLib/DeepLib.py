## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

import gi
gi.require_version('Gst', '1.0')

import sys

from gi.repository import GObject, Gst

from PipelineBuilder import *
from JsonPipelineConfigLoader import *
from Platform import *

class DeepLib():
    def __init__(self):
        # Standard GStreamer initialization
        GObject.threads_init()
        Gst.init(None)
        pass

    @staticmethod
    def init():
        DeepLib.instance = DeepLib()
        DeepLib.instance.platform = Platform.create()
        print("Platform: " + str(DeepLib.instance.platform))

    @staticmethod
    def platform():
        return DeepLib.instance.platform

    @staticmethod
    def pipeline():
        return PipelineBuilder(DeepLib.instance)

    @staticmethod
    def pipelineFromJsonConfig(path):
        return JsonPipelineConfigLoader(DeepLib.instance).loadFromFile(path)

    @staticmethod
    def gstCallback(bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            sys.stdout.write("End-of-stream\n")
            loop.quit()
        elif t==Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            sys.stderr.write("Warning: %s: %s\n" % (err, debug))
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            sys.stderr.write("Error: %s: %s\n" % (err, debug))
            loop.quit()
        return True

    @staticmethod
    def runOnMain(pipeline):
        # create an event loop and feed gstreamer bus mesages to it
        loop = GObject.MainLoop()
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect ("message", DeepLib.gstCallback, loop)

        # start play back and listen to events
        print("Starting pipeline \n")
        pipeline.set_state(Gst.State.PLAYING)
        try:
            loop.run()
        except:
            pass

        # cleanup
        pipeline.set_state(Gst.State.NULL)

class DeepError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

def error(message):
    return DeepError(message)

H264 = "H264"