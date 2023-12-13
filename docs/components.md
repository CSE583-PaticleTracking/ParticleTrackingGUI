# GUI

### Overview
The GUI Component is responsible for creating the user interface that allows users to interact with the application. It provides a visual representation of the software's features and enables users to input data, analyze data, view results, and control the software's functionality.

### What it does:
- Renders user interface elements, such as windows, forms, buttons, input fields, and menus.
- Manages user interactions, including mouse clicks, keyboard inputs, and touch gestures.
- Displays real-time analysis, updates, notifications, and feedback to the user.
- Validates and processing user inputs.
- Ensures accessibility and responsive design for various devices and screen sizes.

### imputs:
- User imput

### output

### How use other components
- Import data
- Particle tracking
- Vector analysis
- Export data



# Load Data

### Overview
The Load Data Component is designed to import external data into the software system, making it available for further processing and analysis. It plays a critical role in ensuring that the software has access to up-to-date and relevant data, which is essential for its functionality.

### What it does: 
- Retrieves data based on defined queries or parameters.
- Detects file format
    - Only .png, .jpeg, .tiff, .seq for images, .avi, .mov for movies, .csv for vector fields
- Loads the data into the software's data storage.
- Shows a sample (few frames) of the images, vector field
    - Only shows a few frames to avoid lagging.
- Transforms and prepares the data for consumption within the software.
- Store it in a local memory
    - Either address or actual images

### imputs:
- File format
- Actual file (image)
- Metadata (csv)

### output
- Transformed data
- Warning message if incorrect data

### How use other components
- GUI
- Particle tracking
- Vector analysis 

# Particle tracking

### Overview
The Particle Tracking Component is designed to track the movement and characteristics of particles or objects within a specified system. It plays a critical role in analyzing and visualizing particle trajectories, enabling various scientific, industrial, and research applications.

### What it does:
- Detects and identifies individual particles or objects within a system.
- Tracks the position and motion of particles over time.
- Analyzes and measures parameters, such as velocity, acceleration, and interactions between particles.
- Provides visualizations, reports, and data output for further analysis.

### Design and architecture
The Particle Tracking Component may follow various tracking algorithms and data processing techniques, depending on the specific use case. It is typically modular and extensible to accommodate different tracking methods.

### imputs:
- User data.
- Future: Sensors, cameras, simulation data, or external devices.
### output 
- file storage, or visualization tools.

### How use other components
- GUI
- Load data
- Export data

## ParticleFinder

### What it does :
- Binarizes images 
- Uses given inputs to identify particles
- Finds particle centorid positions in an image

### Inputs : 
- Images
- A given color threshold
- Area limit the particles can occupy

### Outputs
- Found particles and their centroid coordinate in px

## Predictive Tracker

### What it does : 
- Uses particles centroids in subsequent frames to create tracks
- Particles are connected with their likely next position in the following frame
- Tracks are used to define the position of an object through whole video

### Inputs : 
- Max distance a particle can move between frames
- Centroid positions
- Number of Frames

### Outputs : 
- Particle tracks through a given frame range


# Vector Field Statistics

### Overview
The Vector Field Statistics Component is designed to compute and analyze statistical properties of vector fields, aiding in the understanding and interpretation of complex data distributions. It is a fundamental tool for a wide range of applications, including fluid dynamics, environmental modeling, and data analysis.

### What it does:
- Computation of vector field properties, including mean, variance, divergence, and curl.
- Visualization of vector field statistics through contour plots, streamlines, and other graphical representations.
- Integration with other software components to support broader data analysis and modeling.

### Design and architecture
The Vector Field Statistics Component may follow various statistical algorithms and data processing techniques, depending on the specific use case. It is typically modular and extensible to accommodate different statistical analysis methods.

### inputs:
- Transformed data.

### output 
- file storage, or visualization tools.

### How use other components
- GUI
- Load data
- Export data

## Extract and check consecutive numbers
### what it does
Extracts numbers from CSV file names in the given directory and checks if the numbers are consecutive. Checks: if the directory does not exist, if no CSV files are found in the directory, and if no frame numbers are found in the file names. Raises a warning if the extracted numbers are not consecutive or if there are missing numbers.

### Inputs
- The path to the directory containing CSV files with frame numbers in their names.

 ### Outputs
 - Frame numbers  

## Read CSV files
### What it does
It reads a CSV file and extracts the x and y positions, and u and v velocities. 
    
### Input:
- The path to the CSV file.
    
### Output:
- A 1D array containing x positions.
- A 1D array containing y positions.
- A 1D array containing u velocities.
- A 1D array containing v velocities. 

