import numpy as np
from PIL import Image
import glob
import os
import cv2

def BackgroundImage(inputnames, outputname='background.tif'):
    """
    Given a sequence of images or a video file, calculates the mean pixel values
    over time and saves the result as an image.
    """
    files = glob.glob(inputnames)
    if not files:
        raise ValueError(f"No files found for the pattern {inputnames}")
    
    # Determine the type of input (image sequence, tiff stack, or avi video)
    if files[0].endswith('.avi'):
        # Reading AVI file
        cap = cv2.VideoCapture(files[0])
        Nf = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        _, frame = cap.read()
        bg0 = np.zeros_like(frame, dtype=np.float32)
        for _ in range(Nf):
            _, frame = cap.read()
            bg0 += frame
        cap.release()
    elif files[0].endswith(('.tif', '.tiff', '.gif')):
        # Reading TIFF/GIF stack
        im = Image.open(files[0])
        Nf = im.n_frames
        bg0 = np.zeros((im.height, im.width, 3), dtype=np.float32)
        for i in range(Nf):
            im.seek(i)
            bg0 += np.array(im)
    else:
        # Reading a sequence of images
        Nf = len(files)
        im = Image.open(files[0])
        bg0 = np.zeros((im.height, im.width, 3), dtype=np.float32)
        for file in files:
            im = Image.open(file)
            bg0 += np.array(im)

    # Calculate the mean
    bg = np.round(bg0 / Nf).astype(np.uint8)

    # Convert to grayscale if needed
    if bg.shape[2] == 3:
        bg = np.mean(bg, axis=2).astype(np.uint8)

    # Save the result
    Image.fromarray(bg).save(outputname)

#BackgroundImage('path/to/images/*.png')