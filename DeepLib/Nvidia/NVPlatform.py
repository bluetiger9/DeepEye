from Platform import Platform
from GstElementFactory import *
from PipelineElements import PipelineElement

import sys

# Nvidia DeepStream based platform
class NvidiaPlatform(Platform):
    DEFAUL_DEEPSTREAM_PYTHON_LIB_PATH = '/opt/nvidia/deepstream/deepstream-4.0/sources/python/apps/'

    def __init__(self):
        pass

    @staticmethod
    def tryCreate():
        try:
            sys.path.append(NvidiaPlatform.DEFAUL_DEEPSTREAM_PYTHON_LIB_PATH)

            from common.is_aarch_64 import is_aarch64

            return NvidiaPlatform()

        except ImportError:
            return None

    def createHwAceleratedElement(self, type, props = {}):
        if type == PipelineElement.ELEMENT_TYPE_H264_DECODE:
            return GstElementFactory.element("nvv4l2decoder")

        elif type == PipelineElement.ELEMENT_TYPE_H264_ENCODE:
            return GstElementFactory.element( \
                "nvv4l2h264enc", \
                {
                    "bitrate" : props['bitRate'],
                    "preset-level" : 1,
                    "insert-sps-pps" : 1,
                    "bufapi-version" : 1
                } \
            )

        elif type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_I420_RAW:
            return  GstElementFactory.capsFilter("video/x-raw(memory:NVMM), format=I420")

        elif type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_NV12_720P:
            return GstElementFactory.capsFilter( \
                "video/x-raw(memory:NVMM), format=NV12, width=1280 height=720 framerate=30/1")

        elif type == PipelineElement.ELEMENT_TYPE_VIDEO_CONVERT:
            return GstElementFactory.element("nvvideoconvert")

        elif type == PipelineElement.ELEMENT_TYPE_STREAM_MUX:
            return GstElementFactory.element( \
                "nvstreammux", \
                {
                    'width' : 1920,
                    'height': 1080,
                    'batch-size' : 1,
                    'batched-push-timeout' : 4000000
                } \
            )

        elif type == PipelineElement.ELEMENT_TYPE_CAMERA_SOURCE:
            return GstElementFactory.element("nvarguscamerasrc")

        elif type == PipelineElement.ELEMENT_TYPE_GL_SINK:
            return GstElementFactory.element("nveglglessink")

        elif type == PipelineElement.ELEMENT_TYPE_GL_TRANSFORM:
            return GstElementFactory.element("nvegltransform")

        else:
            return None