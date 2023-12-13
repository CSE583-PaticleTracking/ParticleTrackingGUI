"""
streamlit test file
"""
import os

import streamlit as st

# add package parent directory to sys path

from Additional.read_and_reshape_csv import process_csv_folder

## TODO: add particlepals imports
# import our package/functions

## TODO: check style and run tests

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
        graphic = st.image('src/GUI/default_graphic.jpg')

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
                dir_path = data_path[0:data_path.rfind(data_file)]
                dir_fd = os.open(dir_path, os.O_RDONLY)
            except (IndexError, ValueError, FileNotFoundError) as e:
                data_path_err.text("Invalid input." +
                                   f"\nEncountered error: {e}." +
                                   "\nCheck path.")

            def opener(path, flags):
                return os.open(path, flags, dir_fd=dir_fd)

            if data_extension == '.tif':
                with open(data_file, 'rb', opener=opener) as f:
                    graphic_data = f.read()
                    graphic.image(graphic_data)

        ## TODO: update graphic AFTER first radio button (based on analysis/file type)
        # no longer matters because we are setting default index on radio button, anyway...
        # try:
        #     f = open(data_path, "rb")
        #     image_data = f.read()
        #     graphic.image(image_data)
        # except MediaFileStorageError as e:
        #     data_path_err.text("Invalid path!")
        #     invalid_path = True
        ## TODO: delete block above. leaving for now in case I wnat to reference
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
                threshold = st.sidebar.number_input("Brightness Threshold")
                max_disp = st.sidebar.number_input("Maximum Displacement")
                min_area = st.sidebar.number_input("Minimum Displacement")
                framerate = st.sidebar.slider("Framerate")
                invert = st.sidebar.radio("Invert", ("Bright", "Dark"))

                ## TODO: Implement submit button
                # run other functions from particlepals package here,
                # update inputs as required, and handle output
                submit = st.sidebar.button("Compute")
            else:
                # for vector analysis, computation params are gathered from csv files in directory
                # csv files should follow naming convention, but don't need to check for that here
                ## TODO: add other inputs for VA
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

                # run other functions from particlepals package here,
                # update inputs as required, and handle output
                submit = st.sidebar.button("Compute")

                if submit:
                    try:
                        process_csv_folder(data_path, operation)
                    except FileNotFoundError as e:
                        st.sidebar.text(f"Computation raised error: \n{e}" +
                                        "\nCheck inputs."
                                        )
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

    # if file name hasn't changed, let somebody know
    if file_name == '':
        raise ValueError("Could not get file name from path.")
    return file_name


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