## Reshape CSV file
### What it does
It reshapes the extracted data into a grid for further processing in Python.
    
### Input:
- A 1D array containing x positions.
- A 1D array containing y positions.
- A 1D array containing u velocities.
- A 1D array containing v velocities.
    
### Output:
- A 2D array containing x positions.
- A 2D array containing y positions.
- A 2D array containing u velocities.
- A 2D array containing v velocities. 

## Process CSV files in folder
### What it does
It processes all CSV files in a folder located in the original folder. It performs any processing that you want to do on the data. The user inputs which vector operation to be performed. Analyze each frame and plot the processed frame at each step.

The processed data is saved in a new folder located in the original folder. The name of the new folder is the same as the original folder with the suffix '_processed_'and the date. The processed data is saved with the same name files. It attaches a csv file with the metadata of the processed data. It also attaches a csv file with a list of the processes/operations performed on the data.

### Inputs:
- Path to the folder containing the CSV files.
    
### Outputs:
- New folder with processed csv files, metadata, and list of operations performed.

## Export Data

### Overview
The Export Data Component is designed to enable users to export data from the software for external use, analysis, or sharing. It provides a flexible and user-friendly way to extract and save data in various formats and destinations.

### What it does:
- Allows users to select data for export, specifying data ranges, filters, and formats.
- Supports a variety of export formats like CSV and Excel.

### imputs:
- Transformed and/or processed data.

### output 
- csv/Excel output file.

### How use other components
- GUI
- Particle Tracking
- Vector Analysis
- Export data

## Operate on grid
### What it does
- Perform addition, subtraction, multiplication, or division of a vector on a grid. 
- The vector can be a scalar or a 2D numpy array with the same shape as grid. 
- If a scalar, the same value is added to each element in the grid. If a
    2D numpy array, the vector is added element-wise to the grid.

### Inputs
- spatial and velocity grid.
- vector to perform operation on.
- The mathematical operation to be performed. Options: 'add', 'subtract', 'multiply', 'divide'.

### Outputs
- result. Array with the same shape as grid.

## Filter
### What it does
Locate invalid (NaN) values in a grid and replace them with either the mean or median of the values immediately next to them.
The function iterates over each NaN value in the grid and replaces it with the mean or median of the non-NaN values in its 3x3 neighborhood, excluding itself. Values that have already been replaced by the mean or median filter are ignored in future replacements to prevent reusing them. If more than 3 out of the 9 values used to compute the mean or median are NaN values, the NaN value is not replaced.

### Input
- spatial and velocity grid.
- The filter to be applied. Options: 'mean' or 'median'.

### Output
- Array with the same shape as grid.
- Number of NaN values successfully replaced.
- Number of NaN values unsuccessfully replaced.
- Total number of non-NaN points in the grid.

## PlotTracks
### What it does
This function visualizes the movement of tracked objects in a video file. It takes a video file as input, along with tracking data for various objects. The function reads the video frame by frame and plots the tracks of the objects over the video frames. It highlights the paths of these objects in different colors, allowing you to visually track their movement across frames.

### Inputs
- inputname: Path to the video file.
- vtracks: A list of dictionaries, where each dictionary contains tracking information of an object. This includes the frame number ('T') and the x ('X') and y ('Y') coordinates of the object in each frame.
- framerange (optional): A list of two elements specifying the range of frames to plot. Default is the entire video.

### Outputs
- This function does not return any values but visualizes the tracks directly on the video frames. It displays each frame with the plotted tracks and pauses briefly between frames to create a visual tracking effect.

## FindRegions
### What it does
Given an image "im", FindRegions finds regions that are brighter than
"thresold" and have area larger than "arealim". Region centroids are
returned in the two-column array "pos" (with x-coordinates in the first
column and y-coordinates in the second). Region orientations are
returned in radians, in the vector "ang".

### Inputs
- Image
- Threshold for finding particles
- Size of particle in pixels
- Variable for debugging

### Outputs
- Position and angle of the particle

## FindRegions
### What it does
Given an image "im", FindParticles finds small particles that are
brighter than their four nearest neighbors and also brighter than
"threshold". Particles are located to sub-pixel accuracy by applying a
Gaussian fit in each spatial direction. The input "logs" depends on
the color depth and is re-used for speed. Particle locations are
returned in the two-column array "pos" (with x-coordinates in the first
column and y-coordinates in the second).

### Inputs
- Image
- threshold for finding particles
- color depth

### Outputs
- position of the particle