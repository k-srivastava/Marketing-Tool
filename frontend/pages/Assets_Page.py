from io import BytesIO

import rembg
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Asset Manager', initial_sidebar_state='collapsed')

if 'product_description' not in st.session_state:
    st.session_state['product_description'] = None

if 'hero_image' not in st.session_state:
    st.session_state['hero_image'] = None

if 'logo_image' not in st.session_state:
    st.session_state['logo_image'] = None

if 'support_image_1' not in st.session_state:
    st.session_state['support_image_1'] = None

if 'support_image_2' not in st.session_state:
    st.session_state['support_image_2'] = None

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

        .stTextArea {
            padding-top: 10px;
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

        [data-testid="stFileUploader"] {
            padding: 15px;
            transition: border-color 0.3s;
            border: 1px dashed #E5E5E5;
            border-radius: 8px;
            background-color: #F9F9F9;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #FCA311;
        }

        [data-testid="stFileUploader"] small {
            color: #8D99AE;
        }

        [data-testid="stMarkdownContainer"] hr {
            border: 1px solid #14213D55;
        }

        div.stButton > button[kind="primary"] {
            font-weight: 800;
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

        [data-testid="stCaptionContainer"] {
            font-size: 0.9em;
            color: #5D6D7E !important;
        }
    </style>""",
    unsafe_allow_html=True
)

st.markdown(
    """<h1 style="text-align: center;">Asset Manager</h1>
    <p style='text-align: center; color: #5D6D7E; font-size: 1.1em;'>Upload your product details and visuals to get
        started.</p>""",
    unsafe_allow_html=True
)

st.divider()

with st.container():
    st.subheader('Product Details')

    product_description_raw = st.text_area(
        'Product Description',
        height=150,
        placeholder='Your detailed product description goes here...',
        help="Provide as much detail as possible for better results.",
        label_visibility='collapsed'
    )

    st.session_state['product_description'] = product_description_raw.strip()

st.divider()

st.subheader('Product Assets')
left, middle, right = st.columns(3, gap='large', vertical_alignment='top')

with left:
    st.markdown('##### Hero Image')
    st.caption('Main representation of your product as the hero image in the final poster.')

    hero_image_raw = st.file_uploader('Product Hero Image', type=['png', 'jpg'], label_visibility='collapsed')
    if hero_image_raw is not None:
        hero_image_raw.seek(0)
        hero_image = Image.open(BytesIO(rembg.remove(hero_image_raw.read())))

        st.session_state['hero_image'] = hero_image
        st.image(hero_image, caption='Hero Image Preview')

with middle:
    st.markdown('##### Brand Logo')
    st.caption('Your brand logo (transparent background is recommended).')

    logo_image_raw = st.file_uploader('Brand Hero', type=['png', 'jpg'], label_visibility='collapsed')
    if logo_image_raw is not None:
        logo_image_raw.seek(0)
        logo_image = Image.open(BytesIO(rembg.remove(logo_image_raw.read())))

        st.session_state['logo_image'] = logo_image
        st.image(logo_image, caption='Logo Image Preview')

with right:
    st.markdown('##### Support Images')
    st.caption('Additional angles or context shots to be optionally included.')

    uploaded = st.file_uploader(
        'Support Images', type=['png', 'jpg'], accept_multiple_files=True, label_visibility='collapsed',
        disabled=st.session_state['support_image_1'] is not None and st.session_state['support_image_2'] is not None
    )

    if uploaded:
        for file in uploaded:
            file.seek(0)

            if st.session_state['support_image_1'] is None:
                support_image_1 = Image.open(BytesIO(rembg.remove(file.read())))
                st.session_state['support_image_1'] = support_image_1
                st.image(support_image_1, caption='Support Image Preview (1)')

            elif st.session_state['support_image_2'] is None:
                support_image_2 = Image.open(BytesIO(rembg.remove(file.read())))
                st.session_state['support_image_2'] = support_image_2
                st.image(support_image_2, caption='Support Image Preview (2)')

st.divider()

_, middle, _ = st.columns([1, 2, 1])
with middle:
    submit = st.button('Start Generation', type='primary', use_container_width=True)
    if submit:
        st.switch_page('pages/Design_Preference_Page.py')
