import argparse, sys, os, time, ntpath
from tempfile import tempdir
from PIL import Image
from PIL import features
from vidstab import VidStab
import cv2
import numpy as np

# Setup and parse command line arguments
parser = argparse.ArgumentParser(description="Program creates an animated .webp from a single input image by splitting it into four segments")
parser.add_argument("-I", "--input", help="Set input filepath. Supports .png, .jpg/.jpeg, and .tiff", required=True)
parser.add_argument("-O", "--output", help="Set output directory (Default = .\\Output)", default=str(os.path.dirname(__file__)) + "\\Output")
parser.add_argument("-D", "--duration", help="Set duration of frames in milliseconds (Default = 200ms)", default=200, type=int)
parser.add_argument("-C", "--crop", help="Set the crop factor of each frame (Applied before stabilisation) (Default = 100 = no crop)", default=100, type=int)
parser.add_argument("-S", "--stabilise", help="Use AI to stabilise the frames", action="store_true")
parser.add_argument("-R", "--border", help="Size of border in output. Positive values pad, negative values crop (Default = 0)", default=0, type=int)
parser.add_argument("-G", "--gif", help="Save the animation as a .gif file instead of .webp", action="store_true")
parser.add_argument("-B", "--boomerang", help="Use 'boomerang' style looping", action="store_true")

args = parser.parse_args()

print(("Using input file: %s") % (args.input))
print(("Output directory: %s") % (args.output))
print(("Using frame duration: %sms") % (args.duration))
print(("Using crop factor: %s%%") % (args.crop))
if args.stabilise:
    print(("Stabilisation with a border size of: %s") % (args.border))
else:
    print("No stabilisation")

if args.gif:
    print("Saving as .gif")
else:
    print("Saving as .webp")

if args.boomerang:
    print("Using 'boomerang' style looping")
else:
    print("Using traditional style looping")

# Load input image
try:
    fullImg = np.array(Image.open(args.input))
except Exception as ex:
    print("ERROR - " + str(ex))
    sys.exit(2)

# Check output does not end in a slash and remove if it does
if args.output[-1] == '\\' or args.output[-1] == '/':
    args.output = args.output[:-1]
    print(args.output)

# Check output is a directory and if not, create it
if os.path.isfile(args.output):
    print("ERROR - Output must be a directory, not a file.")
    sys.exit(2)

if args.crop < 0 or args.crop > 100:
    print("ERROR - Crop factor must be between 0 and 100")
    sys.exit(2)

if not os.path.isdir(args.output):
    os.makedirs(args.output)

# Split image into four

# Pillow
# 0,0 = upper left
# Image.crop(x1, y1, x2, y2)
# Image.crop(left, upper, right, lower)
# Image.size[0] = width
# Image.size[1] = height

# numpy
# 0,0 = upper left
# img[y1:y2, x1:x2]
# x1,y1 = left,upper | x2,y2 = right,lower
# img.shape[0] = height
# img.shape[1] = width
subImgWidth = (fullImg.shape[1] / 2) * (args.crop / 100)
subImgHeight = (fullImg.shape[0] / 2) * (args.crop / 100)
xOffset = ((fullImg.shape[1] / 2) - subImgWidth) / 2
yOffset = ((fullImg.shape[0] / 2) - subImgHeight) / 2

# Top Left
# frame1 = fullImg.crop((xOffset, yOffset, xOffset + subImgWidth, yOffset + subImgHeight))
frame1 = fullImg[int(yOffset):int(yOffset + subImgHeight), int(xOffset):int(xOffset + subImgWidth)].copy()
# Bottom Left
# frame2 = fullImg.crop((xOffset, (fullImg.shape[0]/2) + yOffset, xOffset + subImgWidth, (fullImg.shape[0]/2) + yOffset + subImgHeight))
frame2 = fullImg[int((fullImg.shape[0]/2) + yOffset):int((fullImg.shape[0]/2) + yOffset + subImgHeight), int(xOffset):int(xOffset + subImgWidth)].copy()
# Bottom Right
# frame3 = fullImg.crop(((fullImg.shape[1]/2) + xOffset, (fullImg.shape[0]/2) + yOffset, (fullImg.shape[1]/2) + xOffset + subImgWidth, (fullImg.shape[0]/2) + yOffset + subImgHeight))
frame3 = fullImg[int((fullImg.shape[0]/2) + yOffset):int((fullImg.shape[0]/2) + yOffset + subImgHeight), int((fullImg.shape[1]/2) + xOffset):int((fullImg.shape[1]/2) + xOffset + subImgWidth)].copy()
# Top Right
# frame4 = fullImg.crop(((fullImg.shape[1]/2) + xOffset, yOffset, (fullImg.shape[1]/2) + xOffset + subImgWidth, yOffset + subImgHeight))
frame4 = fullImg[int(yOffset):int(yOffset + subImgHeight), int((fullImg.shape[1]/2) + xOffset):int((fullImg.shape[1]/2) + xOffset + subImgWidth)].copy()

# Create sequences
if args.boomerang:
    sequence = [frame1, frame2, frame3, frame4, frame3, frame2]
else:
    sequence = [frame1, frame2, frame3, frame4]
    
# Stabilise frames if selected
if args.stabilise:
    # Setup stabilisation
    stabiliser = VidStab()

    outSequence = []
    for frame in sequence:
        # Stabilise the frame
        stabFrame = stabiliser.stabilize_frame(input_frame=frame, border_type="black", border_size=args.border, smoothing_window=1)
        # Need to bin first frame from the stabiliser as it will be a black frame
        if frame is frame1:
            # Convert stabilised frame to pillow format and append to the output sequence
            outSequence.append(Image.fromarray(np.uint8(frame)).convert('RGB'))
        else:
            # Convert stabilised frame to pillow format and append to the output sequence
            outSequence.append(Image.fromarray(np.uint8(stabFrame)).convert('RGB'))
else:
    outSequence = []
    for frame in sequence:
        # Convert frames to pillow format and append to the output sequence
        outSequence.append(Image.fromarray(np.uint8(frame)).convert('RGB'))

# generate and save awebp/gif to the output dir
if args.gif:
    outPath = args.output + "\\" + ntpath.basename(args.input.split(".")[0]) + "_Animation.gif"
else:
    outPath = args.output + "\\" + ntpath.basename(args.input.split(".")[0]) + "_Animation.webp"

outSequence[0].save(outPath, save_all = True, append_images = outSequence[1:], duration = args.duration, loop = 0)
print("File saved to " + outPath)