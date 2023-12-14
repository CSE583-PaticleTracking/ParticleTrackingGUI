"""
streamlit test file
"""
import os

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# add package parent directory to sys path

from vector_analysis.read_and_reshape_csv import process_csv_folder, read_csv_file, reshape_csv_file
from particle_tracking.PredictiveTracker import Predictive_tracker

def main():
    """
    Main function.
    Builds GUI using the streamlit package.
    Once a user fills in inputs fields with the GUI,
    other particlepals functions are then called from here.
    Inputs:
        None
    Returns:
        None
    """
    # set page config
    st.set_page_config(layout="wide")
    MediaFileStorageError = st.runtime.media_file_storage.MediaFileStorageError
    st.markdown('<p class="big-font">Particle Pals</p>', unsafe_allow_html=True)
    st.markdown(
                '<p class="small-font">Particle Tracking and Vector Analysis Application</p>',
                unsafe_allow_html=True
    )
    build_footer()

    if 'button' not in st.session_state:
        st.session_state.button = False

    def click_button():
        st.session_state.button = not st.session_state.button

    # Define sidebar data input
    data_path = st.sidebar.text_input("Data Path:", None)
    data_path_err = st.sidebar.empty()
    data_extension = None

    # divider between title/description and graphics
    st.divider()

    # define cols for graphic and instructions
    col1, col2 = st.columns((1, 2))
    with col1:
        instructions = st.text("Upload data to get started.")
    with col2:
        default_graphic_path = 'particlepals/resources/default_graphic.jpg'
        try:
            graphic = st.image(default_graphic_path)
        except MediaFileStorageError as e:
            st.text(f"check default graphic path: {default_graphic_path}")

    # update content based on inputs
    if data_path is not None:
        invalid_path = False

        try:
            # get file extension from path string
            data_extension = get_extension(data_path)
        except (IndexError, ValueError) as e:
            data_path_err.text("Invalid input." +
                               f"\nEncountered error: {e}." +
                               "\nCheck path.")

        # extension can be None, 'dir', or '.{extension}'
        # but we will only allow 'dir', '.tif', and '.avi'
        if data_extension is None:
            invalid_path = True
            data_path_err.text("Check path." +
                               "\nFile path must include extension." +
                               "\nDirectory path must end in slash."
            )
        elif data_extension == 'dir':
            ## TODO: update graphic for VA based on csv naming convention
            pass
        else:
            try:
                data_file = get_file_name(data_path, data_extension)
                data_path_err.text(data_file)
                ## implement this feature later...
                # decided that for now we are going to assume .tif and .avi are in working dir.
                # dir_path = get_dir_path(data_path, data_file)
            except (IndexError, ValueError, FileNotFoundError) as e:
                data_path_err.text("Invalid input." +
                                   f"\nEncountered error: {e}." +
                                   "\nCheck path.")

            ## implement this feature later...
            # decided that for now we are going to assume .tif and .avi are in working dir.
            # dir_fd = os.open(dir_path, os.O_RDONLY)
            # def opener(path, flags):
            #     return os.open(path, flags, dir_fd=dir_fd)
            
            if data_extension == '.tif':
                data_path = 'src\\' + data_file
                # with open(data_file, 'rb', opener=opener) as f:
                with open(data_path, 'rb') as f:
                    graphic_data = f.read()
                    graphic.image(graphic_data)

        if not invalid_path:
            # update instructions
            instructions.text("Populate input fields and execute computation.")

            ## add elements to sidebar
            # set starting index for radio button based on file extension
            radio_index = 0
            if data_extension == 'dir':
                radio_index = 1
            analysis_type = st.sidebar.radio(
                label="Analysis Type:",
                options=("Particle Tracking", "Vector Analysis"),
                index=radio_index
            )
            if analysis_type == "Particle Tracking":
                threshold = st.sidebar.number_input("Brightness Threshold", min_value=0)
                max_disp = st.sidebar.number_input("Maximum Displacement", min_value=0)
                min_area = st.sidebar.number_input("Minimum Displacement", min_value=0)
                startframe = st.sidebar.number_input("Start Frame", step=1, min_value=0)
                endframe = st.sidebar.number_input("End Frame", step=1, min_value=startframe+1)
                # framerange = st.sidebar.slider("Framerange")
                invert = st.sidebar.radio("Invert", ("Bright", "Dark"))

                framerange = np.arange(startframe, endframe)

                match invert:
                    case "Bright":
                        invert = 0
                    case "Dark":
                        invert = 1

                submit = st.sidebar.button("Compute", on_click=click_button)

                if st.session_state.button:
                    try:
                        Predictive_tracker(
                            inputnames=data_file,
                            threshold=threshold,
                            max_disp=max_disp,
                            minarea=min_area,
                            invert=invert,
                            framerange=framerange,
                            bground_name=None,
                            noisy=None,
                            gifname=None,
                            found=None,
                            correct=None,
                            yesvels=None
                        )
                    except FileNotFoundError as e:
                        st.sidebar.text(f"Computation raised error: \n{e}" +
                                        "\nCheck inputs."
                                        )
            else:
                # for vector analysis, computation params are gathered from csv files in directory
                # csv files should follow naming convention, but don't need to check for that here
                i = 0
                data_file = f'frame_{i}.csv'
                data_path = get_dir_path(data_path + data_file, 'frame_0.csv')

                # update graphic
                x_positions, y_positions, u_velocities, v_velocities = read_csv_file(os.path.join(data_path, data_file))
                x_grid, y_grid, u_grid, v_grid = reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)
                
                fig = plt.figure(figsize=(4,4))
                plt.quiver(x_grid, y_grid, u_grid, v_grid, scale=15, scale_units='xy', angles='xy', cmap='viridis')
                plt.title(f'Turbulent Velocity Field')
                plt.xlabel('X')
                plt.ylabel('Y')
                graphic.pyplot(fig,use_container_width=False)

                operation = st.sidebar.radio("Operation",
                                            (
                                                'add',
                                                'subtract', 
                                                'multiply', 
                                                'divide', 
                                                'mean', 
                                                'median'
                                            )
                )

                vector_x = st.sidebar.number_input("Vector X")
                vector_y = st.sidebar.number_input("Vector Y")
                vector = (vector_x, vector_y)

                # run other functions from particlepals package here,
                # update inputs as required, and handle output
                submit = st.sidebar.button("Compute", on_click=click_button)

                if st.session_state.button:
                    data_path_err.text(data_path)
                    try:
                        u_grid, v_grid, numbers = process_csv_folder(data_path, operation, vector)
                        frame_num = st.slider('Frame', min_value=min(numbers), max_value=max(numbers))
                        fig = plt.figure(figsize=(4,4))
                        plt.quiver(x_grid, y_grid, u_grid, v_grid, scale=15, scale_units='xy', angles='xy', cmap='viridis')
                        plt.title(f'Turbulent Velocity Field, Frame {frame_num}')
                        plt.xlabel('X')
                        plt.ylabel('Y')
                        graphic.pyplot(fig,use_container_width=False)
                    except FileNotFoundError as e:
                        st.sidebar.text(f"Computation raised error: \n{e}" +
                                        "\nCheck inputs."
                                        )

                # # run other functions from particlepals package here,
                # # update inputs as required, and handle output
                # submit = st.sidebar.button("Compute")

                # if submit:
                #     data_path_err.text(data_path)
                #     try:
                #         u_grid, v_grid, numbers = process_csv_folder(data_path, operation, vector)
                #         frame_num = st.slider('Frame', min_value=min(numbers), max_value=max(numbers))
                #         fig = plt.figure(figsize=(4,4))
                #         plt.quiver(x_grid, y_grid, u_grid, v_grid, scale=15, scale_units='xy', angles='xy', cmap='viridis')
                #         plt.title(f'Turbulent Velocity Field, Frame {frame_num}')
                #         plt.xlabel('X')
                #         plt.ylabel('Y')
                #         graphic.pyplot(fig,use_container_width=False)
                #     except FileNotFoundError as e:
                #         st.sidebar.text(f"Computation raised error: \n{e}" +
                #                         "\nCheck inputs."
                #                         )
    else:
        pass

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


