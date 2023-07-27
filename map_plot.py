import folium
from streamlit_folium import st_folium, folium_static
import streamlit as st
import utm as utm
from data_card import generate_popup_html

def plot_on_map(df):
    m = folium.Map(location=utm.to_latlon(df['x'].mean(), df['y'].mean(), 10, 'N'), 
                 zoom_start=13, control_scale=True, tiles="cartodb positron")

    #Loop through each row in the dataframe
    for i,row in df.iterrows():
        #Setup the content of the popup
        iframe = folium.IFrame(generate_popup_html(row))
        
        #Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300, min_height=100, max_height=100)
        
        #Add each row to the map
        loc = utm.to_latlon(row['x'], row['y'], 10, 'N')

        folium.Marker(
            location=list(loc),
            popup = popup, 
            icon=get_icon(row['type'])
        ).add_to(m)

    st_data = folium_static(m, width=700, height=500)

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
