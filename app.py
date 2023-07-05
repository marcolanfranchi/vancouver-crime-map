import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from data_tools import CrimeDataHandler
from map_plot import plot_on_map
from background import set_bg_hack

# ======================================================
st.set_page_config(layout="centered")
set_bg_hack("images/vanmap-nobg.png")

# ======================================================
vancouver_crime_df = pd.read_csv("data/crimedata_csv_all_years.csv")
crimeData = CrimeDataHandler(vancouver_crime_df)

crimeData.remove_null_rows()
crimeData.remove_null_coord_rows()

van_nbhds = crimeData.get_unique_sorted_vals('NEIGHBOURHOOD')
crime_types = crimeData.get_unique_sorted_vals('TYPE')
years = crimeData.get_unique_sorted_vals("YEAR")
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
# ======================================================

st.title("Vancouver Crimes Map")
st.markdown("Displays a map of crime locations in Vancouver from 2003 up to 2021 by time, neighbourhood, and type of crime.")

# ======================================================
selection_container = st.container()
with selection_container:
    st.markdown("---")
    time_col, neighbourhood_col, crime_col = st.columns(3)

    # ======================================================
    with time_col:
        year_type = st.radio(
            "Year:",
            options=["All (2003-2021)", "Range", "Custom"],
            index=2
        )
        if year_type == "All (2003-2021)":
            year_selection = years
        if year_type == "Range":
            from_year = st.number_input(
                label="From Year:",
                min_value=years[0],
                max_value=years[-2]
            )
            to_year = st.number_input(
                label="To Year:",
                min_value=from_year+1,
                max_value=years[-1]
            )   
            year_selection = range(from_year, to_year+1)
        if year_type == "Custom":
            year_selection = st.multiselect(
                "Select a year",
                options= years,
                default= 2021
            )
    # ======================================================
    with neighbourhood_col:
        nbhd_choice = st.multiselect(
            "Select one or more neighbourhoods",
            options= ['All'] + van_nbhds,
            default='Arbutus Ridge'
            )
        if nbhd_choice.count('All') > 0:
            nbhds_selection = van_nbhds
        else:
            nbhds_selection = nbhd_choice

    # ======================================================
    with crime_col:
        crime_choice = st.multiselect(
            "Select one or more offence types",
            options= ['All'] + crime_types,
            default='Break and Enter Commercial'
            )
        if crime_choice.count('All') > 0:
            crimes_selection = crime_types
        else:
            crimes_selection = crime_choice

    st.markdown("---")

# ======================================================
map_data = crimeData.get_data(year=year_selection, nbhd=nbhds_selection, crime_type=crimes_selection)
# st.dataframe(map_data)
st.text('Year(s) ---------------------------------------------------------------------------')
if year_type == 'Range':
    st.text(str(year_selection[0]) + " to " + str(year_selection[-1]))
elif year_type == 'All (2003-2021)':
    st.text('All (2003-2021)')
elif year_type == "Custom":
    st.text(', '.join([str(y) for y in sorted(year_selection)]))

st.text('Neighbourhood(s) ------------------------------------------------------------------')
if 'All' in nbhds_selection or len([n for n in nbhds_selection if n != 'All']) == len(van_nbhds):
    st.text('All')
else:  
    st.text(', '.join(nbhds_selection))

st.text('Offences --------------------------------------------------------------------------')
for n in [crime for crime in crimes_selection if crime != 'All']:
    count = list(map_data['TYPE']).count(n)
    st.text(n + ": " + str(count))

map_container = st.container()
with map_container:
    st.markdown("---")
    if map_data.empty == False:    
        plot_on_map(map_data)
    else:
        st.warning("No " + str(crimes_selection) + "'s occured in " + str(nbhds_selection) + " during " + str(year_selection))
    st.markdown("---")

