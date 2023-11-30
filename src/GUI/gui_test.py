## streamlit test file 

import numpy as np
import pandas as pd
import streamlit as st

# set page config
st.set_page_config(layout="wide")

# import our package/functions

## Define sidebar elements
upload_button = st.sidebar.button("Upload")

## Define main window elements

row1_1, row1_2 = st.columns((1, 3))

with row1_1:
    st.title("Particle Pals")

with row1_2:
    st.write(
        """
        #
        """
        )
    st.write("Particle Tracking and Vector Analysis Application")

# divider between title/description and graphics
st.divider()

row2_1, row2_2 = st.columns((1, 2))

with row2_1:
    st.write(
        """
        Upload data to get started.
        """
    )

with row2_2:
    image = st.image('./default_graphic.jpg')

## Define placeholders for element to be filled in later
progress_bar = st.empty()


# We clear elements by calling empty on them.
progress_bar.empty()


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
<p><a style='display: block; text-align: center;' href="https://github.com/CSE583-PaticleTracking/ParticleTrackingGUI/tree/main" target="_blank">Check out this project on Github </a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)