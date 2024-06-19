import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

import constants
import plots


def main():
    st.set_page_config(
        page_title="LION data overview",
        page_icon="🦁",
        layout="wide")


    alt.themes.enable("dark")


    df = pd.read_csv("/home/kylo-ren/Manuel/LION/dashboard/data/dashboard_excel.csv")

    fdg_subset = df[df.Tracer== 'FDG']
    psma_subset = df[df.Tracer == 'PSMA']

    stacked_bar = plots.horizontal_stacked_bar_chart(df)
    world_map = plots.world_map_plot(df)

    fdg_plot = plots.speedometer(fdg_subset, constants.NUMBER_OF_FDG_CASES)
    psma_plot = plots.speedometer(psma_subset, constants.NUMBER_OF_PSMA_CASES)

    fdg_verified = fdg_subset["Number of verified cases"].sum()
    psma_verified = psma_subset["Number of verified cases"].sum()

    st.plotly_chart(stacked_bar, use_container_width=True)
    st.plotly_chart(world_map, use_container_width=True)


    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        fdg_col, inner_col2, psma_col = st.columns([1, 1, 1])
        with fdg_col:
            st.plotly_chart(fdg_plot)
            plots.display_progress_bar(fdg_verified, constants.NUMBER_OF_FDG_CASES)


        with psma_col:
            st.plotly_chart(psma_plot)
            plots.display_progress_bar(psma_verified, constants.NUMBER_OF_PSMA_CASES)



main()