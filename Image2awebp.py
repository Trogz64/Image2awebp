import argparse, sys, os, time

parser = argparse.ArgumentParser(description="Program creates an animated .webp from a single input image by splitting it into four segments")
parser.add_argument("-I", "--input", help="Set input filepath", required=True)
parser.add_argument("-O", "--output", help="Set output filepath", default=str(os.path.dirname(__file__)) + "\\Output\\" + str(round(time.time() * 1000)) + ".webp")
parser.add_argument("-D", "--duration", help="Set duration of frames in milliseconds", default=1, type=int)
parser.add_argument("-C", "--crop", help="Set crop factor of each frame (100 == no crop)", default=100, type=int)

args = parser.parse_args()

print(("Using input file: %s") % (args.input))
print(("Output file: %s") % (args.output))
print(("Using frame duration: %sms") % (args.duration))
print(("Using crop factor: %s%%") % (args.crop))