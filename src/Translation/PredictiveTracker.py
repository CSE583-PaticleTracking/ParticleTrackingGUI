import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt
import os
import glob

from Translation.ParticleFinder import ParticleFinder_MHD

def Predictive_tracker(inputnames,threshold,max_disp,bground_name,minarea,invert,
        noisy,framerange,gifname,found,correct,yesvels):
    """
    Predictive_tracker(inputnames,threshold,max_disp,bground_name,minarea,invert,
        noisy,framerange,gifname,found,correct,yesvels)
        Predictive_tracker is a function that tracks particles in a video. 
        Given a movie of particle motions, PredictiveTracker produces Lagrangian 
        particle tracks using a predictive three-frame best-estimate algorithm. 
        The movie must be saved as a series of image files, an image stack in 
        .tif or .gif format, or an uncompressed .avi file; specify the movie in 
        "inputnames" (e.g., '0*.png' or 'stack.tif', or 'movie.avi'). To be 
        identified as a particle, a part of the image must have brightness that 
        differs from the background by at least "threshold". If invert==0, 
        PredictiveTracker seeks particles brighter than the background; if 
        invert==1, PredictiveTracker seeks particles darker than the background; 
        and if invert==-1, PredictiveTracker seeks any sort of contrast. The 
        background is read from the file "bground_name"; see BackgroundImage. If 
        minarea==1, PredictiveTracker seeks single-pixel particles by comparing 
        brightness to adjacent pixels (fast and good for small particles); 
        otherwise PredictiveTracker seeks particles having areas larger than 
        "minarea" (in square pixels; this method is better for tracking large 
        particles). Once identified, each particle is tracked using a kinematic 
        prediction, and a track is broken when no particle lies within "max_disp" 
        pixels of the predicted location. The results are returned in the 
        structure "vtracks", whose fields "len", "X", "Y", "T", "U", and "V" 
        contain the length, horizontal coordinates, vertical coordinates, times, 
        horizontal velocities, and vertical velocities of each track, 
        respectively. If minarea~=1, "vtracks" is returned with an additonal 
        field, "Theta", giving the orientation of the major axis of the particle 
        with respect to the x-axis, in radians. The total number of tracks is 
        returned as "ntracks"; the mean and root-mean-square track lengths are 
        returned in "meanlength" and "rmslength", respectively. If noisy~=0, the 
        movie is repeated with overlaid velocity quivers and the tracks are 
        plotted. If noisy==2, each movie frame is also saved to disk as an image. 
        Requires ParticleFinder.m; also requires read_uncompressed_avi.m for use 
        with .avi movies. This file can be downloaded from 
        http://leviathan.eng.yale.edu/software.
        
        Inputs:
            inputnames - name of the video file to be tracked
            threshold - threshold for finding particles
            max_disp - maximum displacement of particles between frames
            bground_name - name of the background image
            minarea - minimum area of particles
            invert - invert the image
            noisy - plot the tracks
            framerange - range of frames to be tracked
            gifname - name of the gif file
            found - dictionary of found particles
            correct - dictionary of correct particles
            yesvels - calculate velocities
        Outputs:
            vtracks - dictionary of tracks
        Examples:
            vtracks = Predictive_tracker(inputnames,threshold,max_disp,bground_name,minarea,invert,
            noisy,framerange,gifname,found,correct,yesvels)
        Dependencies:
            ParticleFinder_MHD
            """

    # Set defaults
    bground_name_default = 'background.tif'
    noisy_default = 0
    minarea_default = 1
    invert_default = -1
    pausetime = 1/33
    savedirname = 'tracksmovie'
    figsize = [1024, 512]
    framerange_default = [1,  np.inf]
    filterwidth = 1
    fitwidth = 3
    index_default = []
    found_default = []


    # Parse Inputs
    if bground_name is None:
        bground_name = bground_name_default
    if minarea is None:
        minarea = minarea_default
    if invert is None:
        invert = invert_default
    if noisy is None:
        noise = noisy_default
    if framerange is None:
        framerange = framerange_default
    elif len(framerange) == 1:
        framerange = framerange*[1, 1]
    if found is None:
        found = found_default
    if correct is None:
        correct = []
    if yesvels is None:
        yesvels = 1

    # Find Particles in all frames
    outputname = []
    x = None
    y = None
    t = None
    ang = None
    
    x,y,t,ang = ParticleFinder_MHD(inputnames,threshold,framerange,outputname,bground_name,minarea,invert,0)
    found = {'x':x, 'y':y, 't':t, 'ang':ang}
    tfound=t
    print(x)
    print(y)
    print(t)

    tt2 = np.arange(1, max(tfound)+1) 

    
    tt, beginsind = np.unique(tfound,return_index = True)
    
    
    t, endsind = np.unique(tfound,return_index = True)
    

    ends = np.ones_like(tt2)
    begins = ends.copy()

    ends = endsind
    begins = beginsind
    tt = tt2

    Nf = len(tt)

    if Nf < (2*fitwidth+1): 
        raise ValueError(f"Sorry, found too few files named: {inputnames}")

    # Setup array struct arrays for tracks
    ind = range(31)
    nparticles = len(ind)
    tracks = []
    if minarea == 1:
        for ii in range(nparticles):
            tracks[ii] = {'len':1, 'X':x[ind[ii]], 'Y':y[ind[ii]], 'T':1}
    else:
        for ii in range(nparticles):
            print("hello")
            print(x[ii])
            print(y[ii])
            tracks.append({'len':1, 'X':[x[ii]], 'Y':[y[ii]], 'T':[1], 'Theta': 0})
            print(tracks[ii])

    # Keep track of which tracks are active
    active = list(range(1, nparticles+1)) 
    n_active = len(active)
    print(f"Processed frame 1 of {Nf}")
    print(f"    Number of particles found: {nparticles}")
    print(f"    Number of active tracks: {n_active}")
    print(f"    Total number of tracks: {len(tracks)}")

    if not x.shape[0] == 1:
        x = x.T
    if not y.shape[0] == 1:
        y = y.T

    # Loop over frames
    for t in range(2, Nf+1): 

        time = tt[t-1]

    if begins[t-1] == 1 and t != 1:
        nfr1 = 0
        ind = []
    else:
       nfr1 = len(ind)

    if nfr1 == 0:
        print(f"Found no particles in frame {t}")
        

    fr1 = np.column_stack((x[ind], y[ind]))
    if minarea != 1:
        ang1 = []

    # Match the tracks with kinematic predictions
    now = np.zeros((n_active, 2))
    prior = np.zeros((n_active, 2))

    for ii in range(n_active):
        print(tracks[active[ii]-1])
        tr = tracks[active[ii]-1]
        now[ii, 0] = tr['X'][0]
        now[ii,1] = tr['Y'][0]
        if tr['len'] > 1:
            prior[ii, 1] = tr['X'][-2]
            prior[ii, 2] = tr['Y'][-2]
        else:
            prior[ii, :] = now[ii, :]
    
    velocity = now - prior

    estimate = now + velocity

    costs = np.zeros(n_active)
    links = np.zeros(n_active)

   
    if nfr1 > 0:
        for ii in range(n_active):
            dist_fr1 = np.sum((estimate[ii,:]-fr1)**2, axis = 1)
            costs[ii] = np.min(dist_fr1)
            if costs[ii] > max_disp**2:
                continue
            bestmatch = np.where(dist_fr1 == costs[ii])[0]
            if len(bestmatch) != 1:
                continue
            ind = links == bestmatch
            # if np.sum(ind) != 0:
                # if costs[ind] > costs[ii]:
                #     links[ind] = 0
                # else:
                #     continue
            links[ii] = bestmatch

        matched = np.zeros(nfr1)
        for ii in range(n_active):
            if links[ii] != 0:
                print(links[ii])
                tracks[active[ii] - 1]['X'].append(fr1[int(links[ii]),0])
                tracks[active[ii] - 1]['Y'].append(fr1[int(links[ii]),1])
                tracks[active[ii] - 1]['len'] += 1
                tracks[active[ii] - 1]['T'].append(int(time))
                matched[int(links[ii])] = 1
                

        unmatched = np.where(matched == 0)[0]
        if minarea == 1:
            for ii in range(len(unmatched)):
                newtracks = {'len':1, 'X':fr1[unmatched[ii],0], 'Y':fr1[unmatched[ii],1], 'T':time}
        else:
            for ii in range(len(unmatched)):
                newtracks = {'len':1, 'X':[fr1[unmatched[ii],0]], 'Y':[fr1[unmatched[ii],1]], 'T':[time], 'Theta':0}
    else:
        active = []
        newtracks = []
        unmatched = []
        
    active += list(range(len(tracks)+1, len(tracks)+len(newtracks)+1)) 
    print(tracks)
    print(newtracks)
    tracks.append(newtracks)
    n_active = len(active)
    print(tracks)

    print(f"Processed frame {t} of {Nf}")
    print(f"    Number of particles found: {nfr1}")
    print(f"    Number of active tracks: {n_active}")
    print(f"    Number of new tracks started here: {len(unmatched)}")
    print(f"    Number of tracks that found no match: {np.sum(links==0)}")
    print(f"    Total number of tracks: {len(tracks)}")

    vtracks = []
    print(len(tracks))
    
    if not yesvels:
        print("hello")
        for ii in range(len(tracks)):
            if tracks[ii]['len'] == 1:
                vtracks = tracks[ii]
        ntracks = len(vtracks)
        for ii in range(ntracks):
            meanlength = np.mean(vtracks[ii]['len'])
            rmslength = np.sqrt(np.mean(vtracks[ii]['len']**2))

    
    else:   

        # Prune tracks that are too short
        print("Pruning...")
        print(len(vtracks))
        for ii in range(len(tracks)):
            if tracks[ii]['len'] >= (2*fitwidth+1):
                tracks = tracks[ii]
        ntracks = len(tracks)
        for ii in range(ntracks):
            meanlength = np.mean(tracks[ii]['len'])
            rmslength = np.sqrt(np.mean(tracks[ii]['len']**2))

        print('Differentiating...')
        Av = 1.0 / (0.5 * filterwidth**2 * (np.sqrt(np.pi) * filterwidth * math.erf(fitwidth / filterwidth) - 2 * fitwidth * np.exp(-fitwidth**2 / filterwidth**2)))
        vkernel = np.arange(-fitwidth, fitwidth)
        vkernel = Av * vkernel * np.exp(-vkernel**2 / filterwidth**2)
    
        vtracks = []
        for ii in range(ntracks):
            u = -np.convolve(tracks[ii]['X'], vkernel, mode = 'valid')
            v = -np.convolve(tracks[ii]['Y'], vkernel, mode = 'valid')
            if minarea == 1:
                vtrack = {'len': tracks[ii]['len'] - 2*fitwidth,
                        'X':tracks[ii]['X'][fitwidth:-fitwidth], 
                        'Y':tracks[ii]['Y'][fitwidth:-fitwidth],
                        'T':tracks[ii]['T'][fitwidth:-fitwidth],
                        'U':u, 'V':v}
            else:
                print(tracks[ii]['X'])
                vtrack = {'len': tracks[ii]['len'] - 2*fitwidth,
                        'X':tracks[ii]['X'][0],
                        'Y':tracks[ii]['Y'][0],
                        'T':tracks[ii]['T'][0],
                        'U':u, 'V':v, 'Theta':tracks[ii]['Theta']}
            vtracks.append(vtrack)

    # Plotting if needed
    
    # if noisy:
    #     if isinstance(noisy, (int, float)) and noisy > 1:
    #         print(f"Plotting and saving frames.Please do not cover the figure window!")
    #         if not os.path.exists(savedirname):
    #             os.mkdir(savedirname)
    #     else:
    #         print("Plotting...")
    
    #     defaultpos = (0, 0)
    #     fig = plt.figure(figsize = figsize)
    #     ax = fig.add_axes([0, 0, 1, 1])
    #     ax.set_aspect('equal', 'box')
    #     plt.title(f"{ntracks} particle tracks: mean length {meanlength} frames, rms length {rmslength} frames")
    #     plt.xlabel(f"{inputnames}, threshold = {threshold}, max_disp = {max_disp}, {bground_name}, minarea = {minarea}, invert = {invert}")
    #     filepath, _, ext = os.path.splitext(inputnames)

    #     names = glob.glob(inputnames)
    
    #     if ext.lower() == '.avi':
    #         video = cv2.VideoCapture(names[0])
    #         ret, im = video.read()
        
    #     elif len(names) == 1 and ext.lower() == '.tif' or ext.lower() == '.tiff' or ext.lower() =='.gif':
    #         im = cv2.imread(names[0])
    #     else:
    #         im = cv2.imread(names[0]) #????????

    #     hi = ax.imshow(im)
    #     plt.xlim([0.5, im.shape[1]+.5])
    #     plt.ylim([0.5, im.shape[0]+.5])

    #     plt.set_cmap('gray')
    #     colorlist = ax.get_prop_cycle()
    #     Ncolors = len(colorlist)
    #     for vtrack in vtracks:
    #         framerange = np.array([vtrack['T'][0], vtrack['T'][-1]])
    
    #     for ii in range(0, Nf-fitwidth, 2):
    #         nump = 0
    #         ax.lines = []
    #         ind = np.where((framerange[:,0] <= ii+1) & (framerange[:, 1] >= ii+1))[0] 
        
    #         for jj in ind:
    #             col = colorlist[jj % Ncolors]['color']
    #             indt = slice(None, ii - int(framerange[jj, 0]) +1) #says to add a +1
    #             ax.plot(vtracks[jj]['X'][indt], vtracks[jj]['Y'][indt], '-', color = col)
    #             nump += 1
        
    #         if ext.lower() == '.avi':
    #             ret, im = video.read()
    #             hi.set_array(im)
            
    #         elif len(names) == 1 and ext.lower() =='.tif'  or ext.lower() == '.tiff' or ext.lower() =='.gif':
    #             hi.set_array(cv2.imread(names[ii+1]))
            
    #         else:
    #             hi.set_array(cv2.imread(names[ii+1]))

    #         plt.title(f"{nump} particles in {names[0]} ({ii+1} of {Nf}")
    #         plt.draw()
    #         plt.pause(pausetime)

    #         if isinstance(noisy, (int, float)) and noisy > 1:
    #             frame = plt.gca().get_frame()
    #             plt.savefig(os.path.join(filepath, savedirname, f"{names[ii +1]}"))
    #     if isinstance(noisy, (int, float)) and noisy > 1:
    #         video.release()
    #     plt.show()

    print("Done.")
    return vtracks
