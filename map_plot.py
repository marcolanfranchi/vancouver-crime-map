import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static
import pandas as pd
from data_card import generate_popup_html
import streamlit as st

def plot_on_map(df):
    m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], 
                 zoom_start=13, control_scale=True, tiles="cartodb positron")

    #Loop through each row in the dataframe
    for i,row in df.iterrows():
        #Setup the content of the popup
        iframe = folium.IFrame(generate_popup_html(row))
        
        #Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300, min_height=100, max_height=100)
        
        #Add each row to the map
        loc = row['LAT'], row['LON']

        folium.Marker(
            location=list(loc),
            popup = popup, 
            icon=get_icon(row['TYPE'])
        ).add_to(m)

    st_data = folium_static(m, width=700, height=500)

def plot_heatmap(df):
    m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], 
                 zoom_start=13, control_scale=True, tiles="cartodb positron")
    
    heat_data = [[row['LAT'], row['LON']] for index, row in df.iterrows()]

    HeatMap(heat_data, blur=5).add_to(m)
    st_data = folium_static(m, width=700, height=500)


@st.cache_data
def generate_map_title(date_range, nbhds, crimes, all_nbhds, all_crimes):
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    nbhds_title = ''
    if len(nbhds) == len(all_nbhds) or not nbhds:
        nbhds_title = 'All of Vancouver'
    else:
        nbhds_title = ', '.join(nbhds)

    crimes_title = ''
    if len(crimes) == len(all_crimes) or not crimes:
        crimes_title = 'All Crimes'
    else:
        crimes_title = ', '.join(crimes)

    title = f"{nbhds_title} - {crimes_title} ({start_date_str} to {end_date_str})"
    return title

def get_icon(crime_type):
    icon = ""
    color = "red"
    if crime_type == 'Break and Enter Commercial':
        icon="fa-sharp fa-solid fa-building"
    elif crime_type == 'Break and Enter Residential/Other':
        icon="fa-sharp fa-solid fa-house"
    elif crime_type == 'Mischief':
        icon="fa-sharp fa-solid fa-bomb"
    elif crime_type == 'Other Theft':
        icon="fa-sharp fa-solid fa-cart-shopping"
    elif crime_type == 'Theft from Vehicle':
        icon="fa-sharp fa-solid fa-car"
    elif crime_type == 'Theft of Bicycle':
        icon="fa-sharp fa-solid fa-bicycle"
    elif crime_type == 'Theft of Vehicle':
        icon="fa-sharp fa-solid fa-route"
    elif crime_type == 'Vehicle Collision or Pedestrian Struck (with Fatality)':
        icon="fa-sharp fa-solid fa-hospital"
    elif crime_type == 'Vehicle Collision or Pedestrian Struck (with Injury)':
        icon="fa-sharp fa-solid fa-car-burst"

    return folium.Icon(color= color, icon=icon)
