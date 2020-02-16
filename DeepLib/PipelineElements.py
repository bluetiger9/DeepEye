## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

from DeepLib import *
from GstElementFactory import *
from RTSPUtils import *
from NvOsd import *
import configparser

class PipelineElement:
    _autoNr = 1

    @staticmethod
    def autoNr():
        nr = PipelineElement._autoNr
        PipelineElement._autoNr += 1
        return str(nr)

    def __init__(self, id = None, linkTo = None):
        if not id:
            id = type(self).__name__ + PipelineElement.autoNr()

        self.id = id
        self.gstElements = []
        self.gstElementsById = dict()
        self.lastElement = None
        self.linkTo = linkTo
    
    def add(self, element, gstSourcePad = None, gstSinkPad = None, gstProbes = None, id = None, linkTo = None):
        if not id:
            id = PipelineElement.autoNr() + "-gst-" + type(element).__name__
        
        if not linkTo:
            linkTo = self.lastElement

        component = {
            'id' : id,
            'linkTo' : linkTo,
            'gstElement' : element,
            'gstSourcePad' : gstSourcePad,
            'gstSinkPad' : gstSinkPad,
            'gstProbes' : gstProbes
        }

        self.gstElements.append(component)
        self.gstElementsById[id] = component
        self.lastElement = id
        
    def addMultiple(self, *elements):
        for element in elements:
            self.add(element)

class InputElement(PipelineElement):
    def __init__(self, id = None, linkTo = None):
        PipelineElement.__init__(self, id, linkTo)

class OutputElement(PipelineElement):
    def __init__(self, id = None, linkTo = None):
        PipelineElement.__init__(self, id, linkTo)

class ProcessingElement(PipelineElement):
    def __init__(self, id = None, linkTo = None):
        PipelineElement.__init__(self, id, linkTo)

# Input Elements
class FileInput(InputElement):
    def __init__(self, path, encoding = "H264", id = None, linkTo = None):
        InputElement.__init__(self, id, linkTo)

        source = GstElementFactory.element("filesrc", { 'location' : path } )

        if encoding is "H264":
            parser = GstElementFactory.element("h264parse")
            decoder = GstElementFactory.element("nvv4l2decoder")

        else:
            raise error(f"Unkown encoding {encoding}")

        streammux = GstElementFactory.element( \
            "nvstreammux", \
            {
                'width' : 1920,
                'height': 1080,
                'batch-size' : 1,
                'batched-push-timeout' : 4000000
            } \
        )
        
        self.addMultiple(source, parser, decoder)
        self.add(streammux, gstSinkPad='sink_0')


class MipiCameraInput(InputElement):
    def __init__(self, id = None, linkTo = None):
        InputElement.__init__(self, id, linkTo)

        nvcam = GstElementFactory.element("nvarguscamerasrc")
        
        capsFilter = GstElementFactory.capsFilter( \
            "video/x-raw(memory:NVMM), format=NV12, width=1280 height=720 framerate=30/1")
        
        self.addMultiple(nvcam, capsFilter)

class USBCameraInput(InputElement):
    def __init__(self, device = '/dev/video1', id = None, linkTo = None):        
        InputElement.__init__(self, id, linkTo)

        # note: tested with Logitech C920
        v4l2src = GstElementFactory.element("v4l2src", { 'device' : device } )

        #queue = GstElementFactory.element("queue")
        capsFilter = GstElementFactory.capsFilter( \
            "video/x-h264, width=1280, height=720, framerate=30/1")
        h264parse = GstElementFactory.element("h264parse")
        h264decode = GstElementFactory.element("nvv4l2decoder")

        self.addMultiple(v4l2src, capsFilter, h264parse, h264decode)

# Output Elements

class EGLOutput(OutputElement):
    def __init__(self, id = None, linkTo = None):
        OutputElement.__init__(self, id, linkTo)

        eglSink = GstElementFactory.element("nveglglessink")
        if is_aarch64():
            transform = GstElementFactory.element("nvegltransform")
            self.addMultiple(transform, eglSink)

        else:
            self.add(eglSink)

