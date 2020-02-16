/* Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
/* Licence: MIT */

/** Socket Types **/
var videoSocket = new Rete.Socket('Video socket');

/** Vue Controls **/
var VueStrControl = {
    props: ['readonly', 'emitter', 'ikey', 'getData', 'putData'],
    template: '<input type="text" :readonly="readonly" :value="value" @input="change($event)" @dblclick.stop="" @pointerdown.stop="" @pointermove.stop=""/>',
    data() {
        return {
            value: "",
        }
    },
    methods: {
        change(e) {
            this.value = e.target.value;
            this.update();
        },
        update() {
            if (this.ikey)
                this.putData(this.ikey, this.value)
            this.emitter.trigger('process');
        }
    },
    mounted() {
        this.value = this.getData(this.ikey);
    }
}

class StrControl extends Rete.Control {
    constructor(emitter, key, readonly) {
        super(key);
        this.component = VueStrControl;
        this.props = { emitter, ikey: key, readonly };
    }

    setValue(val) {
        this.vueContext.value = val;
    }
}

/** Components */
class GenericComponent extends Rete.Component {
    constructor(name, type, controls = [], inputs = [], outputs = []) {
        super(name);
        this.controls = controls;
        this.inputs = inputs;
        this.outputs = outputs;
        this.type = type;
    }

    builder(node) {
        this.controls.forEach(
            control => node.addControl(new StrControl(this.editor, control))
        );
        this.inputs.forEach(
            input => node.addInput(new Rete.Input(input, "", videoSocket))
        );
        this.outputs.forEach(
            output => node.addOutput(new Rete.Output(output, "", videoSocket))
        );
        node.data['type'] = this.type
        return node
    }

    worker(node, inputs, outputs) {
        //outputs['num'] = node.data.num;
    }
}

var FileInputComponent = new GenericComponent(
    "File Input", "file-input", ['path'], [], ['out']);

var MipiCameraInputComponent = new GenericComponent(
    "MIPI Camera Input", "mipi-camera-input", [], [], ['out']);

var UsbCameraInputComponent = new GenericComponent(
    "USB Camera Input", "usb-camera-input", ['device'], [], ['out']);

var NVInferComponent = new GenericComponent(
    "NV Infer", "nv-infer", ['path'], ['in'], ['out'] );

var NVOsdComponent = new GenericComponent(
    "NV OSD", "nv-osd", [ ], ['in'], ['out'] );

var NVTrackerComponent = new GenericComponent(
    "NV Tracker", "nv-tracker", ['path'], ['in'], ['out'] );

var EGLOutputComponent = new GenericComponent(
    "EGL Output", "egl-output", [ ], ['in'], [] );

var RtspOutputComponent = new GenericComponent(
    "RTSP Output", "rtsp-output", [ 'path' ], ['in'], [] );

var TCPOutputComponent = new GenericComponent(
    "TCP Output", "tcp-output", [ ], ['in'], [] );    

var _editor = undefined;

function exportPipeline() {
    nodes = [];
    for (var editorNode of Object.values(_editor.toJSON()['nodes'])) {
        pipelineNode = {
            "id" : "" + editorNode['id'],
            "type" : editorNode['data']['type'],
            "properties" : Object(),
            "links" : Object()
        }

        for (var [property, value] of Object.entries(editorNode['data'])) {
            if (property != 'type') {
                pipelineNode['properties'][property] = value;
            }
        }

        for (var [input, connections] of Object.entries(editorNode['inputs'])) {
            if (connections['connections'].length > 0) {
                connection = connections['connections'][0];
                pipelineNode['links'][input] = "" + connection['node'] + "/" + connection['output'];
            }
        }

        nodes.push(pipelineNode)
    }

    jsonContent = JSON.stringify({ 'nodes' : nodes }, null, 2);
    downloadAsFile('pipeline.json', jsonContent)
}

function resetPipeline() {
    
}

(async () => {
    var container = document.querySelector('#pipeline-editor');
    var editor = new Rete.NodeEditor('demo@0.1.0', container);
    editor.use(ConnectionPlugin.default);
    editor.use(VueRenderPlugin.default);
    editor.use(ContextMenuPlugin.default);
    editor.use(AreaPlugin);
    editor.use(CommentPlugin.default);
    editor.use(ConnectionMasteryPlugin.default);

    _editor = editor;

    var components = [
        FileInputComponent,
        MipiCameraInputComponent,
        UsbCameraInputComponent,
        NVInferComponent,
        NVOsdComponent,
        NVTrackerComponent,
        EGLOutputComponent,
        RtspOutputComponent,
        TCPOutputComponent
    ];

    var engine = new Rete.Engine('demo@0.1.0');

    components.map(c => {
        editor.register(c);
        engine.register(c);
    });

    var file = await FileInputComponent.createNode({ path: 'test-h264.vid' });
    var nvInfer = await NVInferComponent.createNode({ path: 'primary-infer.txt' });
    var nvOsd = await NVOsdComponent.createNode();
    var eglOut = await EGLOutputComponent.createNode();
    var rtspOut = await RtspOutputComponent.createNode({ path: '/test' });

    var add = await components[1].createNode();

    file.position = [-200, 150];
    nvInfer.position = [100, 150];
    nvOsd.position = [400, 150];
    eglOut.position = [700, 80];
    rtspOut.position = [700, 220]

    editor.addNode(file);
    editor.addNode(nvInfer);
    editor.addNode(nvOsd);
    editor.addNode(eglOut);
    editor.addNode(rtspOut);

    editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
        console.log('process');
        await engine.abort();
        await engine.process(editor.toJSON());
        console.log('JSON: ' + JSON.stringify(editor.toJSON()));
    });

    editor.view.resize();
    AreaPlugin.zoomAt(editor);
    editor.trigger('process');
})();