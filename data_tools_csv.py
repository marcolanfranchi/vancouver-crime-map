import streamlit as st
import pandas as pd

class CrimeDataHandler:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.data = None

    # @st.cache_data
    def load_data(self):
        # Load data from the CSV file
        self.data = pd.read_csv(self.csv_file_path)
        self.preprocess_data()
        self.add_datetime_column()

    # Removes data with no location point
    def preprocess_data(self):
        self.data = self.data.dropna(subset=['NEIGHBOURHOOD', 'X', 'Y'], how='any')
        self.data = self.data.loc[(self.data['X'] != 0) | (self.data['Y'] != 0)]

    def add_datetime_column(self):
        # Ensure all columns are in uppercase
        self.data.columns = self.data.columns.str.upper()

        # Add a 'datetime' column by combining year, month, day, hour, and minute
        self.data['DATETIME'] = pd.to_datetime(self.data[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']])

    # @st.cache_data()
    def get_unique_sorted_vals(self, column):
        return sorted(self.data[column].unique())

     #@st.cache_data
    def get_filtered_data(self, date_range=[], nbhds=[], crimes=[]):
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_data = self.data[(self.data['DATETIME'] >= start_date) & (self.data['DATETIME'] <= end_date)]
        
        if nbhds:
            filtered_data = filtered_data[filtered_data['NEIGHBOURHOOD'].isin(nbhds)]

        if crimes:
            filtered_data = filtered_data[filtered_data['TYPE'].isin(crimes)]

        return filtered_data


    def get_min_date(self):
        min_date = self.data['DATETIME'].min()
        return min_date

    def get_max_date(self):
        max_date = self.data['DATETIME'].max()
        return max_date