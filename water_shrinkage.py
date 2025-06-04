import cv2
import os
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import datetime

def calculate_water_area(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.bitwise_not(thresh)
    water_pixels = cv2.countNonZero(thresh)
    total_pixels = img.shape[0] * img.shape[1]
    water_percent = (water_pixels / total_pixels) * 100
    return water_percent

def load_and_analyze_images(image_folder):
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    water_areas = []
    dates = []

    for f in image_files:
        path = os.path.join(image_folder, f)
        water_percent = calculate_water_area(path)
        if water_percent is not None:
            date_str = f[6:13]  
            # date = datetime.strptime(date_str, "%Y-%m")
            dates.append(date_str)
            water_areas.append(water_percent)

    if not water_areas:
        return [], []

    base_area = water_areas[0]
    # shrinkages = [(base_area - area) / base_area * 100 for area in water_areas]
    shrinkages = [(area - base_area) / base_area * 100 for area in water_areas]

    return dates, shrinkages, image_files

def plot_monthly_line(dates, shrinkages):
    fig = go.Figure(
        data=go.Scatter(
            x=dates,
            y=shrinkages,
            mode='lines+markers',
            marker=dict(color='skyblue')
        )
    )
    fig.update_layout(
        title="Water Shrinkage/Growth Percentage Monthly",
        xaxis_title="Month",
        yaxis_title="Change (%)",
        xaxis_tickangle=-45,
        template="plotly_white",
        dragmode='pan',                 
        hovermode='x unified',        
        transition_duration=200,       
        uirevision='constant'
    )
    return fig


def plot_monthly_bar(dates, shrinkages):
    fig = go.Figure(
        data=go.Bar(
            x=dates,
            y=shrinkages,
            marker_color='forestgreen'
        )
    )
    fig.update_layout(
        title="Water Shrinkage/Growth Percentage Monthly",
        xaxis_title="Month",
        yaxis_title="Change (%)",
        xaxis_tickangle=-45,
        template="plotly_white",
        dragmode='pan',                 
        hovermode='x unified',        
        transition_duration=200,       
        uirevision='constant'
    )
    return fig
