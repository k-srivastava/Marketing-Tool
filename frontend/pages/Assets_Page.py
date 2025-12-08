import streamlit as st

st.set_page_config(page_title='Asset Manager', initial_sidebar_state='collapsed')

if 'hero_image' not in st.session_state:
    st.session_state['hero_image'] = None

if 'logo_image' not in st.session_state:
    st.session_state['logo_image'] = None

if 'support_images' not in st.session_state:
    st.session_state['support_images'] = []

st.markdown(
    """
    <style>
        .stApp {
            background-color: #FFFFFF;
        }

        h1, h2, h3, h4, h5, p, div, label, span {
            font-family: 'Helvetica Nueue', Arial, Helvetica, sans-serif;
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

st.divider()

st.subheader('Product Assets')
left, middle, right = st.columns(3, gap='large', vertical_alignment='top')

with left:
    st.markdown('##### Hero Image')
    st.caption('Main representation of your product as the hero image in the final poster.')

    hero_image_raw = st.file_uploader(
        'Product Hero Image', type=['png', 'jpg'], accept_multiple_files=False, label_visibility='collapsed'
    )

    st.session_state['hero_image'] = hero_image_raw

with middle:
    st.markdown('##### Brand Logo')
    st.caption('Your brand logo (transparent background is recommended).')

    logo_image_raw = st.file_uploader(
        'Brand Hero', type=['png', 'jpg'], accept_multiple_files=False, label_visibility='collapsed'
    )

    st.session_state['logo_image'] = logo_image_raw

with right:
    st.markdown('##### Support Images')
    st.caption('Additional angles or context shots to be optionally included.')

    support_images_raw = st.file_uploader('Support Images', type=['png', 'jpg'], label_visibility='collapsed')

    st.session_state['support_images'] = support_images_raw

st.divider()

_, middle, _ = st.columns([1, 2, 1])
with middle:
    st.button('Start Generation', type='primary', use_container_width=True)
