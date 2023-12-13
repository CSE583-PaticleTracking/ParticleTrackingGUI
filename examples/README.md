# User Guide: Python GUI for Velocity Field Analysis and Particle Tracking

## Introduction:
This document provides step-by-step instructions on how to run a Python Graphical User Interface (GUI) designed to analyze velocity fields and track particles in images. The GUI prompts users for necessary inputs, allowing them to process CSV files for velocity field analysis and employ custom functions for particle tracking. Furthermore, the GUI provides options to export the processed data in user-specified formats.

## System Requirements:

Operating System: Windows, macOS, or Linux
Python 3.x installed

# Getting Started:

## Download the GUI:
- Obtain the GUI files from the GitHub.
- Open a Terminal or Command Prompt:
- Launch a terminal or command prompt on your computer.
- Navigate to GUI Directory
- Use the '''cd''' command to navigate to the directory where the GUI files are located.
- Install Dependencies and the required Python libraries by running the environment:
'''
pip install -r environment.yml
'''

## Run the GUI:
Execute the main GUI script by running:
'''
streamlit run
'''

# Using the GUI:

## GUI Interface Overview:
The GUI will open, presenting a user-friendly interface with options for velocity field analysis and particle tracking.

## Velocity Field Analysis:
### Load CSV File:
- Click the "Load CSV" button to select the CSV file containing velocity field data.
- Provide the path of the folder where the CSV files are stored.

### Select Operation:
- Choose the desired operation from the available options (add, subtract, multiply, divide, mean filter, median filter).

### Adjust Parameters:
- Depending on the chosen operation, enter the required parameters.

### Process Data:
Click the "Compute" button to perform the selected operation on the velocity field.

### Export Processed Data:
- Specify the desired export format (CSV, Excel for future releases, etc.) and click the "Export" button.

# Particle Tracking:
## Load Image:
- Click the "Load Image" button to select the image file containing particles.

## Adjust Parameters:
-  enter the required parameters depending on the data:
    + inputnames - name of the video file to be tracked
    + threshold - threshold for finding particles
    + max_disp - maximum displacement of particles between frames
    + bground_name - name of the background image
    + minarea - minimum area of particles
    + invert - invert the image
    + noisy - plot the tracks
    + framerange - range of frames to be tracked
    + gifname - name of the gif file
    + found - dictionary of found particles
    + correct - dictionary of correct particles
    + yesvels - calculate velocities
    
## Track Particles:
Click the "Track" button to initiate particle tracking.
## Export Tracked Data:
Specify the desired export format (CSV, Excel, etc.) and click the "Export" button.

# Additional Tips:
- Ensure that the input CSV files for velocity field analysis have the correct format (e.g., columns for x, y, and velocity components).
- Particle tracking may require image preprocessing; make sure the selected image is suitable for tracking.

# Closing the GUI:
- Close the GUI window when you have completed your analysis.

# Troubleshooting:
If you encounter any issues, refer to the provided documentation.