import folium
from streamlit_folium import st_folium, folium_static
import streamlit as st
import utm as utm

def plot_on_map(df):
    m = folium.Map(location=utm.to_latlon(df['X'].mean(), df['Y'].mean(), 10, 'N'), 
                 zoom_start=13, control_scale=True, tiles="cartodb positron")

    #Loop through each row in the dataframe
    for i,row in df.iterrows():
        #Setup the content of the popup
        iframe = folium.IFrame("Crime: " + row["TYPE"] + "\n Area: " + row["NEIGHBOURHOOD"] + " Loc: (" + str(row['X']) + "," + str(row['Y']) + ")")
        
        #Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        
        #Add each row to the map
        loc = utm.to_latlon(row['X'], row['Y'], 10, 'N')
        folium.Marker(location=list(loc),
                    popup = popup, c=row['TYPE'],
                    ).add_to(m)

    st_data = folium_static(m, width=700, height=500)
