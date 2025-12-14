from io import BytesIO

import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Poster Validation', initial_sidebar_state='collapsed')

if 'poster' not in st.session_state:
    st.switch_page('pages/Asset_Page.py')

st.markdown(
    """
    <style>
        h1, h2, h3, h4, h5, p, div, label, span {
            font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
            color: #14213D;
        }

        h1 {
            font-weight: 800;
            letter-spacing: -1px;
        }

        h3 {
            font-weight: 700;
            display: inline-block;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #FCA311;
        }

        .stTextArea textarea {
            color: #14213D;
            border: 2px solid #E5E5E5;
            border-radius: 8px;
            background-color: #FCFCFC;
        }

        .stTextArea textarea:focus {
            border-color: #FCA311;
            box-shadow: 0 0 0 1px #FCA311;
        }

        div.stButton > button[kind="primary"] {
            font-weight: 800;
            padding: 1rem;
            transition: all 0.2s ease-in-out;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #14213D;
            border: none;
            background-color: #FCA311;
            box-shadow: 0 4px 10px rgba(252, 163, 17, 0.3);
        }

        div.stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            color: #000000;
            background-color: #E5940F;
            box-shadow: 0 6px 15px rgba(252, 163, 17, 0.4);
        }

        div.stButton > button[kind="secondary"] {
            font-weight: 800;
            padding: 1rem;
            transition: all 0.2s ease-in-out;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #14213D;
            border: none;
            background-color: #E5E5E5;
            box-shadow: 0 4px 10px rgba(229, 229, 229, 0.3);
        }

        div.stButton > button[kind="secondary"]:hover {
            transform: translateY(-2px);
            color: #14213D;
            background-color: #DCDCDC;
            box-shadow: 0 6px 15px rgba(229, 229, 229, 0.4);
        }
    </style>""",
    unsafe_allow_html=True
)

st.markdown(
    """<h1 style="text-align: center;">Poster Validation</h1>
    <p style='text-align: center; color: #5D6D7E; font-size: 1.1em;'>Finalize your designs for the poster and generate
        the finished product.</p>""",
    unsafe_allow_html=True
)

st.divider()

with st.container():
    poster_col, comments_col = st.columns([2.5, 1], gap='large')

    with poster_col:
        raw_poster = st.session_state['poster']['preview']['raw_poster_image']
        final_poster = st.session_state['poster']['preview']['final_poster_image']

        st.image(raw_poster)

        st.divider()

        if final_poster is not None:
            st.image(final_poster)

        else:
            st.warning('No poster generated yet.')

    with comments_col:
        st.markdown(
            f'<h3 style="text-align: center; margin-bottom: 30px;">Feedback</h3>',
            unsafe_allow_html=True
        )

        comments_raw = st.text_area(
            'Comments',
            height=200,
            placeholder='Enter comments for modifications, or any other feedback here...',
            help='Provide as much detail as possible for better results.',
            label_visibility='collapsed'
        )

        st.divider()

        information = st.session_state['poster']['client']['information']
        design_choices = st.session_state['poster']['design']['choices']

        raw_poster = st.session_state['poster']['preview']['raw_poster_image']
        final_poster = st.session_state['poster']['preview']['final_poster_image']

        # Build form-data payload (without raw image bytes) for preview
        data_payload = {
            'name': information['name'],
            'tagline': information['tagline'],
            'brand_name': information['brand_name'],
            'font': design_choices['font'],
            'primary_color': design_choices['color_scheme'][0],
            'secondary_color': design_choices['color_scheme'][1],
            'hero_feature': design_choices['hero_feature'],
            'size': design_choices['size'],
            'comments': comments_raw.strip(),
            'use_ai': str(st.session_state['poster']['metadata']['use_ai']).lower()
        }

        left, right = st.columns(2)

        with left:
            if st.button('Generate Poster', type='primary', use_container_width=True):
                image_to_send = final_poster if final_poster is not None else raw_poster
                buf = BytesIO()
                image_to_send.save(buf, format='PNG')
                buf.seek(0)

                files = {
                    'raw_poster': ('poster.png', buf.getvalue(), 'image/png')
                }

                try:
                    response = requests.post(
                        'http://127.0.0.1:8000/generate',
                        data=data_payload,
                        files=files,
                        timeout=40
                    )
                except Exception as e:
                    st.error(f'Failed to reach generation endpoint: {e}')
                else:
                    if response.status_code == 200:
                        try:
                            img = Image.open(BytesIO(response.content))
                            st.session_state['poster']['preview']['final_poster_image'] = img
                            st.success('Poster generated successfully!')
                            st.rerun()
                        except Exception:
                            st.error('Received invalid image from server.')
                    else:
                        st.warning(f'Generation endpoint returned status {response.status_code}.')

        with right:
            st.button(
                'Back to Layout', type='secondary', use_container_width=True,
                on_click=lambda: st.switch_page('pages/Layout_Preference_Page.py')
            )
