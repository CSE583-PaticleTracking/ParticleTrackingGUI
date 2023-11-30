## streamlit test file 

import numpy as np
import pandas as pd
import streamlit as st

# import our package/functions


# set page config
st.set_page_config(layout="wide")
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

## Define sidebar elements

## Define main window elements
uploaded_file = st.sidebar.file_uploader("Upload")

st.markdown('<p class="big-font">Particle Pals</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">Particle Tracking and Vector Analysis Application</p>', unsafe_allow_html=True)

# divider between title/description and graphics
st.divider()

col1, col2 = st.columns((1, 2))

with col1:
    instructions = st.text("Upload data to get started.")
    if uploaded_file is not None:
        # update instructions
        instructions.text("Populate input fields and execute computation.")

with col2:
    image = st.image('./default_graphic.jpg')
    if uploaded_file is not None:
        # update graphic
        
        # add elements to sidebar
        test_button = st.sidebar.button("test")
        image.image(uploaded_file)

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