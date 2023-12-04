# Load the functions in read_and_reshape_csv.py into the playground.py file. 
import numpy as np
import csv
import os
import read_and_reshape_csv as rrc
import vector_operations as vo

# Create a test CSV file with metadata and data
# test_file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames/metadata.csv'
# test_metadata = {'Sampling frequency': 3303, 
#                  'Sampling units': 'Hz', 
#                  'Number of samples per column': 1000, 
#                  'Number of columns': 4, 
#                  'Calibration status': True,
#                  'Spatial units': 'mm', 
#                  'Parameter units': 'm/s', 
#                  'Temporal units': 's'}

# rrc.add_metadata_to_csv(test_file_path, test_metadata)

# Create a test for extracting metadata from the CSV file
# extracted_metadata = rrc.extract_metadata_from_csv(test_file_path)
# print(extracted_metadata)

# Create a test for extracting frame number from the CSV file
# directory_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames'
# rrc.extract_and_check_consecutive_numbers(directory_path)

# Create a test for reading the CSV file
# test_frame_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames/frame_1.csv'
# x_positions, y_positions, u_velocities, v_velocities = rrc.read_csv_file(test_frame_path)
# print(x_positions)
# print(y_positions)
# print(u_velocities)
# print(v_velocities)

# Create a test for reshaping the CSV file
# x_grid, y_grid, u_grid, v_grid = rrc.reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)
# print(x_grid)
# print(y_grid)
# print(u_grid)
# print(v_grid)

# # Create a test for operating on a grid
# # Create a grid
# grid = 2 * np.ones((2, 2))
# # Create a vector
# vector = 0 * np.ones((2, 2))
# # Specify the operation
# operation = 'divide'
# # Perform the operation on the grid
# result = vo.operate_on_grid(grid, vector, operation)
# print("Original Grid:")
# print(grid)
# print("\nVector:")
# print(vector)
# print("\nResult after {}ing the vector to the grid:".format(operation.capitalize()))
# print(result)

# # Create a test for calculating the magnitude and angle of a vector field
# # Create a grid
# grid = np.array([[np.nan, 0], [0, 1]])
# # Calculate the magnitude and angle of the vector field
# magnitude_grid, angle_grid = vo.calculate_magnitude_and_angle(grid, grid)
# print("Magnitude:")
# print(magnitude_grid)
# print("\nAngle:")
# print(angle_grid)

# Create test for filling in NaN values using filter
# Create a grid
grid = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
# Specify the filter method
methd = 'mean'
# Fill in NaN values using filter
result = vo.fill_in_NaN_values_using_filter(grid, methd)
print("Original Grid:")
print(grid)
print("\nResult after filling in NaN values using {} filter:".format(methd))
print(result)












# def process_csv_folder(folder_path):
#     """
#     The function processes all CSV files in a folder and returns a list of reshaped data for each file.
#     """
#     # Get a list of all files in the folder
#     all_files = os.listdir(folder_path)

#     # Filter out only CSV files
#     csv_files = [file for file in all_files if file.endswith('.csv')]

#     # Initialize empty lists to store reshaped data
#     reshaped_data_list = []

#     # Loop through each CSV file
#     for csv_file in csv_files:
#         # Construct the full path to the CSV file
#         file_path = os.path.join(folder_path, csv_file)

#         # Read CSV file
#         x_positions, y_positions, u_velocities, v_velocities = read_csv_file(file_path)

#         # Reshape CSV file
#         x_grid, y_grid, u_grid, v_grid = reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

#         # You can do more processing here

#         # Append reshaped data to the list
#         reshaped_data_list.append((x_grid, y_grid, u_grid, v_grid))

#     return reshaped_data_list

# Example usage
# folder_path = '/path/to/your/csv/files/'
# reshaped_data_list = process_csv_folder(folder_path)

# Now, reshaped_data_list contains a list of tuples, each containing the reshaped data from one CSV file