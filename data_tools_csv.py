import streamlit as st
import pandas as pd
import utm as utm

@st.cache_data
def csv_to_df(csv_file_path):
    return pd.read_csv(csv_file_path)

@st.cache_data
def cached_get_sorted_vals(data, column):
    return sorted(data[column].unique())


@st.cache_data
def cached_get_date(data, min_or_max):
    if min_or_max == 'min':
        return data['DATETIME'].min()
    else:
        return data['DATETIME'].max()


class CrimeDataHandler:
    def __init__(self):
        self.data = None


    def load_data(self, csv_file_path):
        # Load data from the CSV file
        self.data = csv_to_df(csv_file_path)
        self.preprocess_data()
        self.add_datetime_column()
        self.add_lat_lon_columns()

    # Removes data with no location point
    def preprocess_data(self):
        self.data = self.data.dropna(subset=['NEIGHBOURHOOD', 'X', 'Y'], how='any')
        self.data = self.data.loc[(self.data['X'] != 0) | (self.data['Y'] != 0)]

    def add_datetime_column(self):
        # Ensure all columns are in uppercase
        self.data.columns = self.data.columns.str.upper()

        # Add a 'datetime' column by combining year, month, day, hour, and minute
        self.data['DATETIME'] = pd.to_datetime(self.data[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']])

    def add_lat_lon_columns(self):
        self.data['LAT'], self.data['LON'] = utm.to_latlon(self.data['X'], self.data['Y'], 10, 'N')


    def get_unique_sorted_vals(self, column):
        return cached_get_sorted_vals(self.data, column)

    def get_filtered_data(self, date_range=[], nbhds=[], crimes=[]):
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]) + pd.DateOffset(hours=23, minutes=59)
        filtered_data = self.data[(self.data['DATETIME'] >= start_date) & (self.data['DATETIME'] <= end_date)]
        
        if nbhds:
            filtered_data = filtered_data[filtered_data['NEIGHBOURHOOD'].isin(nbhds)]

        if crimes:
            filtered_data = filtered_data[filtered_data['TYPE'].isin(crimes)]

        return filtered_data


    def get_min_date(self):
        return cached_get_date(self.data, 'min')

    def get_max_date(self):
        return cached_get_date(self.data, 'max')