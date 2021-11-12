import argparse, sys, os, time, ntpath
from PIL import Image
from PIL import features

# Setup and parse command line arguments
parser = argparse.ArgumentParser(description="Program creates an animated .webp from a single input image by splitting it into four segments")
parser.add_argument("-I", "--input", help="Set input filepath. Supports .png, .jpg/.jpeg, and .tiff", required=True)
parser.add_argument("-O", "--output", help="Set output directory (Default = .\\Output)", default=str(os.path.dirname(__file__)) + "\\Output")
parser.add_argument("-D", "--duration", help="Set duration of frames in milliseconds (Default = 200ms)", default=200, type=int)
parser.add_argument("-C", "--crop", help="Set crop factor of each frame (Default = 100 = no crop)", default=100, type=int)
parser.add_argument("-G", "--gif", help="Save the animation as a .gif file instead of .webp", action="store_true")

args = parser.parse_args()

print(("Using input file: %s") % (args.input))
print(("Output directory: %s") % (args.output))
print(("Using frame duration: %sms") % (args.duration))
print(("Using crop factor: %s%%") % (args.crop))

# Load input image
try:
    fullImg = Image.open(args.input)
except:
    print("Error reading input file")
    sys.exit(2)

# Check output does not end in a slash and remove if it does
if args.output[-1] == '\\' or args.output[-1] == '/':
    args.output = args.output[:-1]
    print(args.output)

# Check output is a directory and if not, create it
if os.path.isfile(args.output):
    print("Output must be a directory, not a file.")
    sys.exit(2)

if not os.path.isdir(args.output):
    os.makedirs(args.output)

# Split image into four

# Image.crop(x1, y1, x2, y2)
# Image.size[0] = width
# Image.size[1] = height
frame1 = fullImg.crop(((fullImg.size[0]/2), (fullImg.size[1]/2), fullImg.size[0], fullImg.size[1]))
frame2 = fullImg.crop(((fullImg.size[0]/2), 0, fullImg.size[0], (fullImg.size[1]/2)))
frame3 = fullImg.crop((0, 0, (fullImg.size[0]/2), (fullImg.size[1]/2)))
frame4 = fullImg.crop((0, (fullImg.size[1]/2), (fullImg.size[0]/2), fullImg.size[1]))

#TODO Implement crop functionality

# generate and save awebp/gif to file

sequence = [frame1, frame2, frame3, frame4]
if args.gif:
    sequence[0].save((args.output + "\\" + ntpath.basename(args.input.split(".")[0]) + "_Animation.gif"), save_all = True, append_images = sequence[1:], duration = args.duration, loop = 0)
    print("File saved to " + args.output + "\\" + ntpath.basename(args.input.split(".")[0]) + "_Animation.gif")
else:
    sequence[0].save((args.output + "\\" + ntpath.basename(args.input.split(".")[0]) + "_Animation.webp"), save_all = True, append_images = sequence[1:], duration = args.duration)
    print("File saved to " + args.output + "\\" + ntpath.basename(args.input.split(".")[0]) + "_Animation.webp")