class RTSPOuput(OutputElement):
    def __init__(self, deepLib, bitRate = 1000000, updPort = 12222, name = "rtsp-output", path = "/test", id = None, linkTo = None):        
        OutputElement.__init__(self, id, linkTo)
        
        if not hasattr(deepLib, 'rtspServer'):
            deepLib.rtspServer = RTSPServer()
            
        deepLib.rtspServer.addPath(path)

        print("Create RTSP streamp\n")
        nvvidconv = GstElementFactory.element("nvvideoconvert")

        capsFilter = GstElementFactory.capsFilter("video/x-raw(memory:NVMM), format=I420")

        h264Encoder = GstElementFactory.element( \
            "nvv4l2h264enc", \
            { 
                "bitrate" : bitRate,
                "preset-level" : 1,
                "insert-sps-pps" : 1,
                "bufapi-version" : 1
            } \
        )

        rtph264Pay = GstElementFactory.element("rtph264pay")

        udpSink = GstElementFactory.element( \
            "udpsink", \
            {
                "host" : "127.0.0.1",
                "port" :  updPort,
                "async" : False,
                "sync" : 0
            }
        )

        self.addMultiple(nvvidconv, capsFilter, h264Encoder, rtph264Pay, udpSink)

class TCPOutput(OutputElement):
    def __init__(self, bitRate = 1000000, port = 8888, id = None, linkTo = None):        
        OutputElement.__init__(self, id, linkTo)

        videoconvert = GstElementFactory.element("videoconvert")
        
        theoraenc = GstElementFactory.element("theoraenc")
        
        oggmux = GstElementFactory.element("oggmux")

        tcpserversink = GstElementFactory.element( \
            "tcpserversink", \
            {
                "host" : "0.0.0.0",
                "port" : port
            } \
        )

        self.addMultiple(videoconvert, theoraenc, oggmux, tcpserversink)

# Processing Elements:
class NVInfer(ProcessingElement):
    def __init__(self, configPath, id = None, linkTo = None):
        ProcessingElement.__init__(self, id, linkTo)

        pgie = GstElementFactory.element("nvinfer", \
            { 'config-file-path' : configPath } \
        )
        self.add(pgie)

class NVTracker(ProcessingElement):
    def __init__(self, configPath, id = None, linkTo = None):
        ProcessingElement.__init__(self, id, linkTo)

        config = configparser.ConfigParser()
        config.read(configPath)
        config.sections()

        props = dict()
        for key in config['tracker']:
            if key == 'tracker-width' :
                tracker_width = config.getint('tracker', key)
                props['tracker-width'] = tracker_width
            if key == 'tracker-height' :
                tracker_height = config.getint('tracker', key)
                props['tracker-height'] = tracker_height
            if key == 'gpu-id' :
                tracker_gpu_id = config.getint('tracker', key)
                props['gpu_id'] = tracker_gpu_id
            if key == 'll-lib-file' :
                tracker_ll_lib_file = config.get('tracker', key)
                props['ll-lib-file'] = tracker_ll_lib_file
            if key == 'll-config-file' :
                tracker_ll_config_file = config.get('tracker', key)
                props['ll-config-file'] = tracker_ll_config_file
            if key == 'enable-batch-process' :
                tracker_enable_batch_process = config.getint('tracker', key)
                props['enable_batch_process'] = tracker_enable_batch_process
        
        nvtracker = GstElementFactory.element("nvtracker", props)
        self.add(nvtracker)

class NVOsd(ProcessingElement):
    def __init__(self, id = None, linkTo = None):
        ProcessingElement.__init__(self, id, linkTo)       
        nvvidconv = GstElementFactory.element("nvvideoconvert")
        nvosd = GstElementFactory.element("nvdsosd")
        self.add(nvvidconv)
        self.add(nvosd, gstProbes = { "sink" : osd_sink_pad_buffer_probe })

class Multiplexer(ProcessingElement):
    def __init__(self, nrOutputs, linkTo, id = None):
        ProcessingElement.__init__(self, id)

        tee = GstElementFactory.element("tee")
        teeId = self.id + "-tee"
        self.add(tee, id = teeId, linkTo = linkTo, gstSourcePad='src_%u')

        for i in range(0, nrOutputs):
            queue = GstElementFactory.element("queue")
            self.add(queue, id = self.outputId(i), linkTo = teeId)

    def outputId(self, nr):
        return self.id + "-queue-" + str(nr)