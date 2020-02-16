import sys
sys.path.append('..')

import * from DeepLib

def main(args):
	# Check input arguments
	if len(args) != 2:
		sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
		sys.exit(1)

	pipeline = DeepLib() \
	 	.pipeline() \
		.withFileSource(args[1]) \
		.withRtspOutput() \
		.build()

	DeepLib.runOnMain(pipeline)

if __name__ == '__main__':
	sys.exit(main(sys.argv))