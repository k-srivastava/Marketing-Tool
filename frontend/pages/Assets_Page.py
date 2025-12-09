import streamlit as st

from frontend.middleware import styles

st.set_page_config(page_title='Asset Manager', initial_sidebar_state='collapsed')

if 'hero_image' not in st.session_state:
    st.session_state['hero_image'] = None

if 'logo_image' not in st.session_state:
    st.session_state['logo_image'] = None

if 'support_images' not in st.session_state:
    st.session_state['support_images'] = []

st.markdown(styles.TEXT_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <style>
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
    if hero_image_raw is not None:
        st.session_state['hero_image'] = hero_image_raw

with middle:
    st.markdown('##### Brand Logo')
    st.caption('Your brand logo (transparent background is recommended).')

    logo_image_raw = st.file_uploader(
        'Brand Hero', type=['png', 'jpg'], accept_multiple_files=False
    )
    if logo_image_raw is not None:
        st.session_state['logo_image'] = logo_image_raw

with right:
    st.markdown('##### Support Images')
    st.caption('Additional angles or context shots to be optionally included.')
    if "extra_imgs" not in st.session_state:
        st.session_state.extra_imgs = []

    uploaded = st.file_uploader(
        "Upload support images", type=["jpg", "png"], accept_multiple_files=True,
        disabled=len(st.session_state.extra_imgs) >= 2)
    if uploaded:
        for file in uploaded:
            if file.name not in [f.name for f in st.session_state.extra_imgs]:
                if len(st.session_state.extra_imgs) < 2:
                    st.session_state.extra_imgs.append(file)
                else:
                    st.error("You can only upload 2 images max.")

st.divider()

_, middle, _ = st.columns([1, 2, 1])
with middle:
    submit = st.button('Start Generation', type='primary', use_container_width=True)
    if submit:
        st.switch_page("pages/Hero_Layout.py")
