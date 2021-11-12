# Image2awebp

A script to turn a single image into an animated .webp (or .gif) file by splitting the image into four frames.

Frames are in the order:

1. Bottom Right

2. Top Right

3. Top Left

4. Bottom Left

---

## Supported File Types

The program has been tested with:

- .png

- .jpg

- .tiff

The program uses the [Pillow](https://pillow.readthedocs.io/en/stable/installation.html) `Image.load()` method, so other image filetypes may be supported.

---

## Usage

```txt
Image2awebp.py [-h] -I INPUT [-O OUTPUT] [-D DURATION] [-C CROP]

optional arguments:
  -h, --help            show this help message and exit

  -I INPUT, --input INPUT
                        Set input filepath. Supports .png, .jpg/.jpeg, and .tiff
  
  -O OUTPUT, --output OUTPUT
                        Set output directory (Default = .\Output)
  
  -D DURATION, --duration DURATION
                        Set duration of frames in milliseconds (Default = 200ms)
  
  -C CROP, --crop CROP  Set crop factor of each frame (Default = 100 = no crop)

  -G, --gif             Save the animation as a .gif file instead of .webp
```

### Examples

- Provide an input image and leave all the other settings as the default

```sh
Image2awebp.py --input "inputImage.jpg"
```

- Provide an input image, set the duration of each frame to 100ms and set the crop factor to 90%

```sh
Image2awebp.py -I "inputImage.jpg" -D 100 -C 90
```

- Provide an input image, set the output directory, and leave the other settings as default

```sh
Image2awebp.py -I "inputImage.png" --output "C:\Users\outputDir"
```

- Provide an input image, set the duration of each frame to 250ms, and save the animation as a .gif

```sh
Image2awebp.py -I "InputImage.tiff" -G --duration 250
```

---

## Dependencies

- Requires [Python](https://www.python.org/) version 3.5.3 or higher

- Requires [Pillow](https://pillow.readthedocs.io/en/stable/installation.html) version 8.2.0 or higher

---

## TODO

- Implement crop functionality
