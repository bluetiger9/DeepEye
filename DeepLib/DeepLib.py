## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

DEFAUL_DEEPSTREAM_PYTHON_LIB_PATH = '/opt/nvidia/deepstream/deepstream-4.0/sources/python/apps/'

import sys
sys.path.append(DEFAUL_DEEPSTREAM_PYTHON_LIB_PATH)

import gi
gi.require_version('Gst', '1.0')

from gi.repository import GObject, Gst
from common.is_aarch_64 import is_aarch64
from common.bus_call import bus_call

from PipelineBuilder import *
from JsonPipelineConfigLoader import *

class DeepLib():
    def __init__(self):
        # Standard GStreamer initialization
        GObject.threads_init()
        Gst.init(None)
        pass
    
    @staticmethod
    def init():
        DeepLib.instance = DeepLib()
   
    @staticmethod
    def pipeline():
        return PipelineBuilder(DeepLib.instance)
    
    @staticmethod
    def pipelineFromJsonConfig(path):
        return JsonPipelineConfigLoader(DeepLib.instance).loadFromFile(path)

    @staticmethod
    def runOnMain(pipeline):
        # create an event loop and feed gstreamer bus mesages to it
        loop = GObject.MainLoop()
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect ("message", bus_call, loop)
    
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