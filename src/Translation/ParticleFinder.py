import os
import sys
from PIL import Image
import cv2
import numpy as np
import struct
import glob
from skimage import measure, morphology

def ParticleFinder_MHD(inputnames, threshold, framerange=None, outputname=None, bground_name=None, arealim=None, invert=None, noisy=None):
    # Default values
    framerange_default = [1, float('inf')]  # by default, all frames
    bground_name_default = 'background.tif'
    noisy_default = 0  # don't plot unless requested
    arealim_default = 1
    invert_default = -1  # by default, use absolute contrast
    pausetime = 1/30  # seconds to pause between frames when plotting
    savedirname = 'particlesmovie'
    barsize = 8  # if interested in angle, plot particles as rods 5 px long

    # Check for necessary parameters
    if inputnames is None or threshold is None:
        raise ValueError("Usage: [x,y,t,ang] = ParticleFinder_MHD(inputnames, threshold, [framerange], [outputname], [bground_name], [arealim], [invert], [noisy])")

    # Assign default values if parameters are not provided
    framerange = framerange if framerange is not None else framerange_default
    if len(framerange) == 1:
        framerange = [framerange[0], framerange[0]]

    bground_name = bground_name if bground_name is not None else bground_name_default
    arealim = arealim if arealim is not None else arealim_default
    invert = invert if invert is not None else invert_default
    noisy = noisy if noisy is not None else noisy_default

    writefile = outputname is not None

    filepath, ext = os.path.splitext(inputnames)
    names = glob.glob(inputnames)

    if ext.lower() == '.avi':
        movtype = 'avi'
        v = cv2.VideoCapture(os.path.join(filepath, names[0]))
        color_depth = 8  # Default assumption

        ret, frame = v.read()
        if frame.dtype == np.uint8:
            color_depth = 2**8

        ht, wd, _ = frame.shape
        tmin = max(framerange[0], 1)
        tmax = min(framerange[1], int(v.get(cv2.CAP_PROP_FRAME_COUNT)))

    elif len(names) == 1 and ext.lower() in ['.tif', '.tiff', '.gif']:
        movtype = 'stack'
        im = Image.open(os.path.join(filepath, names[0]))
        color_depth = 2**im.bits
        ht, wd = im.size
        tmin = max(framerange[0], 1)
        tmax = min(framerange[1], im.n_frames)

    Nf = tmax - tmin + 1

    if arealim == 1:
        logs = np.log(np.arange(1, color_depth + 1))
        logs = np.insert(logs, 0, np.log(0.0001))
    else:
        logs = []
    

     
    background = np.array(Image.open(bground_name))

    # Convert RGB to grayscale if necessary
    if len(background.shape) == 3:
        background = np.round(np.mean(background, axis=2)).astype(np.uint8)

    N = 0
    x, y, t = [], [], []
    ang = []

    memloc = 0
    for ii in range(tmax):  # Loop over frames
        if arealim > 1:
            pos, ang1 = FindRegions(im, threshold, arealim)
        else:
            pos = FindParticles(im, threshold, logs)
            ang1 = []

        N = pos.shape[0]
        if ii == 0:  # First frame, pre-allocate arrays for speed
            x = np.full(N * Nf, np.nan)
            y = np.full(N * Nf, np.nan)
            t = np.full(N * Nf, np.nan)
            if arealim != 1:
                ang = np.full((N * Nf, 9), np.nan)  # Additional properties

        if N > 0:
            x[memloc:memloc + N] = pos[:, 0]
            y[memloc:memloc + N] = pos[:, 1]
            if arealim != 1:
                ang[memloc:memloc + N] = ang1
            memloc += N

        if ii % 25 == 0:  # Display progress every 25 frames
            print(f'Found {N} particles in frame {ii + 1} of {Nf}.')

        lastind = ii

    # Trim the arrays to the actual size
    x, y, t = x[:memloc], y[:memloc], t[:memloc]
    if arealim != 1:
        ang = ang[:memloc]

    # Sort by time
    I = np.argsort(t)
    x, y, t = x[I], y[I], t[I]
    if arealim != 1:
        ang = ang[I]
    else:
        ang = []

    print('Done.')


def FindParticles(im, threshold, logs):
    s = im.shape

    # Identify the local maxima that are above the threshold
    maxes = np.argwhere((im >= threshold) &
                        (im > np.roll(im, 1, axis=1)) &
                        (im > np.roll(im, -1, axis=1)) &
                        (im > np.roll(im, 1, axis=0)) &
                        (im > np.roll(im, -1, axis=0)))

    # Throw out unreliable maxes in the outer ring
    good = (maxes[:, 0] != 0) & (maxes[:, 1] != 0) & (maxes[:, 0] != s[0] - 1) & (maxes[:, 1] != s[1] - 1)
    maxes = maxes[good]

    # Find the horizontal and vertical positions
    x, y = maxes[:, 0], maxes[:, 1]

    # Look up the logarithms of the relevant image intensities
    z1 = logs[im[np.clip(x-1, 0, s[0]-1), y] + 1]
    z2 = logs[im[x, y] + 1]
    z3 = logs[im[np.clip(x+1, 0, s[0]-1), y] + 1]

    # Compute the centers
    xcenters = -0.5 * (z1 * (-2*x - 1) + z2 * (4*x) + z3 * (-2*x + 1)) / (z1 + z3 - 2*z2)
    z1 = logs[im[x, np.clip(y-1, 0, s[1]-1)] + 1]
    z3 = logs[im[x, np.clip(y+1, 0, s[1]-1)] + 1]
    ycenters = -0.5 * (z1 * (-2*y - 1) + z2 * (4*y) + z3 * (-2*y + 1)) / (z1 + z3 - 2*z2)

    # Make sure we have no bad points
    good = np.isfinite(xcenters) & np.isfinite(ycenters)

    # Fix up the coordinate system (to match MATLAB's system)
    pos = np.column_stack((ycenters[good], xcenters[good]))

    return pos


def FindRegions(im, threshold, arealim, debug=False):
    if isinstance(arealim, int) or isinstance(arealim, float):
        arealim = [arealim, np.inf]  # Assume single size is a minimum

    s = im.shape
    inm = im > threshold
    inm = morphology.remove_small_objects(inm, min_size=arealim[0])

    props = measure.regionprops_table(inm.astype(int), intensity_image=im, 
                                      properties=('centroid', 'area', 'mean_intensity', 
                                                  'max_intensity', 'orientation', 
                                                  'major_axis_length', 'minor_axis_length', 
                                                  'weighted_centroid', 'perimeter'))

    props = np.array([props[key] for key in props.keys()]).T  # Convert dict to array

    # Check if weighted centroid should be used
    weightedcentroid = True
    if weightedcentroid:
        pos = props[:, -2:]  # Weighted centroid
    else:
        pos = props[:, :2]  # Normal centroid

    # Filtering regions based on area limits and removing regions on the edge
    good = np.logical_and.reduce([pos[:, 0] != 1, pos[:, 1] != 1, 
                                  pos[:, 0] != s[1], pos[:, 1] != s[0], 
                                  props[:, 1] > arealim[0], props[:, 1] < arealim[1]])

    pos = pos[good]
    ang = props[good]

    # Debugging visualization (optional)
    if debug:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 10))
        plt.imshow(im, cmap='gray')
        plt.scatter(pos[:, 1], pos[:, 0], c='r')
        plt.show()

    return pos, ang