# ParticleTrackingGUI

### Version
ParticleTrackingGUI 1.0
- Functioning GUI with vector analysis
- Translated particle tracker to python

### Project Goals
Create a Python GUI for tracking particle trajectories from images. After tracking, the user can 
export desired data and statistics. This GUI can be used for both personal/research purposes.

### File structure
```
.
├── README.md
├── LICENSE
├── environment.yml
├── .gitignore
├── .github/workflow
│   └── python-package-conda.yml
├── docs
│   ├── CSE 583 Final Presentation.pdf
│   ├── CSE583 Technology Review .pdf
│   ├── ParticleTrackingDocumentation.pdf
│   ├── ParticleTrackingGUI_diagram.pdf
│   ├── components.md
│   ├── use_cases.md
│   └── use_stories.md
├── examples
│   ├── README.md
│   ├── demo.mp4
│   └── data
│       ├── testtracks.avi
│       └── turbulent_frames
└── particlepals
    ├── __init__.py
    ├── gui_main.py
    ├── particle_tracking
    │   ├── BackgroundImage.py
    │   ├── ParticleFinder.py
    │   ├── PredictiveTracker.py
    │   ├── plottracks.py
    │   ├── test_velocities.py
    │   ├── tracking_scripts.py
    │   ├── velocities.py
    │   └── README.md
    ├── resources
    │   ├── myenv
    │   ├── animation_demo.py
    │   ├── plotting_demo.py
    │   └── README.md
    └── vector_analysis
        ├── generate_turbulent_velocity_field.py
        ├── playground.py
        ├── read_and_reshape_csv.py
        ├── test_read_and_reshape_csv.py
        ├── vector_operations.py
        ├── test_vector_operations.py
        ├── extra.txt
        └── README.md
```

### Docs
This folder contains example use cases, components, and a diagram to explain the GUI's operation.
There is a technology review that explains the group's thoughts on choosing Streamlit to help with
GUI construction. 

### Examples
There are examples available explaining the use and final results of the GUI.


### Members
A project designed by Particle Pals: 

- Julio Chavez
- Carlos Abarca
- Chandler Heintz
- Mohan Kukreja
- Torry Yan
