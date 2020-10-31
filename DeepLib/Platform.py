from PipelineElements import PipelineElement
from GstElementFactory import *

class Platform():
    def createHwAceleratedElement(type):
        return None

    @staticmethod
    def create():
        from Nvidia.NVPlatform import NvidiaPlatform
        nvidia = NvidiaPlatform.tryCreate()

        if nvidia:
            return nvidia

        else:
            return GenericPlatform.create()

# Generic Gstreamer platform
class GenericPlatform(Platform):
    def __init__(self):
        pass

    @staticmethod
    def create():
        return GenericPlatform()

    def createHwAceleratedElement(self, type, props = {}):
        if type == PipelineElement.ELEMENT_TYPE_H264_DECODE:
            return GstElementFactory.element("avdec_h264")

        elif type == PipelineElement.ELEMENT_TYPE_H264_ENCODE:
            return GstElementFactory.element( \
                "x264enc", \
                {
                    "bitrate" : props['bitRate'],
                    "speed-preset" : "ultrafast",
                    "tune" : "zerolatency"
                } \
            )

        elif type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_I420_RAW:
            return GstElementFactory.capsFilter("video/x-raw, format=I420")

        elif type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_NV12_720P:
            return GstElementFactory.capsFilter( \
                "video/x-raw, format=NV12, width=1280 height=720 framerate=30/1")

        elif type == PipelineElement.ELEMENT_TYPE_VIDEO_CONVERT:
            return GstElementFactory.element("videoconvert")

        elif type == PipelineElement.ELEMENT_TYPE_CAMERA_SOURCE:
            return GstElementFactory.element("v4l2src")

        elif type == PipelineElement.ELEMENT_TYPE_GL_SINK:
            return GstElementFactory.element("glimagesink")

        else:
            return None
