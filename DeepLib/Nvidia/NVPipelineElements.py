from DeepLib import *
from GstElementFactory import *
from RTSPUtils import *
from Nvidia.NvOsd import *
from PipelineElements import *

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
