import pandas as pd
from scipy.spatial.distance import pdist, squareform
import streamlit as st


def find_closer_population(target, comparisons):
    t = pd.read_csv("Modern Ancestry.txt", header=0, index_col=0)
    d = pdist(t)
    d = pd.DataFrame(squareform(d), index=t.index, columns=t.index)
    distance_1 = d.loc[target, comparisons[0]]
    distance_2 = d.loc[target, comparisons[1]]

    if distance_1 < distance_2:
        closer = comparisons[0]
        percent_closer = (1 - distance_1 / distance_2) * 100
    else:
        closer = comparisons[1]
        percent_closer = (1 - distance_2 / distance_1) * 100

    return "{} is {:.2f}% closer to {} than {}.".format(
        target, percent_closer, closer, comparisons[1 - comparisons.index(closer)])


def main():
    st.set_page_config(
        page_title="Find Closer Population", page_icon="🌎", layout="wide")
    st.title("Find Closer Population")
    t = pd.read_csv("Modern Ancestry.txt", header=0, index_col=0)
    options = list(t.index)
    default_option = "Southwest Europe:Spanish:Galician (Galicia)"
    default_options = ["North Africa:Maghreb:Moroccan (Oujda)",
                       "Northwest Europe:British Isles:Irish"]

    target = st.selectbox("Select Target Population:",
                          options, index=options.index(default_option))
    comparison = st.multiselect("Select Source Populations:",
                                options, default=default_options, key='comp')

    if len(comparison) == 2:
        if st.button("Calculate Distance"):
            result = find_closer_population(target, comparison)
            st.code(result)
    else:
        st.warning("Please select exactly 2 source populations.")

    st.caption(
        "We employ the G25 population data and the Euclidean method to calculate population distances.")


if __name__ == '__main__':
    main()
