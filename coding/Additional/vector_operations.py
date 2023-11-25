import numpy as np
import csv

def add_vector_to_grid(grid, vector, scale=False):
    if scale:
        vector = np.array(vector) / np.max(np.abs(vector))

    result = grid + vector
    return result

def subtract_vector_from_grid(grid, vector, scale=False):
    if scale:
        vector = np.array(vector) / np.max(np.abs(vector))

    result = grid - vector
    return result