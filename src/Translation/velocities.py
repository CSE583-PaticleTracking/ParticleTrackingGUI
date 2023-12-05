import numpy as np
import matplotlib.pyplot as plt

def velocities(vtracks, framerange=[-np.inf, np.inf], noisy=0):
    """
    Converts velocity tracks to velocities and plots if noisy is not 0.
    vtracks: Input data in structured format.
    framerange: Range of frames to consider.
    noisy: Controls plotting, 0 means no plot.
    """

    if not vtracks:
        raise ValueError("Input does not appear to contain tracks.")
    
    Nall = sum(len(track['len']) for track in vtracks)
    u = np.full(Nall, np.nan)
    v = np.full(Nall, np.nan)
    x = np.full(Nall, np.nan)
    y = np.full(Nall, np.nan)
    t = np.full(Nall, np.nan)
    tr = np.full(Nall, np.nan)

    pos = 0
    for ii, track in enumerate(vtracks):
        ind = (track['T'] >= min(framerange)) & (track['T'] <= max(framerange))
        Np = np.sum(ind)
        range_slice = slice(pos, pos + Np)
        u[range_slice] = track['U'][ind]
        v[range_slice] = track['V'][ind]
        x[range_slice] = track['X'][ind]
        y[range_slice] = track['Y'][ind]
        t[range_slice] = track['T'][ind]
        tr[range_slice] = ii
        pos += Np


    # Removing unwanted frames
    valid_indices = ~np.isnan(u)
    u, v, x, y, t, tr = u[valid_indices], v[valid_indices], x[valid_indices], y[valid_indices], t[valid_indices], tr[valid_indices]

    # Sorting by time
    sorted_indices = np.argsort(t)
    u, v, x, y, t, tr = u[sorted_indices], v[sorted_indices], x[sorted_indices], y[sorted_indices], t[sorted_indices], tr[sorted_indices]

    # Plot if noisy is true
    #If noisy is not zero, the function proceeds to plot the data using Matplotlib's quiver function.
    #The quiver plot visually represents the velocity vectors at each particle's position.
    #The aspect ratio is set to equal, and the plot is adjusted to be tight around the data.
    #The plot title is set based on the range of frames considered.
    if noisy:
        plt.figure()
        plt.quiver(x, y, u, v)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('tight')
        if framerange[0] == framerange[1]:
            title_str = f"{len(x)} particles in frame {framerange[0]}"
        else:
            if np.isinf(framerange[0]):
                framerange[0] = t[0]
            if np.isinf(framerange[1]):
                framerange[1] = t[-1]
            title_str = f"{len(x)} particles in frames {min(framerange)} to {max(framerange)}"
        plt.title(title_str)
        plt.show()


    return u, v, x, y, t, tr
