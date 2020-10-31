import sys
sys.path.append('..')

from DeepLib import *

def main(args):
	# Check input arguments
	if len(args) != 2:
		sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
		sys.exit(1)

 	# initialize DeepLib
    DeepLib.init()

    # build pipeline
	pipeline = DeepLib() \
		.pipeline() \
		.withFileSource(args[1]) \
		.withNVInfer("dstest1_pgie_config.txt") \
		.withNVOsd() \
		.withRtspOutput() \
		.build()
	
	DeepLib.runOnMain(pipeline)

if __name__ == '__main__':
	sys.exit(main(sys.argv))
