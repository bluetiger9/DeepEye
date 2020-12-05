from Platform import Platform
from Platform import GenericPlatform
from GstElementFactory import *
from PipelineElements import PipelineElement

import sys

# Xilinx UltraScale+ based platforms
class XilinxPlatform(GenericPlatform):
    def __init__(self):
        pass

    @staticmethod
    def tryCreate():
        import platform

        if not "xilinx" in platform.platform():
            return None
            
        return XilinxPlatform()

    def createHwAceleratedElement(self, type, props = {}):
        if type == PipelineElement.ELEMENT_TYPE_H264_DECODE:
            return GstElementFactory.element("omxh264dec")

        elif type == PipelineElement.ELEMENT_TYPE_H264_ENCODE:
            return GstElementFactory.element( \
                "omxh264enc", \
                {
                    "target-bitrate" : props['bitRate'],
                } \
            )

        elif type == PipelineElement.ELEMENT_TYPE_HDMI_SOURCE:
            # TODO device
            return GstElementFactory.element("v4l2src")

        elif type == PipelineElement.ELEMENT_TYPE_HDMI_SINK:
            # TODO xlnxvideosink sink-type="hdmi" sync=false
            return GstElementFactory.element( \
                "kmssink", \
                {
                    "bus-id" : "b00c0000.v_mix",
                    "plane-id" : 30,
                    "sync" : False,
                    "fullscreen-overlay" : False
                } \
            )

        elif type == PipelineElement.ELEMENT_TYPE_DISPLAYPORT_SINK:
            # TODO xlnxvideosink sink-type="dp" sync=false
            return GstElementFactory.element( \
                "kmssink", \
                {
                    "bus-id" : "b00c0000.v_mix",
                    "plane-id" : 30,
                    "sync" : False,
                    "fullscreen-overlay" : False
                } \
            )

        else:
            return super().createHwAceleratedElement(type, props)