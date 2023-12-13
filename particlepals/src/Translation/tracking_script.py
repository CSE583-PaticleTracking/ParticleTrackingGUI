
import cv2
import matplotlib.pyplot as plt
from PredictiveTracker import Predictive_tracker
from velocities import velocities
from plottracks import plot_tracks_avi
import numpy as np

inputname = '/Users/mohankukreja/Documents/ParticleTrackingGUI/src/Translation/testtracks.avi'

vid = cv2.VideoCapture(inputname)

if not vid.isOpened():
    print("Error opening video file")
    exit()


frame_num = 0
vid.set(cv2.CAP_PROP_POS_FRAMES, frame_num)  # Frame numbering starts at 0 in cv2
success, img = vid.read()

# if success:
#     # Plot one frame
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.axis('off')  # Turn off axis numbers
#     plt.show()
# else:
#     print("Error reading frame")
#     exit()

threshold = 40
max_disp = 8
bground_name = []
minarea = 2
invert = 0
framerange = range(11,20)

vtracks = Predictive_tracker(inputname, threshold, max_disp, bground_name, minarea, invert, None, framerange, None, None, None, None)
print(vtracks)
u,v,x,y,t, tr=velocities(vtracks, framerange);

if not framerange:
    images2plot = range(int(vid.get(cv2.CAP_PROP_FRAME_COUNT)))  # All frames
else:
    images2plot = range(framerange[0], framerange[1] + 1)

# Plotting particles
for i in images2plot:
    vid.set(cv2.CAP_PROP_POS_FRAMES, i)
    success, frame = vid.read()
    if success:
        plt.figure(2)
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        # Find and scatter particles
        part = np.where(t == i)[0]
        plt.scatter(x[part], y[part], c='r', marker='o')

        plt.pause(0.1)  # Pause in seconds
        plt.clf()


plot_tracks_avi(inputname, vtracks, framerange)
