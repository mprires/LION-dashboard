import streamlit as st
import altair as alt
import os

import constants
import download_data
import plots


def main():
    st.set_page_config(
        page_title="LION data overview",
        page_icon="🦁",
        layout="wide")



    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    lion_logo = download_data.fetch_image_from_s3("enhance-pet", "lion/lion_round.png",
                                                   aws_access_key_id, aws_secret_access_key)

    # Display the image using HTML and CSS for styling
    st.markdown(
        f"""
        <style>
        .clickable-image {{
            position: absolute;
            top: -150px;
            left: -100px;
            width: 350px;
            height: 350px;
            overflow: hidden;
            border-radius: 50%;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            align-items: center;
            justify-content: center;
            z-index: 10;
        }}
        .clickable-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        </style>

        <a href="https://github.com/LalithShiyam/LION/tree/main" target="_blank" rel="noopener noreferrer" class="clickable-image">
            <img src='data:image/jpeg;base64,{lion_logo}'>
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 style='text-align: center; color: white; font-size: 2.5em;'>
            🦁 LION Data Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    df = download_data.read_excel_from_s3(bucket_name="enhance-pet", file_key="lion/dashboard_excel.csv",
                                          aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

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

    enhance_logo = download_data.fetch_image_from_s3("enhance-pet", "lion/EANM-ENHANCE-PET-Reveal.jpg",
                                                  aws_access_key_id, aws_secret_access_key)
    st.markdown(
        f"""
        <style>
        .bottom-right-image-container {{
            position: absolute;
            bottom: -200px;
            right: 0px;
            width: 250px;
            height: 250px;
            overflow: hidden;
            border-radius: 0%;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            transition: opacity 0.3s ease;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }}
        .bottom-right-image {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        </style>

        <a id="image-link2" href="https://www.enhance.pet" target="_blank" rel="noopener noreferrer">
            <div class="bottom-right-image-container">
                <img src='data:image/jpeg;base64,{enhance_logo}' class="bottom-right-image">
            </div>
        </a>
        <script>
        var imageLink2 = document.getElementById('image-link2');
        var lastScrollTop = 0;

        window.addEventListener('scroll', function() {{
            var st = window.pageYOffset || document.documentElement.scrollTop;
            if (st > lastScrollTop) {{
                // Downscroll code
                imageLink2.style.opacity = '0';
            }} else {{
                // Upscroll code
                imageLink2.style.opacity = '1';
            }}
            lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
        }}, false);
        </script>
        """,
        unsafe_allow_html=True
    )


main()