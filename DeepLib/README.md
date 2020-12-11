# DeepLib

**[GStreamer](https://gstreamer.freedesktop.org/)** based video processing pipelines made easy.

## Introduction
**DeepLib** is an easy to use **Python** library, which allows creating **GStreamer** based **video processing pipelines** in an easy way. It is based on **GStreamer Python Bindings library**, and simplifies building video pipelines, by grouping pipeline components, in bigger and much easier to understand logical blocks.

It allows creating **video processing pipelines** with as little code as:
```
    # initialize DeepLib
    DeepLib.init()

    # build pipeline
    pipeline = DeepLib \
        .pipeline() \
        .withMipiCameraInput() \
        .withEGLOutput() \
        .build()
```

## Features

A **DeepLib** pipeline is built up from multiple **pipeline elements**. Each DeepLib pipeline element implements a specific functionality.

The **pipeline elements** are of 3 **types**: `input`, `output` and `processing` element

**Input Elements**:
- File Input
- MIPI Camera Input
- USB Camera Input
- HDMI Input

**Output Elements**:
- EGL Output
- HDMI Output
- DisplayPort Output
- RTSP Output
- TCP Output
- WebRTC Output

**Processing Elements**:
- Multiplexer
- different Inference, Tracking, and other Deep Learning related elements 

## Platforms

**DeepLib** was initially created for **NVidia Jetson** based devices, but now it also supports **Xilinx UltraScale+** devices and as well as generic **GStreamer** platforms like **PC**-s, or the **Raspberry Pi**.

**DeepLib** automatically detects the current **`Platform`** on which is running. For common tasks video encoding (H.264, H.265) **hardware acceleration** is used when awailable.

Some **features**, like vendor specific deep learning framework based elements are available only on **specific `Platform`**-s.

## Getting started

To use **DeepLib**, **Python 3.5+** and **GStreamer** are needed:
```
$ sudo apt-get install python3 python3-pip
$ sudo pip3 install pyds
$ sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio gir1.2-gst-rtsp-server-1.0

```

**DeepLib** can be installed by cloning this repository:
```
$ git clone https://github.com/bluetiger9/DeepEye.git
```

The examples can be run as follows:
```
$ cd DeepEye/DeepLib/Examples
$ python3 <SomeExample>.py [...args]
```

## License
The code is licensed under the [MIT License](https://opensource.org/licenses/MIT).
