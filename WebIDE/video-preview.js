/* Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
/* Licence: MIT */

function playVideo(uri, videoElementId) {
    video = document.getElementById(videoElementId)
    source = video.children[0]
    source.setAttribute('src', uri);
    video.load();
    video.play();
}

document.getElementById('video-uri-1')
    .addEventListener('change', e => playVideo(e.target.value, 'video-1'))

document.getElementById('video-uri-2')
    .addEventListener('change', e => playVideo(e.target.value, 'video-2'))