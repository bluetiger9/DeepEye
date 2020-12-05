## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

from DeepLib import *
from GstElementFactory import *
from RTSPUtils import *

class PipelineElement:
    ELEMENT_TYPE_H264_DECODE = "h264decode"
    ELEMENT_TYPE_H264_ENCODE = "h264encode"
    ELEMENT_TYPE_CAPS_FILTER_I420_RAW = "capsfilterI420raw"
    ELEMENT_TYPE_CAPS_FILTER_NV12_720P = "capsfilterNV12p720"
    ELEMENT_TYPE_VIDEO_CONVERT = "videoconvert"
    ELEMENT_TYPE_STREAM_MUX = "streammux"
    ELEMENT_TYPE_CAMERA_SOURCE = "camsource"
    ELEMENT_TYPE_GL_SINK = "glsink"
    ELEMENT_TYPE_GL_TRANSFORM = "gltransform"
    ELEMENT_TYPE_HDMI_SOURCE = "hdmiSource"
    ELEMENT_TYPE_HDMI_SINK = "hdmiSink"
    ELEMENT_TYPE_DISPLAYPORT_SINK = "displayPortSink"

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
    def __init__(self, platform, path, encoding = "H264", id = None, linkTo = None):
        InputElement.__init__(self, id, linkTo)

        source = GstElementFactory.element("filesrc", { 'location' : path } )

        if encoding is "H264":
            parser = GstElementFactory.element("h264parse")
            decoder = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_H264_DECODE)

        else:
            raise error("Unkown encoding {}".format("encoding"))

        streammux = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_STREAM_MUX)

        self.addMultiple(source, parser, decoder)

        if streammux:
            self.add(streammux, gstSinkPad='sink_0')

        else:
            queue = GstElementFactory.element("queue")
            self.add(queue)


class MipiCameraInput(InputElement):
    def __init__(self, platform, id = None, linkTo = None):
        InputElement.__init__(self, id, linkTo)

        cam = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_CAMERA_SOURCE)

        capsFilter = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_CAPS_FILTER_NV12_720p)

        self.addMultiple(cam, capsFilter)

class USBCameraInput(InputElement):
    def __init__(self, platform, device = '/dev/video1', id = None, linkTo = None, encoding = "H264"):
        InputElement.__init__(self, id, linkTo)

        # note: tested with Logitech C920
        v4l2src = GstElementFactory.element("v4l2src", { 'device' : device } )

        self.add(v4l2src)

        if encoding is "H264":
            capsFilter = GstElementFactory.capsFilter( \
                "video/x-h264, width=1280, height=720, framerate=30/1")
            h264parse = GstElementFactory.element("h264parse")
            h264decode = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_H264_DECODE)

            self.addMultiple(capsFilter, h264parse, h264decode)

class HDMIInput(InputElement):
    def __init__(self, platform, id = None, linkTo = None):
        InputElement.__init__(self, id, linkTo)

        hdmiInput = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_HDMI_SOURCE)

        self.add(hdmiInput)

# Output Elements

class EGLOutput(OutputElement):
    def __init__(self, platform, id = None, linkTo = None):
        OutputElement.__init__(self, id, linkTo)

        glSink = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_GL_SINK)

        glTransform = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_GL_TRANSFORM)
        if glTransform:
            self.add(glTransform)

        self.add(glSink)

class RTSPOuput(OutputElement):
    def __init__(self, deepLib, bitRate = 1000000, updPort = 12222, name = "rtsp-output", path = "/test", id = None, linkTo = None):
        OutputElement.__init__(self, id, linkTo)

        if not hasattr(deepLib, 'rtspServer'):
            deepLib.rtspServer = RTSPServer()

        deepLib.rtspServer.addPath(path)

        print("Create RTSP streamp\n")

        vidconv = deepLib.platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_VIDEO_CONVERT)

        capsFilter =  deepLib.platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_CAPS_FILTER_I420_RAW)

        h264Encoder = deepLib.platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_H264_ENCODE, { "bitRate" : bitRate })

        rtph264Pay = GstElementFactory.element("rtph264pay")

        udpSink = GstElementFactory.element( \
            "udpsink", \
            {
                "host" : "127.0.0.1",
                "port" :  updPort,
                "async" : False,
                "sync" : False
            }
        )

        self.addMultiple(vidconv, capsFilter, h264Encoder, rtph264Pay, udpSink)

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

class HDMIOutput(OutputElement):
    def __init__(self, platform, id = None, linkTo = None):
        OutputElement.__init__(self, id, linkTo)

        hdmiSink = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_HDMI_SINK)

        self.add(hdmiSink)

class DisplayPortOutput(OutputElement):
    def __init__(self, platform, id = None, linkTo = None):
        OutputElement.__init__(self, id, linkTo)

        dpSink = platform.createHwAceleratedElement(PipelineElement.ELEMENT_TYPE_DISPLAY_PORT_SINK)

        self.add(dpSink)

# Processing Elements

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
