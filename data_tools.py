import pandas as pd
import psycopg2
from psycopg2 import sql
import streamlit as st

class CrimeDataHandler:
    def __init__(self):
        self.connection_string = self._get_connection_string()

    def _get_connection_string(self):
        postgres_secrets = st.secrets["postgres"]
        return f"postgresql://{postgres_secrets['user']}:{postgres_secrets['password']}@{postgres_secrets['host']}:{postgres_secrets['port']}/{postgres_secrets['dbname']}"

    @st.cache_data(ttl=60)  # Add cache to the get_data function with a time-to-live of 60 seconds
    def get_data(_self, date_range=None, nbhd=None, crime_type=None):
        with psycopg2.connect(_self.connection_string) as conn:
            query = _self._build_query(date_range, nbhd, crime_type)
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(data, columns=columns)

        data.dropna(subset=['neighbourhood', 'x', 'y'], inplace=True)
        return data

    @st.cache_data(ttl=600)
    def get_min_date_from_db(_self):
        with psycopg2.connect(_self.connection_string) as conn:
            with conn.cursor() as cursor:
                query = sql.SQL("SELECT MIN(datetime) FROM crime_data;")
                cursor.execute(query)
                min_date = cursor.fetchone()[0]
        return min_date

    @st.cache_data(ttl=600)
    def get_max_date_from_db(_self):
        with psycopg2.connect(_self.connection_string) as conn:
            with conn.cursor() as cursor:
                query = sql.SQL("SELECT MAX(datetime) FROM crime_data;")
                cursor.execute(query)
                max_date = cursor.fetchone()[0]
        return max_date

    def get_unique_sorted_vals(self, column):
        # Safely escape the column name using string formatting
        query = sql.SQL("SELECT DISTINCT " + column + " FROM crime_data;") # .format(sql.Identifier(column).as_string(conn_or_curs=None))
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                unique_vals = cursor.fetchall()

        unique_vals = [val[0] for val in unique_vals if val[0] is not None]
        return sorted(unique_vals)

    def _build_query(self, date_range, nbhds, crime_types):
        query_template = sql.SQL("SELECT * FROM crime_data WHERE {conditions};")
        conditions = []
        params = {}

        if date_range:
            start_date = date_range[0]
            end_date = date_range[1]
        conditions.append(sql.SQL("datetime >= CAST('" + str(start_date) + "' as date) AND datetime <= CAST('" + str(end_date) + "' as date)"))
        params["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
        params["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S")
        if nbhds:
            conditions.append(sql.SQL("neighbourhood IN " + "(" + str(nbhds)[1:-1] + ")"))
            params["nbhd"] = tuple(nbhds)
        if crime_types:
            conditions.append(sql.SQL("type IN " + "(" + str(crime_types)[1:-1] + ")"))
            params["crime_type"] = tuple(crime_types)

        if not conditions:
            conditions.append(sql.SQL("TRUE"))  # Fetch all rows if no conditions specified

        query = query_template.format(conditions=sql.SQL(" AND ").join(conditions))
        print(query.as_string(context=None))
        return query.as_string(context=None)
