import streamlit as st
from data_tools_csv import CrimeDataHandler
from map_plot import plot_on_map, plot_heatmap, generate_map_title
from background import set_bg_hack
from datetime import timedelta

# ======================================================

st.set_page_config(
    page_title="VCM",
    page_icon="🚔",
    layout="wide",
)

# remove streamlit's main menu and footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
# set_bg_hack("images/vanmap-nobg.png")

# ======================================================
crimeData = CrimeDataHandler()
crimeData.load_data(csv_file_path="data/crimedata_csv_AllNeighbourhoods_AllYears-aug14-2023.csv")

van_nbhds = crimeData.get_unique_sorted_vals("NEIGHBOURHOOD")
crime_types = crimeData.get_unique_sorted_vals("TYPE")
years = crimeData.get_unique_sorted_vals("YEAR")
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
min_date = crimeData.get_min_date()
max_date = crimeData.get_max_date()
# ===================================================================================================================================

st.title(":gray[Vancouver Crimes Map]")
st.info("Display a map of crimes in Vancouver by selecting neighbourhoods, crimes, and a range of dates.")

# ========================================================================

# sidebar
with st.sidebar:
    all_neighbourhoods = st.checkbox("Click to View all Neighbourhoods")
    nbhd_choice = st.multiselect(
        "Select one or more neighbourhoods",
        options= van_nbhds,
        default=van_nbhds[0],
        disabled = all_neighbourhoods
        )
    if all_neighbourhoods:
        nbhds_selection = van_nbhds
    else:
        nbhds_selection = nbhd_choice

    st.markdown("---") # ================================================

    all_crimes = st.checkbox("Click to View all Crimes")
    crime_choice = st.multiselect(
        "Select one or more offence types",
        options= crime_types,
        default=crime_types[0],
        disabled = all_crimes
        )
    if all_crimes:
        crimes_selection = crime_types
    else:
        crimes_selection = crime_choice    

    st.markdown("---") # ================================================

    time_selection = st.date_input("Select a date range",
                                        value = [max_date - timedelta(days=30), max_date], 
                                       # default_start = max_date - timedelta(days=30),
                                       # default_end = max_date,
                                       min_value = min_date,
                                       max_value = max_date)
    
    st.markdown("---") # ================================================
    
    map_data = None
    map_button = st.button("View Map")
    if map_button:
        map_data = crimeData.get_filtered_data(date_range=time_selection, nbhds=nbhds_selection, crimes=crimes_selection)


    # st.text('Year(s) ---------------------------------------------------------------------------')
    # if year_type == 'Range':
    #     years_label = str(year_selection[0]) + " to " + str(year_selection[-1])
    # elif year_type == 'All (2003-2023)' or (year_type == "Custom" and not year_selection):
    #     years_label = 'All (2003-2023)'
    # elif year_type == "Custom":
    #     years_label = ', '.join([str(y) for y in sorted(year_selection)])
    # st.text(years_label)

    # st.text('Neighbourhood(s) ------------------------------------------------------------------')
    # if 'All' in nbhds_selection or len([n for n in nbhds_selection if n != 'All']) == len(van_nbhds) or not nbhds_selection:
    #     nbhds_label = 'All'
    # else:  
    #     nbhds_label = ', '.join(nbhds_selection)
    # st.text(nbhds_label)

    # st.text('Offences --------------------------------------------------------------------------')
    # for n in [crime for crime in crimes_selection if crime != 'All']:
    #     count = list(map_data['type']).count(n)
    #     st.text(n + ": " + str(count))
    # offences_label = ', '.join(crimes_selection)

map_container = st.container()
with map_container:
    st.markdown("---")
    if map_data is not None:
        if len(map_data) != 0:
            tab1, tab2 = st.tabs(["Location Map", "HeatMap"])
            with tab1:
                st.header("Crime Locaion Map")
                st.text("")
                st.subheader(generate_map_title(date_range=time_selection, nbhds=nbhds_selection, crimes=crimes_selection,
                                        all_nbhds=van_nbhds, all_crimes=crime_types)) 
                st.text("")
                st.text("")
                plot_on_map(map_data)
                st.text("")
                st.text("")
                st.dataframe(map_data[['TYPE', 'HUNDRED_BLOCK', 'NEIGHBOURHOOD', 'DATETIME', ]], hide_index=True)
            with tab2:
                st.header("Crime HeatMap")
                st.text("")
                st.subheader(generate_map_title(date_range=time_selection, nbhds=nbhds_selection, crimes=crimes_selection,
                                        all_nbhds=van_nbhds, all_crimes=crime_types)) 
                st.text("")  
                st.text("")
                plot_heatmap(map_data)
                st.text("")
                st.text("")
                st.dataframe(map_data[['TYPE', 'HUNDRED_BLOCK', 'NEIGHBOURHOOD', 'DATETIME', ]], hide_index=True)
            # with tab3:
            #     st.header("Crime HeatMap Over Time")
            #     st.subheader(generate_map_title(date_range=time_selection, nbhds=nbhds_selection, crimes=crimes_selection,
            #                             all_nbhds=van_nbhds, all_crimes=crime_types))
            #     plot_heatmap(map_data, with_time=True)

        else:
            st.warning("There are no crimes fitting the selected options. Try expanding the time range.")

    #     else:
    #         st.warning("No " + offences_label + "'s occured in " + nbhds_label + " during " + years_label)
    #     st.markdown("---")



