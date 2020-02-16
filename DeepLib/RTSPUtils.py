################################################################################
# Copyright (c) 2020, ATTILA TŐKÉS (tokes_atti@yahoo.com) All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
################################################################################
import gi
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer

class RTSPServer():
    def __init__(self):
        print("Creating RTSP server")
        self.server = GstRtspServer.RTSPServer()
        
        self.server.attach(None)
        print("Creating Rtsp server done.")

    def addPath(self, path):
        factory = RTSPPipelineFactory()
        factory.set_shared(True)
        
        self.server.get_mount_points().add_factory(path, factory)

class RTSPPipelineFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, udpPort = 12222, encoding = "H264"):
        GstRtspServer.RTSPMediaFactory.__init__(self)
        self.udpPort = udpPort
        self.encoding = encoding

    def do_create_element(self, url):
        pipeline_str = f"( udpsrc name=pay0 port={self.udpPort} caps=\"application/x-rtp, \
            media=video, clock-rate=90000, encoding-name={self.encoding}, payload=96\" )"
        print(f"RTSP pipeline def: {pipeline_str}")
        return Gst.parse_launch(pipeline_str)

