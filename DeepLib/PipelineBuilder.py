## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

from DeepLib import *
from GstElementFactory import *
from PipelineElements import *
from Nvidia.NVPipelineElements import *
from Xilinx.XilinxPipelineElements import *
from Pipeline import *

class PipelineBuilder:
    def __init__(self, deepLib):
        self.deepLib = deepLib
        self.platform = deepLib.platform
        self.pipeline = Pipeline(GstElementFactory.pipeline())

    def add(self, element):
        self.pipeline.add(element)
        return self

    def withFileInput(self, path, encoding = "H264", id = None):
        return self.add(FileInput(self.platform, path, encoding, id = id))

    def withMipiCameraInput(self, id = None):
        return self.add(MipiCameraInput(id = id))

    def withUsbCameraInput(self, device = '/dev/video1', id = None, linkTo = None, encoding = "H264"):
        return self.add(USBCameraInput(self.platform, device, id = id, encoding = encoding))

    def withHdmiInput(self, id = None):
        return self.add(HDMIInput(self.platform, id = id, linkTo = linkTo))
    
    def withEGLOutput(self, id = None, linkTo = None):
        return self.add(EGLOutput(self.platform, id = id, linkTo = linkTo))

    def withRtspOutput(self, bitRate = 1000000, updPort = 12222, name = "rtsp-output", path = "/test", id = None, linkTo = None):
        return self.add(RTSPOuput(self.deepLib, bitRate, updPort, name, path, id = id, linkTo = linkTo))

    def withTcpOutput(self, bitRate = 1000000, port = 8888, id = None, linkTo = None):
        return self.add(TCPOutput(bitRate, port, id = id, linkTo = linkTo))

    def withHdmiOutput(self, id = None, linkTo = None):
        return self.add(HDMIOutput(self.platform, id = id, linkTo = linkTo))
    
    def withDisplayPortOutput(self, id = None, linkTo = None):
        return self.add(DisplayPortOutput(self.platform, id = id, linkTo = linkTo))

    # NVidia specific
    def withNVInfer(self, configPath, id = None, linkTo = None):
        return self.add(NVInfer(configPath, id = id, linkTo = linkTo))

    def withNVTracker(self, configPath, id = None, linkTo = None):
        return self.add(NVTracker(configPath, id = id, linkTo = linkTo))

    def withNVOsd(self, id = None, linkTo = None):
        return self.add(NVOsd(id = id, linkTo = linkTo))

    # Xilinx specific
    def withXilinxFaceDetect(self, id = None, linkTo = None):
        return self.add(XilinxFaceDetect(id = id, linkTo = linkTo))

    def withXilinxPersonDetect(self, id = None, linkTo = None):
        return self.add(XilinxPersonDetect(id = id, linkTo = linkTo))

    def withSingleShotDetector(self, model, id = None, linkTo = None):
        return self.add(XilinxSingleShotDetector(model, id = id, linkTo = linkTo))

    def build(self):
        return self.pipeline.asGstPipeline()