def get_extension(path):
    '''
    Gets file extension from path.
    Inputs:
        path: string containing path to file or directory. 
            Can be absolute or relative. Directory path should
            end with a slash.
    Returns:
        extension: string extension for files or 'dir' for directories.
    '''
    # initialize output
    extension = None

    # since paths can be relative, convention will be to include / or \
        # for directory paths (i.e. NOT just leave off dot)

    # find last "." in path .
    # this is either beginning of extension OR part of relative path
        # OR may not exist for absolute paths to directories
    dot_idx = path.rfind('.')

    # path should never end in a dot
    if not len(path) > dot_idx:
        return extension

    # edge case: path is current directory (./) or parent directory (../)
    # all other relative paths (that make sense) should have 
        # chars besides . & / after the first slash...
    # these should be handled if we just check for directory first
    if path[-1] in ('/', '\\'):
        extension = 'dir'
    elif dot_idx != -1 and path[dot_idx + 1] not in ('/', '\\'):
        extension = path[dot_idx:]
    else:
        pass

    return extension


def get_file_name(path, extension):
    """
    Gets file name from full path.
    Inputs:
        path: string containing path to file. 
            Can be absolute or relative.
    Returns:
        file_name: string file name including extension
    """
    file_name = ''

    # make sure this isn't a directory JIC
    if extension == 'dir':
        raise ValueError("Path must include file name and extension.")
    elif '/' in path:
        slash_idx = path.rfind('/')
        file_name = path[slash_idx+1:]
    elif '\\' in path:
        slash_idx = path.rfind('\\')
        file_name = path[slash_idx+1:]
    else:
        # if path is just a file name, return it
        file_name = path
    # if file name hasn't changed, let somebody know
    if file_name == '':
        raise ValueError("Could not get file name from path.")
    
    return file_name


