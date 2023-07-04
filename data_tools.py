import pandas as pd
from functools import lru_cache

class CrimeDataHandler:
    def __init__(self, data):
        self.data = data
    
    def remove_null_rows(self):
        self.data = self.data.dropna(subset=['NEIGHBOURHOOD', 'X', 'Y'], how='any')
        
    def get_unique_sorted_vals(self, column):
        return sorted(self.data[column].unique())
    
    @lru_cache(maxsize=None) # cache results of method
    def get_data(self, year=None, month=None):
        return self
    

