## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

import json
from PipelineElements import *

class JsonPipelineConfigLoader:
    def __init__(self, deepLib):		
        self.deepLib = deepLib
        self.pipelineBuilder = self.deepLib.pipeline()

    def loadFromFile(self, path):
        with open(path) as json_file:
            data = json.load(json_file)
            for element in data['elements']:
                id = element['id']
                type = element['type']
                properties = element.get('properties')
                links = element.get('links')
                self.parseElement(id, type, properties, links)

        return self.pipelineBuilder.build()

    def parseElement(self, id, type, properties, connections):
        print(f"parse element {id} {type} {properties} {connections}")
        if type == 'file-input':
            self.pipelineBuilder.withFileInput(id = id, path = properties['path'])

        elif type == 'mipi-camera-input':
            self.pipelineBuilder.withMipiCameraInput(id = id)

        elif type == 'usb-camera-input':
            self.pipelineBuilder.withUsbCameraInput(id = id)

        elif type == 'nv-infer':
            self.pipelineBuilder.withNVInfer(id = id, configPath = properties['path'], \
                linkTo = self.connectionToComponentId(connections['in']))
        
        elif type == 'nv-tracker':
            self.pipelineBuilder.withNVTracker(id = id, configPath = properties['path'], \
                linkTo = self.connectionToComponentId(connections['in']))
    
        elif type == 'nv-osd':
            self.pipelineBuilder.withNVOsd(id = id, linkTo = self.connectionToComponentId(connections['in']))
        
        elif type == 'egl-output':
            self.pipelineBuilder.withEGLOutput(id = id, linkTo = self.connectionToComponentId(connections['in']))
        
        elif type == 'rtsp-output':
            self.pipelineBuilder.withRtspOuput(id = id, path = properties['path'], linkTo = connections['in'])
        
        elif type == 'tcp-output':
            self.pipelineBuilder.withTCPOuput(id = id, path = properties['path'], linkTo = connections['in'])
        

    def connectionToComponentId(self, connection):
        return connection.split('/')[0]
