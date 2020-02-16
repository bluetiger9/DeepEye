## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

from DeepLib import *
from GstElementFactory import *
from RTSPUtils import *
from PipelineElements import *     

class Pipeline:
    def __init__(self, gstPipeline):		
        self.pipeline = gstPipeline
        self.elements = []
        self.elementsById = dict()

    def add(self, element):
        self.elements.append(element)
        self.elementsById[element.id] = element

    def asGstPipeline(self):
        # auto-generate links:
        byId = dict()
        byLink = dict()
        lastElementId = None
        lastElementById = dict()
        for element in self.elements:
            if element.linkTo:
                lastElementId = lastElementById[element.linkTo]
                
            for subElement in element.gstElements:
                id = subElement['id']
                byId[id] = subElement

                linkTo = subElement['linkTo']                
                if not linkTo and lastElementId:
                    subElement['linkTo'] = lastElementId
                    linkTo = subElement['linkTo']

                if not linkTo in byLink:
                    byLink[linkTo] = []
                
                byLink[linkTo].append(id)
                lastElementId = id
                lastElementById[element.id] = id

        # auto-generate multiplexers (for outputs linked to multiple inputs)
        multiplexersById = dict()
        multiplexersOutNrById = dict()        
        for id, fromList in byLink.items():
            if len(fromList) > 1:
                print(f"multiplexer {id}")
                multiplexersById[id] = Multiplexer(len(fromList), id = "multiplexer-" + id, linkTo = id)
                multiplexersOutNrById[id] = 0
                self.elements.append(multiplexersById[id])
                for nr in range(0, len(fromList)):
                    byId[fromList[nr]]['linkTo'] = multiplexersById[id].outputId(nr)
                    print(f"   link_multi {fromList[nr]} {byId[fromList[nr]]['linkTo']}")

        # add elements:
        for element in self.elements:               
            for subElement in element.gstElements:
                id = subElement['id']
                byId[id] = subElement
                linkTo = subElement['linkTo']
                gstElement = subElement['gstElement']
                print(f"add_comp {id} linkto: {linkTo}")	
                self.pipeline.add(gstElement)

        # link:
        last = None
        for element in self.elements:
            for subElement in element.gstElements:
                id = subElement['gstElement']
                gstElement = subElement['gstElement']
                linkTo = subElement['linkTo']
                if linkTo:
                    linkToElement = byId[linkTo]
                    last = linkToElement['gstElement']
                    print(f"link {linkToElement['id']} -> {subElement['id']}")
                    #if linkTo in multiplexersById and id in byLink[linkTo]:
                    #    multiplexerOutNr = multiplexersOutNrById[linkTo]
                    #    multiplexersOutNrById[linkTo] += 1
                    #    linkToElement = byId[multiplexersById[linkTo].outputId(multiplexerOutNr)]
                    #    print(f"   link_multi {linkToElement['id']}")

                    if subElement['gstSinkPad'] or linkToElement['gstSourcePad']:
                        if subElement['gstSinkPad']:
                            sinkPad = gstElement.get_request_pad(subElement['gstSinkPad'])
                        else:
                            sinkPad = gstElement.get_static_pad("sink")

                        if linkToElement['gstSourcePad']:
                            srcPad = last.get_request_pad(linkToElement['gstSourcePad'])
                        else:
                            srcPad = last.get_static_pad("src")

                        srcPad.link(sinkPad)

                    else: 
                        last.link(gstElement)
                
            last = gstElement
        
        # probes
        for component in self.elements:
            for subElement in element.gstElements:
                gstElement = subElement['gstElement']
                if subElement['gstProbes']:
                    for pad, probe in subElement['gstProbes'].items():
                        print(f"add_probe {pad} {probe}")
                        pad = gstElement.get_static_pad(pad)
                        pad.add_probe(Gst.PadProbeType.BUFFER, probe, 0)
        
        return self.pipeline