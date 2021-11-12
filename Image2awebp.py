import argparse, sys, os, time
from PIL import Image

# Setup and parse command line arguments
parser = argparse.ArgumentParser(description="Program creates an animated .webp from a single input image by splitting it into four segments")
parser.add_argument("-I", "--input", help="Set input filepath. Supports .png and .jpg/.jpeg", required=True)
parser.add_argument("-O", "--output", help="Set output directory (Default = .\\Output\\)", default=str(os.path.dirname(__file__)) + "\\Output")
parser.add_argument("-D", "--duration", help="Set duration of frames in milliseconds (Default = 1ms)", default=1, type=int)
parser.add_argument("-C", "--crop", help="Set crop factor of each frame (Default = 100 = no crop)", default=100, type=int)

args = parser.parse_args()

print(("Using input file: %s") % (args.input))
print(("Output file: %s") % (args.output))
print(("Using frame duration: %sms") % (args.duration))
print(("Using crop factor: %s%%") % (args.crop))

# Load input image
try:
    fullImg = Image.open(args.input)
    print(fullImg.size[0])
    print(fullImg.size[1])
except:
    print("Error reading input file")
    sys.exit(2)

# Split image into four

# .crop(x1, y1, x2, y2)
# fullImg.size[0] = width
# fullImg.size[1] = height
frame1 = fullImg.crop(((fullImg.size[0]/2), (fullImg.size[1]/2), fullImg.size[0], fullImg.size[1]))
frame2 = fullImg.crop(((fullImg.size[0]/2), 0, fullImg.size[0], (fullImg.size[1]/2)))
frame3 = fullImg.crop((0, 0, (fullImg.size[0]/2), (fullImg.size[1]/2)))
frame4 = fullImg.crop((0, (fullImg.size[1]/2), (fullImg.size[0]/2), fullImg.size[1]))

# generate awebp

# save awebp to file