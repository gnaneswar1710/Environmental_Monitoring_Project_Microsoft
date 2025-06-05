import os
import streamlit as st
import deforestation as defo
import urban_expansion as urban
import water_shrinkage as water
import plotly.graph_objects as go
import cv2
import time



st.set_page_config(page_title="Environmental Monitoring Dashboard", layout="wide")
st.title("Environmental Monitoring Dashboard")

# Project selection
project = st.sidebar.selectbox("Select Project", ["Deforestation", "Urban Expansion", "Water Shrinkage"])

# Conditional views based on selected project
if project == "Water Shrinkage":
    view = "Monthly"
else:
    view = st.sidebar.radio("Select View", ["Yearly", "Monthly"])

plot_type = st.sidebar.radio("Plot Type", ["Line Plot", "Bar Plot"])

plot_config = {
    "scrollZoom": True,
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "doubleClick": "reset",
}

class Deforestation:
    def __init__(self, yearly_data, df):
        self.yearly_data = yearly_data
        self.df = df

    def deforestation_yearly(self):
        image_dir2 = "DEFORESTATION_IMAGES\\Deforestation_yearly_color_images"
        image_files2 = sorted([f for f in os.listdir(image_dir2) if f.endswith('.png')])

        dates2 = list(self.yearly_data.keys())
        per_change2 = list(self.yearly_data.values())

        # Sidebar Controls
        enable_timelapse = st.sidebar.checkbox("Enable Timelapse")
        timelapse_speed = st.sidebar.slider("Timelapse Speed (sec/frame)", 0.1, 2.0, 0.5, 0.1)
        # Initialize session state for timelapse
        if enable_timelapse:
            if "is_playing2" not in st.session_state:
                st.session_state.is_playing2 = False
            if "frame_idx2" not in st.session_state:
                st.session_state.frame_idx2 = 0
            if "start_idx2" not in st.session_state:
                st.session_state.start_idx2 = 0
            if "end_idx2" not in st.session_state:
                st.session_state.end_idx2 = len(dates2) - 1


            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates2, y=per_change2, mode='lines+markers', name='Deforest Change (%)', line=dict(color='skyblue')))
            marker_trace = go.Scatter(x=[dates2[0]], y=[per_change2[0]], mode='markers', name='Current Point', marker=dict(color='red', size=10))
            fig.add_trace(marker_trace)
            fig.update_layout(title="Deforestation Yearly", xaxis_title="Yearly", yaxis_title="Change (%)", template="plotly_dark")

            
            if enable_timelapse:
                st.subheader("Timelapse Playback")

                start_idx2, end_idx2 = st.select_slider(
                    "Select Range for Timelapse",
                    options=list(range(len(dates2))),
                    value=(st.session_state.start_idx2, st.session_state.end_idx2),
                    format_func=lambda i: dates2[i]
                )
                st.session_state.start_idx2 = start_idx2
                st.session_state.end_idx2 = end_idx2

                # Ensure frame is within selected range
                if st.session_state.frame_idx2 < start_idx2 or st.session_state.frame_idx2 > end_idx2:
                    st.session_state.frame_idx2 = start_idx2

                # Layout columns for plot and image side by side
                plot_col, image_col = st.columns([2, 1])

                # Update marker position on plot
                fig.data[1].x = [dates2[st.session_state.frame_idx2]]
                fig.data[1].y = [per_change2[st.session_state.frame_idx2]]

                with plot_col:
                    st.plotly_chart(fig, use_container_width=True)

                with image_col:
                    current_image = os.path.join(image_dir2, image_files2[st.session_state.frame_idx2])
                    st.image(current_image, caption=f"Date: {dates2[st.session_state.frame_idx2]}", use_container_width=True)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    play_clicked = st.button("▶ Play")
                with col2:
                    pause_clicked = st.button("⏸ Pause")
                with col3:
                    reset_clicked = st.button("🔄 Reset")

                if play_clicked:
                    st.session_state.is_playing2 = True
                if pause_clicked:
                    st.session_state.is_playing2 = False
                if reset_clicked:
                    st.session_state.is_playing2 = False
                    st.session_state.start_idx2 = 0
                    st.session_state.end_idx2 = len(dates2) - 1
                    st.session_state.frame_idx2 = 0
                    st.rerun()

                # If playing, move forward
                if st.session_state.is_playing2:
                    time.sleep(timelapse_speed)
                    if st.session_state.frame_idx2 < end_idx2:
                        st.session_state.frame_idx2 += 1
                    else:
                        st.session_state.is_playing2 = False 
                    st.rerun()

            else:
                plot_col, image_col = st.columns([2, 1])
                with plot_col:
                    fig.data[1].x = [dates2[0]]
                    fig.data[1].y = [per_change2[0]]
                    st.plotly_chart(fig, use_container_width=True)
                with image_col:
                    current_image = os.path.join(image_dir2, image_files2[0])
                    st.image(current_image, caption=f"Date: {dates2[0]}", use_container_width=True)
        else:
            fig = defo.plot_yearly_line(self.yearly_data) if plot_type == "Line Plot" else defo.plot_yearly_bar(self.yearly_data)
            st.plotly_chart(fig, use_container_width=True, config = plot_config)


    def deforestation_monthly(self):
        image_dir3 = "DEFORESTATION_IMAGES\\Deforestation_monthly_color_images"
        image_files3 = sorted([f for f in os.listdir(image_dir3) if f.endswith('.png')])

        dates3 = list(self.df.keys())
        per_change3 = list(self.df.values())
         # Sidebar Controls
        enable_timelapse = st.sidebar.checkbox("Enable Timelapse")
        timelapse_speed = st.sidebar.slider("Timelapse Speed (sec/frame)", 0.1, 2.0, 0.5, 0.1)
        if enable_timelapse:
            # Initialize session state for timelapse
            if "is_playing3" not in st.session_state:
                st.session_state.is_playing3 = False
            if "frame_idx3" not in st.session_state:
                st.session_state.frame_idx3 = 0
            if "start_idx3" not in st.session_state:
                st.session_state.start_idx3 = 0
            if "end_idx3" not in st.session_state:
                st.session_state.end_idx3 = len(dates3) - 1

            # Static Plot with dynamic marker
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates3, y=per_change3, mode='lines+markers', name='Deforestation Changes (%)', line=dict(color='skyblue')))
            marker_trace = go.Scatter(x=[dates3[0]], y=[per_change3[0]], mode='markers', name='Current Point', marker=dict(color='red', size=10))
            fig.add_trace(marker_trace)
            fig.update_layout(title="Deforestation Monnthly", xaxis_title="Months", yaxis_title="Changes (%)", template="plotly_dark")


            if enable_timelapse:
                st.subheader("Timelapse Playback")

                start_idx3, end_idx3 = st.select_slider(
                    "Select Range for Timelapse",
                    options=list(range(len(dates3))),
                    value=(st.session_state.start_idx3, st.session_state.end_idx3),
                    format_func=lambda i: dates3[i]
                )
                st.session_state.start_idx3 = start_idx3
                st.session_state.end_idx3 = end_idx3

                
                if st.session_state.frame_idx3 < start_idx3 or st.session_state.frame_idx3 > end_idx3:
                    st.session_state.frame_idx3 = start_idx3

                # Layout columns for plot and image side by side
                plot_col, image_col = st.columns([2, 1])

                # Update marker position on plot
                fig.data[1].x = [dates3[st.session_state.frame_idx3]]
                fig.data[1].y = [per_change3[st.session_state.frame_idx3]]

                with plot_col:
                    st.plotly_chart(fig, use_container_width=True)

                with image_col:
                    current_image = os.path.join(image_dir3, image_files3[st.session_state.frame_idx3])
                    st.image(current_image, caption=f"Date: {dates3[st.session_state.frame_idx3]}", use_container_width=True)

                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    play_clicked = st.button("▶ Play")
                with col2:
                    pause_clicked = st.button("⏸ Pause")
                with col3:
                    reset_clicked = st.button("🔄 Reset")

                if play_clicked:
                    st.session_state.is_playing3 = True
                if pause_clicked:
                    st.session_state.is_playing3 = False
                if reset_clicked:
                    st.session_state.is_playing3 = False
                    st.session_state.start_idx3 = 0
                    st.session_state.end_idx3 = len(dates3) - 1
                    st.session_state.frame_idx3 = 0
                    st.rerun()

                # If playing, move forward
                if st.session_state.is_playing3:
                    time.sleep(timelapse_speed)
                    if st.session_state.frame_idx3 < end_idx3:
                        st.session_state.frame_idx3 += 1
                    else:
                        st.session_state.is_playing3 = False
                    st.rerun()

            else:
                plot_col, image_col = st.columns([2, 1])
                with plot_col:
                    fig.data[1].x = [dates3[0]]
                    fig.data[1].y = [per_change3[0]]
                    st.plotly_chart(fig, use_container_width=True)
                with image_col:
                    current_image = os.path.join(image_dir3, image_files3[0])
                    st.image(current_image, caption=f"Date: {dates3[0]}", use_container_width=True)
        else:
            fig = defo.plot_monthly_line(self.df) if plot_type == "Line Plot" else defo.plot_monthly_bar(self.df)
            st.plotly_chart(fig, use_container_width=True, config = plot_config)



