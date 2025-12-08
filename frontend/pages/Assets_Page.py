import streamlit as st

st.set_page_config(page_title='Asset Manager', initial_sidebar_state='collapsed')

if 'hero_image' not in st.session_state:
    st.session_state['hero_image'] = None

if 'logo_image' not in st.session_state:
    st.session_state['logo_image'] = None

if 'support_images' not in st.session_state:
    st.session_state['support_images'] = []

st.markdown(
    """<h1 style="text-align: center;">Asset Manager</h1>
    <p style='text-align: center; color: #808080;'>Upload your product details and visuals to get started.</p>""",
    unsafe_allow_html=True
)

st.divider()

with st.container():
    st.subheader('Product Details')

    product_description_raw = st.text_area(
        'Product Description',
        height=150,
        placeholder='Your detailed product description goes here...',
        help="Provide as much detail as possible for better results."
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
