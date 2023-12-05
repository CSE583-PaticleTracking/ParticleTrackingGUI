import streamlit as st
import pandas as pd
from PIL import Image
# import cv2
import numpy as np

def particle_tracking_app(inputnames, invert, noisy):
    # Placeholder for particle tracking function
    # Replace this with your actual particle tracking function
    # and return the required output.

    # For demonstration purposes, returning dummy data
    vtracks = [{"length": 10, "coordinates": (0, 0), "time": 1, "velocity": (1, 1)}]
    ntracks = 1
    meanlength = 10
    rmslength = 5

    return vtracks, ntracks, meanlength, rmslength

# Streamlit app layout
st.title("Particle Tracking App")

# Input parameters
uploaded_file = st.file_uploader("upload file", type=["mp4", "jpg", "png", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.type == 'video/mp4':
        video_bytes = uploaded_file.read()
        st.video(video_bytes)

    elif uploaded_file.type in ['image/jpg', 'image/jpeg', 'image/png']:

        image = Image.open(uploaded_file)
        st.image(image, caption="uploaded picture", use_column_width=True)
    else:
        st.warning("nonsupport file type")


invert = st.radio("Invert", [0, 1, -1], index=2, format_func=lambda option: {0: "Bright", 1: "Dark", -1: "Any"}[option])
noisy = st.checkbox("Noisy (Plotting and Visualization Options)")

# Button to trigger particle tracking
if st.button("Run Particle Tracking"):
    st.info("Particle tracking in progress...")

    # Call the particle tracking function
    vtracks, ntracks, meanlength, rmslength = particle_tracking_app(
        uploaded_file, invert, noisy
    )

    st.success("Particle tracking completed!")

    # Display the output
    st.subheader("Output:")
    st.write(f"Total Number of Tracks: {ntracks}")
    st.write(f"Mean Length of Tracks: {meanlength}")
    st.write(f"Root Mean Square Length of Tracks: {rmslength}")

    # Display a sample of tracked particle information
    if ntracks > 0:
        st.subheader("Sample Tracked Particle Information:")
        st.table(vtracks[:min(5, ntracks)])