class UrbanExpansion:
    def __init__(self, urban_area_percent_yearly, urban_area_percent_monthly):
        self.urban_area_percent_yearly = urban_area_percent_yearly
        self.urban_area_percent_monthly = urban_area_percent_monthly

    def urban_expansion_yearly(self):
        image_dir1 = "URBAN_EXPANSION_IMAGES\\Urban_expansion_yearly_images"
        image_files1 = sorted([f for f in os.listdir(image_dir1) if f.endswith('.png')])

        dates1 = list(self.urban_area_percent_yearly.keys())
        per_change1 = list(self.urban_area_percent_yearly.values())

        # Sidebar Controls
        enable_timelapse = st.sidebar.checkbox("Enable Timelapse")
        timelapse_speed = st.sidebar.slider("Timelapse Speed (sec/frame)", 0.1, 2.0, 0.5, 0.1)
        if enable_timelapse:
            # Initialize session state for timelapse
            if "is_playing1" not in st.session_state:
                st.session_state.is_playing1 = False
            if "frame_idx1" not in st.session_state:
                st.session_state.frame_idx1 = 0
            if "start_idx1" not in st.session_state:
                st.session_state.start_idx1 = 0
            if "end_idx1" not in st.session_state:
                st.session_state.end_idx1 = len(dates1) - 1


            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates1, y=per_change1, mode='lines+markers', name='Expansion (%)', line=dict(color='skyblue')))
            marker_trace = go.Scatter(x=[dates1[0]], y=[per_change1[0]], mode='markers', name='Current Point', marker=dict(color='red', size=10))
            fig.add_trace(marker_trace)
            fig.update_layout(title="Urban Expansion Yearly", xaxis_title="Yearly", yaxis_title="Urban Area (%)", template="plotly_dark")


            if enable_timelapse:
                st.subheader("Timelapse Playback")

                start_idx1, end_idx1 = st.select_slider(
                    "Select Range for Timelapse",
                    options=list(range(len(dates1))),
                    value=(st.session_state.start_idx1, st.session_state.end_idx1),
                    format_func=lambda i: dates1[i]
                )
                st.session_state.start_idx1 = start_idx1
                st.session_state.end_idx1 = end_idx1


                
                if st.session_state.frame_idx1 < start_idx1 or st.session_state.frame_idx1 > end_idx1:
                    st.session_state.frame_idx1 = start_idx1

                # Layout columns for plot and image side by side
                plot_col, image_col = st.columns([2, 1])

                # Update marker position on plot
                fig.data[1].x = [dates1[st.session_state.frame_idx1]]
                fig.data[1].y = [per_change1[st.session_state.frame_idx1]]

                with plot_col:
                    st.plotly_chart(fig, use_container_width=True)

                with image_col:
                    current_image = os.path.join(image_dir1, image_files1[st.session_state.frame_idx1])
                    st.image(current_image, caption=f"Date: {dates1[st.session_state.frame_idx1]}", use_container_width=True)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    play_clicked = st.button("▶ Play")
                with col2:
                    pause_clicked = st.button("⏸ Pause")
                with col3:
                    reset_clicked = st.button("🔄 Reset")

                if play_clicked:
                    st.session_state.is_playing1 = True
                if pause_clicked:
                    st.session_state.is_playing1 = False
                if reset_clicked:
                    st.session_state.is_playing1 = False
                    st.session_state.start_idx1 = 0
                    st.session_state.end_idx1 = len(dates1) - 1
                    st.session_state.frame_idx1 = 0
                    st.rerun()

                # If playing, move forward
                if st.session_state.is_playing1:
                    time.sleep(timelapse_speed)
                    if st.session_state.frame_idx1 < end_idx1:
                        st.session_state.frame_idx1 += 1
                    else:
                        st.session_state.is_playing1 = False
                    st.rerun()

            else:
                plot_col, image_col = st.columns([2, 1])
                with plot_col:
                    fig.data[1].x = [dates1[0]]
                    fig.data[1].y = [per_change1[0]]
                    st.plotly_chart(fig, use_container_width=True)
                with image_col:
                    current_image = os.path.join(image_dir1, image_files1[0])
                    st.image(current_image, caption=f"Date: {dates1[0][:4]}", use_container_width=True)
        else:
            fig = urban.plot_yearly_line(self.urban_area_percent_yearly) if plot_type == "Line Plot" else urban.plot_yearly_bar(self.urban_area_percent_yearly)
            st.plotly_chart(fig, use_container_width=True, config = plot_config)

    def urban_expansion_monthly(self):
        image_dir0 = "URBAN_EXPANSION_IMAGES\\Urban_expansion_monthly_color"
        image_files0 = sorted([f for f in os.listdir(image_dir0) if f.endswith('.png')])

        dates0 = list(self.urban_area_percent_monthly.keys())
        per_change0 = list(self.urban_area_percent_monthly.values())

        # Sidebar Controls
        enable_timelapse = st.sidebar.checkbox("Enable Timelapse")
        timelapse_speed = st.sidebar.slider("Timelapse Speed (sec/frame)", 0.1, 2.0, 0.5, 0.1)
        if enable_timelapse:
            # Initialize session state for timelapse
            if "is_playing0" not in st.session_state:
                st.session_state.is_playing0 = False
            if "frame_idx0" not in st.session_state:
                st.session_state.frame_idx0 = 0
            if "start_idx0" not in st.session_state:
                st.session_state.start_idx0 = 0
            if "end_idx0" not in st.session_state:
                st.session_state.end_idx0 = len(dates0) - 1

            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates0, y=per_change0, mode='lines+markers', name='Expansion (%)', line=dict(color='skyblue')))
            marker_trace = go.Scatter(x=[dates0[0]], y=[per_change0[0]], mode='markers', name='Current Point', marker=dict(color='red', size=10))
            fig.add_trace(marker_trace)
            fig.update_layout(title="Urban Expansion Monnthly", xaxis_title="Months", yaxis_title="Urban Area (%)", template="plotly_dark")


            if enable_timelapse:
                st.subheader("Timelapse Playback")

                start_idx0, end_idx0 = st.select_slider(
                    "Select Range for Timelapse",
                    options=list(range(len(dates0))),
                    value=(st.session_state.start_idx0, st.session_state.end_idx0),
                    format_func=lambda i: dates0[i]
                )
                st.session_state.start_idx0 = start_idx0
                st.session_state.end_idx0 = end_idx0



                if st.session_state.frame_idx0 < start_idx0 or st.session_state.frame_idx0 > end_idx0:
                    st.session_state.frame_idx0 = start_idx0

                # Layout columns for plot and image side by side
                plot_col, image_col = st.columns([2, 1]) 

                # Update marker position on plot
                fig.data[1].x = [dates0[st.session_state.frame_idx0]]
                fig.data[1].y = [per_change0[st.session_state.frame_idx0]]

                with plot_col:
                    st.plotly_chart(fig, use_container_width=True)

                with image_col:
                    current_image = os.path.join(image_dir0, image_files0[st.session_state.frame_idx0])
                    st.image(current_image, caption=f"Date: {dates0[st.session_state.frame_idx0]}", use_container_width=True)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    play_clicked = st.button("▶ Play")
                with col2:
                    pause_clicked = st.button("⏸ Pause")
                with col3:
                    reset_clicked = st.button("🔄 Reset")

                if play_clicked:
                    st.session_state.is_playing0 = True
                if pause_clicked:
                    st.session_state.is_playing0 = False
                if reset_clicked:
                    st.session_state.is_playing0 = False
                    st.session_state.start_idx0 = 0
                    st.session_state.end_idx0 = len(dates0) - 1
                    st.session_state.frame_idx0 = 0
                    st.rerun()

                # If playing, move forward
                if st.session_state.is_playing0:
                    time.sleep(timelapse_speed)
                    if st.session_state.frame_idx0 < end_idx0:
                        st.session_state.frame_idx0 += 1
                    else:
                        st.session_state.is_playing0 = False
                    st.rerun()

            else:
                plot_col, image_col = st.columns([2, 1])
                with plot_col:
                    fig.data[1].x = [dates0[0]]
                    fig.data[1].y = [per_change0[0]]
                    st.plotly_chart(fig, use_container_width=True)
                with image_col:
                    current_image = os.path.join(image_dir0, image_files0[0])
                    st.image(current_image, caption=f"Date: {dates0[0]}", use_container_width=True)
        else:
            fig = urban.plot_monthly_line(self.urban_area_percent_monthly) if plot_type == "Line Plot" else urban.plot_monthly_bar(self.urban_area_percent_monthly)
            st.plotly_chart(fig, use_container_width=True, config = plot_config)



