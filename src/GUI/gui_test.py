## streamlit test file 

import numpy as np
import pandas as pd
import streamlit as st

## TODO: add particlepals imports
# import our package/functions

## TODO: check style and run tests

def main():
    # set page config
    st.set_page_config(layout="wide")
    MediaFileStorageError = st.runtime.media_file_storage.MediaFileStorageError
    st.markdown('<p class="big-font">Particle Pals</p>', unsafe_allow_html=True)
    st.markdown('<p class="small-font">Particle Tracking and Vector Analysis Application</p>', unsafe_allow_html=True)
    build_footer()

    ## Define main window elements
    data_path = st.sidebar.text_input("Data File Path:", None)
    data_path_err = st.sidebar.empty()
    data_extension = None

    # divider between title/description and graphics
    st.divider()

    # define cols for graphic and instructions 
    col1, col2 = st.columns((1, 2))
    with col1:
        instructions = st.text("Upload data to get started.")

    with col2:
        image = st.image('./default_graphic.jpg')

    # update content based on inputs 
    if (data_path is not None):
        invalid_path = False

        # get file extension from path string
        # find last "." in path and assume this is beginning of file extension
        dot_idx = data_path.rfind('.')

        # since paths can be relative, convention should be to include / or \
            # for directory paths (i.e. NOT just leave off dot)
        # if no dot found, advise user to edit path
        if dot_idx == -1 or dot_idx < len(data_path) - 3:
            invalid_path = True
            data_path_err.text("Check path.\nFile path must include extension.\nDirectory path must end in slash.")

        elif data_path[-1] in ['/', '\\']:
            data_extension = 'dir'

            ## TODO: Update graphic based on frame one csv
        else:
            data_extension = data_path[dot_idx:]

            ## TODO: add logic for handling different extensions

            # update graphic
            try:
                f = open(data_path, "rb")
                image_data = f.read()
                image.image(image_data)
            except MediaFileStorageError as e:
                data_path_err.text("Invalid path!")
                invalid_path = True
        
        if not invalid_path:        
            # update instructions
            instructions.text("Populate input fields and execute computation.")

            ## TODO: update params/format for each input
            # add elements to sidebar
            analysis_type = st.sidebar.radio("Analysis Type:", ("Particle Tracking", "Vector Analysis"))
            if analysis_type == "Particle Tracking":
                threshold = st.sidebar.slider("Brightness Threshold")
                max_disp = st.sidebar.number_input("Maximum Displacement")
                min_area = st.sidebar.number_input("Minimum Displacement")
                invert = st.sidebar.radio("Invert", ("Bright", "Dark", "Any"))
            else:
                # for vector analysis, computation params are gathered from csv files in directory
                # csv files should follow naming convention:
                    # dir
                    # TODO: add specific file names to dictionary, make sure they are all in folder, and then read data from them
                va_file_names = {}
                read_vector_analysis_files(data_path, va_file_names)

            ## TODO: Implement submit button
                # i.e. run other functions from particlepals package here, update inputs as required, and handle output
            submit = st.sidebar.button("Compute")

# threshold: Sets the brightness threshold
#   for particle identification.
# max_disp: Maximum displacement allowed
#   for particle tracking.
# bground_name: Name of the file containing
#   the background image.
# minarea: Minimum area for particle
#   identification (default is 1 pixel).
# invert: Determines whether to track bright
#   (0), dark (1), or any contrast (-1) particles.
# noisy: Controls the plotting and
#   visualization options.

def build_footer():
    footer = """<style>
    a:link , a:visited{
    background-color: transparent;
    color: white;
    text-decoration: none;
    }

    a:hover,  a:active {
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: black;
    text-align: center;
    }
    </style>
    <div class="footer">
    <p><a style='display: block; text-align: center;' href="https://github.com/CSE583-PaticleTracking/ParticleTrackingGUI/tree/main" target="_blank">Check out this project on Github</a></p>
    </div>
    """
    st.markdown(footer,unsafe_allow_html=True)
    st.markdown("""
    <style>
    .big-font {
        font-size:40px;
    }
    .small-font {
        font-size:20px;
    }
    .block-container {
        padding-top: 0px;
        margin-top: 30px;
        padding-bottom: 10px;
    }
    .st-emotion-cache-16txtl3 {
        padding-top: 0px;
        margin-top: 100px;
        margin-left: 50px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return footer


def read_vector_analysis_files(data_path, va_file_names):
    pass


if __name__ == '__main__':
	main()