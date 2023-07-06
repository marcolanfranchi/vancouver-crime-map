import pandas as pd
from functools import lru_cache

class CrimeDataHandler:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        self.preprocess_data()

    def preprocess_data(self):
        self.data = self.data.dropna(subset=['NEIGHBOURHOOD', 'X', 'Y'], how='any')
        self.data = self.data.loc[(self.data['X'] != 0) | (self.data['Y'] != 0)]
        
    def get_unique_sorted_vals(self, column):
        return sorted(self.data[column].unique())
    
    # @lru_cache(maxsize=None) # cache results of method
    def get_data(self, year=[], nbhd=[], crime_type=[]):
        filtered_data = self.data.copy()
        
        if year:
            filtered_data = filtered_data[filtered_data['YEAR'].isin(year)]
        if nbhd:
            filtered_data = filtered_data[filtered_data['NEIGHBOURHOOD'].isin(nbhd)]
        if crime_type:
            filtered_data = filtered_data[filtered_data['TYPE'].isin(crime_type)]
        
        filtered_data['COORDS'] = list(zip(filtered_data['X'], filtered_data['Y']))
        
        return filtered_data
