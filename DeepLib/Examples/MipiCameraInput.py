import sys
sys.path.append('..')

from DeepLib import *

def main(args):
    # initialize DeepLib
    DeepLib.init()

    # build pipeline
    pipeline = DeepLib \
        .pipeline() \
        .withMipiCameraInput() \
        .withEGLOutput() \
        .build()

    # run on the main thread
    DeepLib.runOnMain(pipeline)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