class WaterShrinkage:
    def __init__(self, dates, shrinkages, image_files):
        self.dates = dates
        self.shrinkages = shrinkages
        self.image_files = image_files

    def water_shrinkage_monthly(self):
        image_dir = "WATER_SHRINKAGE_IMAGES\\Water_shrinkage_color_images"
        # Sidebar Controls
        enable_timelapse = st.sidebar.checkbox("Enable Timelapse")
        timelapse_speed = st.sidebar.slider("Timelapse Speed (sec/frame)", 0.1, 2.0, 0.5, 0.1)
        if enable_timelapse:
            # Initialize session state for timelapse
            if "is_playing" not in st.session_state:
                st.session_state.is_playing = False
            if "frame_idx" not in st.session_state:
                st.session_state.frame_idx = 0
            if "start_idx" not in st.session_state:
                st.session_state.start_idx = 0
            if "end_idx" not in st.session_state:
                st.session_state.end_idx = len(self.dates) - 1

        
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.dates, y=self.shrinkages, mode='lines+markers', name='Shrinkage (%)', line=dict(color='skyblue')))
            marker_trace = go.Scatter(x=[self.dates[0]], y=[self.shrinkages[0]], mode='markers', name='Current Point', marker=dict(color='red', size=10))
            fig.add_trace(marker_trace)
            fig.update_layout(title="Monthly Water Shrinkage Change", xaxis_title="Months", yaxis_title="Change (%)", template="plotly_dark")


            if enable_timelapse:
                st.subheader("Timelapse Playback")

                start_idx, end_idx = st.select_slider(
                    "Select Range for Timelapse",
                    options=list(range(len(self.dates))),
                    value=(st.session_state.start_idx, st.session_state.end_idx),
                    format_func=lambda i: self.dates[i]
                )
                st.session_state.start_idx = start_idx
                st.session_state.end_idx = end_idx


            
                if st.session_state.frame_idx < start_idx or st.session_state.frame_idx > end_idx:
                    st.session_state.frame_idx = start_idx

                # Layout columns for plot and image side by side
                plot_col, image_col = st.columns([2, 1])

                # Update marker position on plot
                fig.data[1].x = [self.dates[st.session_state.frame_idx]]
                fig.data[1].y = [self.shrinkages[st.session_state.frame_idx]]

                with plot_col:
                    st.plotly_chart(fig, use_container_width=True)

                with image_col:
                    current_image = os.path.join(image_dir, self.image_files[st.session_state.frame_idx])
                    st.image(current_image, caption=f"Date: {self.dates[st.session_state.frame_idx]}", use_container_width=True)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    play_clicked = st.button("▶ Play")
                with col2:
                    pause_clicked = st.button("⏸ Pause")
                with col3:
                    reset_clicked = st.button("🔄 Reset")

                if play_clicked:
                    st.session_state.is_playing = True
                if pause_clicked:
                    st.session_state.is_playing = False
                if reset_clicked:
                    st.session_state.is_playing = False
                    st.session_state.start_idx = 0
                    st.session_state.end_idx = len(dates) - 1
                    st.session_state.frame_idx = 0
                    st.rerun()

                
                if st.session_state.is_playing:
                    time.sleep(timelapse_speed)
                    if st.session_state.frame_idx < end_idx:
                        st.session_state.frame_idx += 1
                    else:
                        st.session_state.is_playing = False 
                    st.rerun()

            else:
                plot_col, image_col = st.columns([2, 1])
                with plot_col:
                    fig.data[1].x = [self.dates[0]]
                    fig.data[1].y = [self.shrinkages[0]]
                    st.plotly_chart(fig, use_container_width=True)
                with image_col:
                    current_image = os.path.join(image_dir, self.image_files[0])
                    st.image(current_image, caption=f"Date: {self.dates[0]}", use_container_width=True)
        else:
            fig = water.plot_monthly_line(self.dates, self.shrinkages) if plot_type == "Line Plot" else water.plot_monthly_bar(self.dates, self.shrinkages)
            st.plotly_chart(fig, use_container_width=True, config = plot_config)


