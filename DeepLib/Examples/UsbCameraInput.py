import sys
sys.path.append('..')

from DeepLib import *

def main(args):
    # Check input arguments
    if len(args) != 2:
        sys.stderr.write("usage: %s <usb camera device>\n" % args[0])
        sys.exit(1)
    else:
        device = args[1]

    # initialize DeepLib
    DeepLib.init()

    # build pipeline
    pipeline = DeepLib \
        .pipeline() \
        .withUsbCameraInput(device) \
        .withEGLOutput() \
        .build()

    #.withEGLOutput() \
    # run on the main thread
    DeepLib.runOnMain(pipeline)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
