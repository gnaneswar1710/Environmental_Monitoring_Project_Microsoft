# import cv2
# import os
# import numpy as np
# import matplotlib.pyplot as plt

# def load_and_analyze_images(image_folder):
#     # Load and sort images
#     image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

#     # Dictionary to store white pixel percentage for each month
#     urban_area_percent_yearly = {}
#     urban_area_percent_monthly = {}
#     for file in image_files:
#         image_path = os.path.join(image_folder, file)

#         # Load image
#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"Failed to load {file}")
#             continue

#         # Convert to HSV color space
#         hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
#         # These values may need fine-tuning based on your image brightness/contrast
#         lower_white = np.array([0, 0, 200])
#         upper_white = np.array([180, 50, 255])
#         mask = cv2.inRange(hsv, lower_white, upper_white)

#         # Count bright pixels
#         bright_pixels = cv2.countNonZero(mask)
#         total_pixels = image.shape[0] * image.shape[1]

#         percent_bright = (bright_pixels / total_pixels) * 100
#         file = file[:15]
#         urban_area_percent_yearly[file[6:10]] = percent_bright  # or adjust date slicing
#         urban_area_percent_monthly[file[6:13]] = percent_bright

#     return urban_area_percent_yearly, urban_area_percent_monthly



# def plot_yearly_bar(urban_area_percent_yearly):
#     urban_year_keys = list(urban_area_percent_yearly.keys())
#     urban_year_values = list(urban_area_percent_yearly.values())
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.bar(urban_year_keys, urban_year_values, color='steelblue')
#     ax.set_title("Urban Expansion Yearly")
#     ax.set_xlabel("Years")
#     ax.set_ylabel("Urban Area (%)")
#     plt.xticks(rotation=45, ha='right')
#     ax.grid(True, linestyle='--', alpha=0.5)
#     plt.tight_layout()
#     return fig

# def plot_yearly_line(urban_area_percent_yearly):
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.plot(list(urban_area_percent_yearly.keys()), list(urban_area_percent_yearly.values()), marker='o', color='navy')
#     ax.set_title("Urban Expansion Yearly")
#     ax.set_xlabel("Years")
#     ax.set_ylabel("Urban Area (%)")
#     ax.grid(True, linestyle='--', alpha=0.4)
#     plt.tight_layout()
#     return fig

# def plot_monthly_line(urban_area_percent_monthly):
#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.plot(list(urban_area_percent_monthly.keys()), list(urban_area_percent_monthly.values()), marker='o', color='darkgreen')
#     ax.set_title("Urban Expansion Monthly")
#     ax.set_xlabel("Months")
#     ax.set_ylabel("Urban Area (%)")
#     plt.xticks(rotation=45, ha='right')
#     ax.grid(True, linestyle='--', alpha=0.4)
#     plt.tight_layout()
#     return fig

# def plot_monthly_bar(urban_area_percent_monthly):
#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.bar(urban_area_percent_monthly.keys(), urban_area_percent_monthly.values(), color='forestgreen')
#     ax.set_title("Urban Expansion Monthly")
#     ax.set_xlabel("Months")
#     ax.set_ylabel("Urban Area (%)")
#     plt.xticks(rotation=45, ha='right')
#     ax.grid(True, linestyle='--', alpha=0.4)
#     plt.tight_layout()
#     return fig

import cv2
import os
import numpy as np
import plotly.graph_objects as go

def load_and_analyze_images(image_folder):
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    urban_area_percent_yearly = {}
    urban_area_percent_monthly = {}

    for file in image_files:
        image_path = os.path.join(image_folder, file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load {file}")
            continue

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 50, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)

        bright_pixels = cv2.countNonZero(mask)
        total_pixels = image.shape[0] * image.shape[1]
        percent_bright = (bright_pixels / total_pixels) * 100

        file = file[:15]
        urban_area_percent_yearly[file[6:10]] = percent_bright
        urban_area_percent_monthly[file[6:13]] = percent_bright

    return urban_area_percent_yearly, urban_area_percent_monthly


def plot_yearly_bar(urban_area_percent_yearly):
    fig = go.Figure(
        data=go.Bar(
            x=list(urban_area_percent_yearly.keys()),
            y=list(urban_area_percent_yearly.values()),
            marker_color='steelblue'
        )
    )
    fig.update_layout(
        title="Urban Expansion Yearly",
        xaxis_title="Years",
        yaxis_title="Urban Area (%)",
        xaxis_tickangle=-45,
        template="plotly_white",
        dragmode='pan',                 
        hovermode='x unified',        
        transition_duration=200,       
        uirevision='constant'
    )
    return fig


def plot_yearly_line(urban_area_percent_yearly):
    fig = go.Figure(
        data=go.Scatter(
            x=list(urban_area_percent_yearly.keys()),
            y=list(urban_area_percent_yearly.values()),
            mode='lines+markers',
            marker=dict(color='blue')
        )
    )
    fig.update_layout(
        title="Urban Expansion Yearly",
        xaxis_title="Years",
        yaxis_title="Urban Area (%)",
        template="plotly_white",
        dragmode='pan',                 
        hovermode='x unified',        
        transition_duration=200,       
        uirevision='constant'
    )
    return fig


def plot_monthly_bar(urban_area_percent_monthly):
    fig = go.Figure(
        data=go.Bar(
            x=list(urban_area_percent_monthly.keys()),
            y=list(urban_area_percent_monthly.values()),
            marker_color='forestgreen'
        )
    )
    fig.update_layout(
        title="Urban Expansion Monthly",
        xaxis_title="Months",
        yaxis_title="Urban Area (%)",
        xaxis_tickangle=-45,
        template="plotly_white",
        dragmode='pan',                 
        hovermode='x unified',        
        transition_duration=200,       
        uirevision='constant'
    )
    return fig


def plot_monthly_line(urban_area_percent_monthly):
    fig = go.Figure(
        data=go.Scatter(
            x=list(urban_area_percent_monthly.keys()),
            y=list(urban_area_percent_monthly.values()),
            mode='lines+markers',
            marker=dict(color='darkgreen')
        )
    )
    fig.update_layout(
        title="Urban Expansion Monthly",
        xaxis_title="Months",
        yaxis_title="Urban Area (%)",
        template="plotly_white",
        dragmode='pan',                 
        hovermode='x unified',        
        transition_duration=200,       
        uirevision='constant'
    )
    return fig
