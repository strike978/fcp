import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import streamlit as st

# Set page title
st.set_page_config(page_title="Find Closest Populations", page_icon="🌎")

# Add page header
st.caption("This web application leverages G25 population data to calculate the distances between selected target populations and a reference population. The distances are calculated using the Euclidean algorithm, a popular method for measuring the geometric distance between two points in a high-dimensional space.")

# Read in data from the selected input file
t = pd.read_csv('Modern Era.txt', delimiter=",", index_col=0)

# Add a checkbox for selecting input data from the input file
use_manual_input = st.checkbox("Use G25 Coordinates")

# Define a text input for the input row
if use_manual_input:
    input_row_data = st.text_input(
        "Enter G25 Coordinates")
    if input_row_data:
        input_row_data = input_row_data.split(',')
        input_row_name = input_row_data[0]
        input_row = np.array([float(x) for x in input_row_data[1:]])
    else:
        input_row = None
else:
    input_row_name = st.selectbox("Select reference population", t.index)
    input_row = t.loc[input_row_name]

# Define a multiselect box for the target rows
target_rows = st.multiselect("Select target populations", t.index)

if not target_rows:
    st.error("Please select at least one target population.")

# Add a "Calculate Distance" button
if st.button("Calculate Distance"):

  # This is the code that calculates the distance between the selected populations.
    distances = {}
    if input_row is not None:
        for target_row in target_rows:
            d = squareform(pdist(np.vstack((input_row, t.loc[target_row]))))
            distance = d[0, 1]
            distances[target_row] = distance

        sorted_target_rows = sorted(distances, key=distances.get)
        closest_target_row = sorted_target_rows[0]
        closest_distance = distances[closest_target_row]

  # Printing the distance between the selected populations.
        st.write("Distance to:")
        for target_row in sorted_target_rows:
            st.code(f"{target_row}: {distances[target_row]:.2f}")
