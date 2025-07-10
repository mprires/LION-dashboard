import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import constants
import numpy as np


def aggregate_sites(df):
    """
    Aggregates site information for each country into a single string.

    Parameters:
    - df (DataFrame): The DataFrame containing 'Country', 'Site', and 'Number of expected cases'.

    Returns:
    - DataFrame: A DataFrame with aggregated site information.
    """
    # Group by 'Country' and aggregate sites
    grouped = df.groupby('Country').agg({
        'Site': lambda x: '<br>'.join(x),
        'Number of expected cases': 'sum'
    }).reset_index()

    return grouped


def world_map_plot(df):

    aggregated_df = aggregate_sites(df)

    fig = go.Figure(data=go.Choropleth(
        locations=aggregated_df['Country'],
        z=aggregated_df['Number of expected cases'],
        text=aggregated_df['Site'],
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar=dict(title=None),
        colorscale=px.colors.sequential.Plasma,
        showscale=True,

    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcountries=True,
            showcoastlines=True,
            bgcolor="#0E1117",
            landcolor="#343A40",
            showlakes=False,
            projection_type='equirectangular',
        ),
        width=1500,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    fig.update_traces(
        hovertemplate="'<b>%{text}</b><br>Country: %{location}<br>Cases: %{z}<br><extra></extra>"
    )

    return fig

def donut_plot(df, target_column, expected_total):

    sum_values = df[target_column].sum()
    remaining_value = expected_total - sum_values
    pastel_colors = ['#BCABAE', '#0F0F0F']
    plot_data = pd.DataFrame({"Category": ["Curated", "Remaining"],
                              "Value": [sum_values, remaining_value]})

    plot_data['percentage'] = (plot_data['Value'] / expected_total) * 100

    plot = alt.Chart(plot_data, autosize="fit").mark_arc(innerRadius=70).encode(
        theta=alt.Theta(field="Value", type="quantitative", stack=True),
        color = alt.Color(field='Category', type='nominal', scale=alt.Scale(range=pastel_colors), legend=alt.Legend(title='Category')),
        tooltip=[alt.Tooltip(field='Category', type='nominal', title='Category'),
                 alt.Tooltip(field='Value', type='quantitative', title='Value'),
                 alt.Tooltip(field='percentage', type='quantitative', title='Percentage')]
    ).properties(width=200,
                 height=200
    ).configure_view(
        clip=False,
        strokeOpacity=0  # Remove the border around the plot area
    )
    return plot


def create_stacked_vertical_bar_chart(df, max_value, bar_height=200, bar_width=40):
    """
    Creates a vertical stacked bar chart representing progress.

    Parameters:
    - df (DataFrame): The DataFrame containing the data.
    - max_value (float): The maximum value for the progress.
    - bar_height (int): The height of the vertical bar chart.
    - bar_width (int): The width of the vertical bar chart.
    - title (str): Optional title displayed above the bar chart.
    """
    value = df["Number of verified cases"].sum()
    remaining_value = max_value - value
    progress_percentage = value / max_value  # Calculate the progress percentage

    # Create the data for the stacked bar chart
    bar_data = pd.DataFrame({
        'Category': ['Completed', 'Remaining'],
        'Value': [value, remaining_value]
    })

    # Create the stacked bar chart using Altair
    bar_chart = alt.Chart(bar_data).mark_bar(size=bar_width).encode(
        x=alt.X('Category:N', title='', axis=None),  # Hide x-axis
        y=alt.Y('Value:Q', scale=alt.Scale(domain=[0, max_value]), title='', axis=None),  # Hide y-axis
        color=alt.Color('Category:N', scale=alt.Scale(domain=['Completed', 'Remaining'], range=['#e55f42', '#e0e0e0']),
                        legend=None)
    ).properties(
        width=bar_width,
        height=bar_height
    ).configure_view(
        strokeWidth=0  # Remove the border around the plot
    )

    return bar_chart

def speedometer(df, total_cases, steps=1000):

    value = df["Number of curated cases"].sum()
    gradient_colors = generate_gradient_colors("#8c52ff", "#ff5757", steps)

    step_ranges = [(i * total_cases / steps, (i + 1) * total_cases / steps) for i in range(steps)]
    gradient_steps = [{'range': [start, end], 'color': color} for (start, end), color in
                      zip(step_ranges, gradient_colors)]

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=value,
        mode="gauge+number",
        title={'text': "Number of Curated Cases"},
        gauge={
            'axis': {'range': [None, total_cases]},
            'bar': {'color': "#45062E"},
            'steps': gradient_steps
        }
    ))
    fig.update_layout(
        margin=dict(
            autoexpand=False,
            t=0,
            b=0
        )
    )
    return fig