if __name__ == "__main__":
    #Deforestation Main
    if project == "Deforestation":
        image_folder_deforestation = "DEFORESTATION_IMAGES\\Deforestation_monthly_images"
        df = defo.load_and_analyze_images(image_folder_deforestation)
        st.subheader("Deforestation")
        yearly_data = defo.compute_yearly_avg(df)
        de = Deforestation(yearly_data, df)
        if view == 'Yearly':
            de.deforestation_yearly()
        elif view == 'Monthly':
            de.deforestation_monthly()

    #Urban Expansion Main
    elif project == "Urban Expansion":
        image_folder_urbanexpansion = "URBAN_EXPANSION_IMAGES\\Urban_expansion_monthly_images"
        urban_area_percent_yearly,urban_area_percent_monthly = urban.load_and_analyze_images(image_folder_urbanexpansion)
        st.subheader("Urban Expansion")
        ue = UrbanExpansion(urban_area_percent_yearly, urban_area_percent_monthly)
        if view == 'Yearly':
            ue.urban_expansion_yearly()
        elif view == 'Monthly':
            ue.urban_expansion_monthly()

    #Water Shrinkage Main
    elif project == "Water Shrinkage":
        image_folder_watershrinkage = "WATER_SHRINKAGE_IMAGES\\Water_shrinkage_satellite_images"
        dates, shrinkages, image_files = water.load_and_analyze_images(image_folder_watershrinkage)    
        st.subheader("Water Shrinkage")
        ws = WaterShrinkage(dates, shrinkages, image_files)
        if view == 'Monthly':
            ws.water_shrinkage_monthly()
        