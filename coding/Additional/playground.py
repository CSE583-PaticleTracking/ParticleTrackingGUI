# Load the functions in read_and_reshape_csv.py into the playground.py file. 
import numpy as np
import csv
import os
import read_and_reshape_csv as rrc

# Create a test CSV file with metadata and data
test_file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/coding/Additional/turbulent_frames/metadata.csv'
test_metadata = {'Sampling frequency': 3303, 
                 'Sampling units': 'Hz', 
                 'Number of samples per column': 1000, 
                 'Number of columns': 4, 
                 'Calibration status': True,
                 'Spatial units': 'mm', 
                 'Parameter units': 'm/s', 
                 'Temporal units': 's'}

rrc.add_metadata_to_csv(test_file_path, test_metadata)