def get_dir_path(full_path, file):
    """
    Gets absolute path (excluding file name and extension) from full path.
    Inputs:
        path: string containing path to file plus file name and extension.
            Path can be absolute or relative.
        file: file name and extension.
    Returns:
        dir_path: string absolute path to file's parent directory
    """
    file_idx = full_path.rfind(file)
    dir_path = full_path[0:file_idx]
    is_relative_path = '.' in dir_path
    if not is_relative_path:
        return dir_path
    else:
        # replace relative references with absolute
        cwd = os.getcwd()
        dot_idx = dir_path.find('.')

        # first dot should always be at index zero...
        if dot_idx != 0:
            raise ValueError("Invalid path. Path should start with relative refs.")

        # check if referencing current directory ('.') or parent's ('..')
        if '..' in dir_path:
            # if path starts with '.':
            if dir_path[dot_idx+1] != '.':
                # since '.' is followed by '..', can simply remove it here...
                # and we know that this is at index 0, followed by a single slash
                dir_path = dir_path[2:]
            # else:
            #    pass

            # now there is NO single dot but there is/are double(s)
            # if referencing parent directory, count occurences
            # then remove from abs path accordingly...
            double_dot_count = dir_path.count('..')
            for _ in range(double_dot_count):
                remove_from_idx = cwd.rfind('\\')
                cwd = cwd[:remove_from_idx]
                remove_to_idx = dir_path.find('..')
                dir_path = dir_path[remove_to_idx+2:]

            # now construct new path by removing all dots and replacing with cwd
            remove_to_idx = dir_path.rfind('..')
            dir_path = cwd + dir_path[remove_to_idx:]

        # if no parent references, simply replace single dot with cwd
        else:
            dir_path = dir_path.replace('.', cwd)

        if '/' in dir_path:
            dir_path = dir_path.replace('/','\\')

        return dir_path


def build_footer():
    """
    Defines footer using unsafe_allow_html=True arg in markdwon element
    Inputs:
        None
    Returns:
        None
    """
    st.markdown("""
    <div class="footer">
    <p><a style='display: block; text-align: center;' href="https://github.com/CSE583-PaticleTracking/ParticleTrackingGUI/tree/main" target="_blank">Check out this project on Github</a></p>
    </div>
    """
    ,unsafe_allow_html=True)
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
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()