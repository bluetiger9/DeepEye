/* Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
/* Licence: MIT */

function onVideoPreviewSelected() {
    document.getElementById('pipeline-editor').style.visibility = 'hidden';
    document.getElementById('pipeline-editor-li').classList.remove('active');    
    document.getElementById('video-preview').style.visibility = 'visible';
    document.getElementById('video-preview-li').classList.add('active');
}

function onPipelineEditorSelected() {
    document.getElementById('pipeline-editor').style.visibility = 'visible';
    document.getElementById('pipeline-editor-li').classList.add('active');    
    document.getElementById('video-preview').style.visibility = 'hidden';
    document.getElementById('video-preview-li').classList.remove('active');

}