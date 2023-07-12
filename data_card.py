import streamlit as st
from folium.plugins import MarkerCluster

def format_date(month, date, year):
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month - 1]
    return f"{month_name} {date}, {year}"

def format_time(hour, minute):
    am_pm = "AM" if hour < 12 else "PM"
    hour = hour % 12 if hour % 12 != 0 else 12
    return f"{hour:02d}:{minute:02d} {am_pm}"

def generate_popup_html(row):
    offence = row["TYPE"]
    location = row["NEIGHBOURHOOD"]
    block = row["HUNDRED_BLOCK"]
    day = format_date(row["MONTH"], row["DAY"], row["YEAR"])
    time = format_time(row["HOUR"], row["MINUTE"])

    html = f"""
        <div style="font-family: monospace; color: #0c0c0c;">
            <p>{offence}</p>
            <p>{location}, {block}, Vancouver, BC</p>
            <p>{day} at {time}</p>
        </div>
    """
    return html



