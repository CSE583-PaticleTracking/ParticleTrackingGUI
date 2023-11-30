## streamlit test file 

import numpy as np
import streamlit as st

# import our package/functions

## Define sidebar elements
upload_button = st.sidebar.button("Upload")

## Define main window elements
title_text = '''# ParticlePals
                Particle Tracking and Vector Analysis Application'''
title = st.markdown(title_text)
# image = st.image()


## Define placeholders for element to be filled in later
progress_bar = st.empty()


# We clear elements by calling empty on them.
progress_bar.empty()

