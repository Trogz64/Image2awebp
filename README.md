# Image2awebp

A script to turn a single image into an animated .webp file by splitting the image into four frames.

Frames are in the order:

1. Bottom Right

2. Top Right

3. Top Left

4. Bottom Left

---

## Usage

```txt
Image2awebp.py [-h] -I INPUT [-O OUTPUT] [-D DURATION] [-C CROP]

optional arguments:
  -h, --help            show this help message and exit
  
  -I INPUT, --input INPUT
                        Set input filepath
  
  -O OUTPUT, --output OUTPUT
                        Set output directory
  
  -D DURATION, --duration DURATION
                        Set duration of frames in milliseconds

  -C CROP, --crop CROP  Set crop factor of each frame (100 == no crop)
```

### Examples

- Provide an input image and leave all the other settings as the default

```sh
Image2awebp.py --input "inputImage.jpg"
```

- Provide an input image, set the duration of each fram to 3ms and set the crop factor to 90%

```sh
Image2awebp.py -I "inputImage.jpg" -D 3 -C 90
```

- Provide an input image, set the output directory, and leave the other settings as default

```sh
Image2awebp.py -I "inputImage.jpg" --output "C:\Users\outputDir"
```

---

## Dependencies

- Requires [Python](https://www.python.org/) version 3.5.3 or higher
