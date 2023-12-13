import cv2
import matplotlib.pyplot as plt
import numpy as np

def plot_tracks_avi(inputname, vtracks, framerange=None):
    # Read the video
    vid = cv2.VideoCapture(inputname)

    if framerange is None:
        framerange = [1, int(vid.get(cv2.CAP_PROP_FRAME_COUNT))]
    
    # Color list from current color cycle
    colorlist = plt.rcParams['axes.prop_cycle'].by_key()['color']

    ntracks = len(vtracks)
    track_frame_range = np.full((ntracks, 2), np.nan)

    print(ntracks)
    print(vtracks)
    for jj in range(ntracks):
        track_frame_range[jj, 0] = vtracks[jj]['T']
        track_frame_range[jj, 1] = vtracks[jj]['T']

    first_track = np.nanmin(track_frame_range)
    last_track = np.nanmax(track_frame_range)
    print(framerange[0])
    print(framerange[1] + 1)
    print(last_track)
    for i in range(int(first_track), int(last_track)):
        if i < first_track or i > last_track:
            continue

        vid.set(cv2.CAP_PROP_POS_FRAMES, i - 1)
        ret, frame = vid.read()

        if not ret:
            break

        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.title(f'frame {i}')
        plt.axis('image')

        for jj in range(ntracks):
            if track_frame_range[jj, 0] <= i <= track_frame_range[jj, 1]:
                col = colorlist[jj % len(colorlist)]
                indt = slice(0, i - int(track_frame_range[jj, 0]) + 1)
                plt.plot(vtracks[jj]['X'], vtracks[jj]['Y'], '-', color=col)

        plt.pause(0.5)
        plt.clf()

    vid.release()

    # plot_tracks_avi('video.avi', vtracks, [5, 10])
