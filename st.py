import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import streamlit as st

# Set page title
st.set_page_config(page_title="Find Closest Populations", page_icon="🌎")

# Read in data from the selected input file
t = pd.read_csv('Modern Era.txt', delimiter=",", index_col=0)

st.caption("Calculate similarity between populations using G25 population data and the Euclidean algorithm. Choose to enter G25 coordinates manually or select a population.")

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
    input_row_name = st.selectbox("Select population", t.index)
    input_row = t.loc[input_row_name]

# Define a slider for the number of rows to display
num_rows = st.slider("Number of populations to display",
                     min_value=1, max_value=len(t.index), value=10)

# Add a "Calculate Distance" button
if st.button("Calculate") and input_row is not None:

    # Calculate distances between the reference population and all other populations
    similarities = {}
    for target_row in t.index:
        if target_row != input_row_name:
            d = squareform(pdist(np.vstack((input_row, t.loc[target_row]))))
            distance = d[0, 1]
            similarity = (1 - distance) * 100
            similarities[target_row] = similarity

    sorted_target_rows = sorted(
        similarities, key=similarities.get, reverse=True)
    most_similar_target_row = sorted_target_rows[0]
    most_similar_similarity = similarities[most_similar_target_row]

    # Printing the similarity index between the reference population and all other populations
    for i, target_row in enumerate(sorted_target_rows[:num_rows]):
        st.code(f"{i + 1}. {target_row}: {similarities[target_row]:.2f}%")
