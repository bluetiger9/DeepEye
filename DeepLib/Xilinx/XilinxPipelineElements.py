from DeepLib import *
from GstElementFactory import *
from RTSPUtils import *
from PipelineElements import *

# Processing Elements:
class XilinxFaceDetect(ProcessingElement):
    def __init__(self, id = None, linkTo = None):
        ProcessingElement.__init__(self, id, linkTo)

        videoconvert = GstElementFactory.element("videoconvert")
        facedetect = GstElementFactory.element("vaifacedetect")

        self.addMultiple(videoconvert, facedetect)

class XilinxPersonDetect(ProcessingElement):
    def __init__(self, id = None, linkTo = None):
        ProcessingElement.__init__(self, id, linkTo)

        persondetect = GstElementFactory.element("vaipersondetect")
        videoconvert = GstElementFactory.element("videoconvert")

        self.addMultiple(videoconvert, persondetect)
