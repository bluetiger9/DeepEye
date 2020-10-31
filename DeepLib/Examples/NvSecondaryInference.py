import sys
sys.path.append('..')

from DeepLib import *

def main(args):
	# Check input arguments
	if len(args) != 2:
		sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
		sys.exit(1)

	DeepLib.init()

	pipeline = DeepLib() \
		.pipeline() \
		.withFileInput(args[1]) \
		.withNVInfer("dstest2_pgie_config.txt") \
		.withNVTracker("dstest2_tracker_config.txt") \
		.withNVInfer("dstest2_sgie1_config.txt") \
		.withNVInfer("dstest2_sgie2_config.txt") \
		.withNVInfer("dstest2_sgie3_config.txt") \
		.withNVOsd() \
		.withRtspOutput() \
		.build()
	
	DeepLib.runOnMain(pipeline)

if __name__ == '__main__':
	sys.exit(main(sys.argv))
