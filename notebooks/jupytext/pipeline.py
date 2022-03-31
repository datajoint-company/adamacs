# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Pipeline Activation

# `adamacs/pipeline.py` includes all the pieces required to activate the whole pipeline.
# This can be done with the following import function.

import datajoint as dj
from adamacs.pipeline import subject, surgery, session, behavior, equipment, imaging, scan

# To visualize the pipeline, we can generate diagrams for any combination of schemas.

dj.Diagram(session)+dj.Diagram(subject)
