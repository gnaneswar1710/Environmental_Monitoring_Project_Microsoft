import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def load_and_analyze_images(image_folder):
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    percentage_changes = {}

    for i in range(1, len(image_files)):
        prev = cv2.imread(os.path.join(image_folder, image_files[i - 1]), cv2.IMREAD_GRAYSCALE)
        curr = cv2.imread(os.path.join(image_folder, image_files[i]), cv2.IMREAD_GRAYSCALE)

        if prev is None or curr is None:
            continue

        if prev.shape != curr.shape:
            curr = cv2.resize(curr, (prev.shape[1], prev.shape[0]))

        diff = cv2.absdiff(curr, prev)
        percent_diff = np.sum(diff > 25) / diff.size * 100
        dates = f"{image_files[i-1][6:13]} → {image_files[i][6:13]}"
        # dates = f"{image_files[i-1][6:13]}"
        percentage_changes[dates] = percent_diff

    return percentage_changes


def plot_monthly_bar(percentage_changes):
    df = pd.DataFrame(list(percentage_changes.items()), columns=['Date', 'Change (%)'])
    fig = px.bar(df, x='Date', y='Change (%)', title="Monthly Deforestation Change", color='Change (%)')
    fig.update_layout(xaxis_title="Months", yaxis_title="Deforestation Change (%)", xaxis_tickangle=-45, dragmode='pan', hovermode='x unified', transition_duration=200, uirevision='constant',)
    return fig


def plot_monthly_line(percentage_changes):
    df = pd.DataFrame(list(percentage_changes.items()), columns=['Date', 'Change (%)'])
    fig = px.line(df, x='Date', y='Change (%)', title="Monthly Deforestation Change", markers=True)
    fig.update_layout(xaxis_title="Months", yaxis_title="Deforestation Change (%)", xaxis_tickangle=-45,  dragmode='pan', hovermode='x unified', transition_duration=200, uirevision='constant',)
    return fig

def compute_yearly_avg(percentage_changes):
    yearly_changes = {}
    for dates, percent in percentage_changes.items():
        year = dates.split("→")[1].strip()[:4]
        # year = dates[:4]
        yearly_changes.setdefault(year, []).append(percent)
    return {year: np.mean(vals) for year, vals in yearly_changes.items()}



def plot_yearly_bar(yearly_data):
    df = pd.DataFrame(list(yearly_data.items()), columns=['Year', 'Average Change (%)'])
    fig = px.bar(df, x='Year', y='Average Change (%)', title="Yearly Deforestation Change", color='Average Change (%)')
    fig.update_layout(xaxis_title="Years", yaxis_title="Avg. Change (%)",  dragmode='pan', hovermode='x unified', transition_duration=200, uirevision='constant',)
    return fig

def plot_yearly_line(yearly_data):
    df = pd.DataFrame(list(yearly_data.items()), columns=['Year', 'Average Change (%)'])
    fig = px.line(df, x='Year', y='Average Change (%)', title="Yearly Deforestation Change", markers=True)
    fig.update_layout(xaxis_title="Years", yaxis_title="Avg. Change (%)",dragmode='pan', hovermode='x unified', transition_duration=200, uirevision='constant',)
    return fig