def generate_gradient_colors(start_color, end_color, steps):
    """
    Generates a list of colors forming a gradient between the start and end colors.

    Parameters:
    - start_color (str): The starting color in hex format.
    - end_color (str): The ending color in hex format.
    - steps (int): The number of steps to divide the gradient into.

    Returns:
    - list of str: List of gradient colors in hex format.
    """
    start_color = np.array([int(start_color[i:i+2], 16) for i in range(1, 7, 2)])
    end_color = np.array([int(end_color[i:i+2], 16) for i in range(1, 7, 2)])
    colors = [f"#{''.join(f'{int(c):02x}' for c in start_color + (end_color - start_color) * i / (steps - 1))}" for i in range(steps)]
    return colors


def display_progress_bar(actual_value, expected_total, title="Segmented cases"):
    """
    Displays a progress bar indicating the progress towards the expected total with a custom pink color and bold text.

    Parameters:
    - actual_value (float): The current value achieved.
    - expected_total (float): The total value expected.
    - title (str): The title displayed above the progress bar.
    """
    progress_percentage = actual_value / expected_total   # Calculate the progress percentage

    st.markdown(f"**{title}**")  # Display the title

    # Create a custom HTML for the progress bar with bold text
    progress_html = f"""
    <style>
    .progress-container {{
        width: 100%;
        background-color: #ddd;
        border-radius: 5px;
    }}
    .progress-bar {{
        width: {str(progress_percentage * 250)}%;
        height: 30px;
        background-color: #ff69b4;  /* Pink color */
        text-align: center;
        line-height: 30px;
        color: white;
        font-weight: bold;  /* Make the text bold */
        border-radius: 5px;
    }}
    </style>
    <div class="progress-container">
      <div class="progress-bar">{progress_percentage:.1%}</div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)  # Render the HTML

    # Optionally, display the percentage and actual values below the bar
    st.markdown(f"**{progress_percentage:.1%}** ({actual_value} of {expected_total})")


def horizontal_stacked_bar_chart(df):
    """
    Creates a single horizontal stacked bar chart for the total cases of each site.

    Parameters:
    - df (DataFrame): The DataFrame containing 'Site' and 'Number of expected cases'.
    """
    # Aggregate data by site
    aggregated_df = df.groupby('Site').sum().reset_index()

    fig = go.Figure()

    # Define a color palette for the sites
    colors = px.colors.sequential.Plasma

    # Add a bar trace for each site, all with the same y value to stack horizontally
    for i, row in aggregated_df.iterrows():
        fig.add_trace(go.Bar(
            y=['Total Cases'],  # Single category for all sites
            x=[row['Number of expected cases']],  # Case count for the site
            orientation='h',
            name=row['Site'],
            text=row['Site'],
            showlegend=False,
            hovertemplate='<b>%{text}</b><br>' +
                          'Cases: %{x}<br>' +
                          '<extra></extra>',  # Customize hover text
            marker=dict(
                color=colors[i % len(colors)],  # Assign colors from the palette
                line=dict(width=1, color='#0E1117')  # Border color
            )
        ))

    # Customize layout to fit a dark theme
    fig.update_layout(
        title='Number of Expected Cases by Site',
        xaxis_title='Number of Expected Cases',
        yaxis_title='',
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='white'),
        barmode='stack',  # Enable stacking
        showlegend=True,   # Show legend to differentiate sites
        height=230
    )

    return fig