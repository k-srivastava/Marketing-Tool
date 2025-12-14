from typing import Optional

import streamlit as st
from PIL import Image, ImageOps
from streamlit.delta_generator import DeltaGenerator


def generate_page_labels(num_support_images: int) -> list[str]:
    """
    Generate page labels for the layout preference page based on the number of support images.

    :param num_support_images: Number of support images to include in the layout.
    :type num_support_images: int

    :return: List of page labels.
    :rtype: list[str]
    """
    page_labels = ['Hero Image Placement', 'Product Logo Placement']

    for i in range(num_support_images):
        page_labels.append(f'Support Image ({i + 1}) Placement')

    return page_labels


def generate_page_headings(num_support_images: int) -> list[str]:
    """
    Generate headings for the layout preference page based on the number of support images.

    :param num_support_images: Number of support images to include in the layout.
    :type num_support_images: int

    :return: List of page headings.
    :rtype: list[str]
    """
    page_headings = ['Hero Layout', 'Logo Layout']

    for i in range(num_support_images):
        page_headings.append(f'Support Image ({i + 1}) Layout')

    return page_headings


def create_option_thumbnails(
        asset: Image.Image, canvas_size: int = 200, canvas_color: str = '#E5E5E5', border_color: str = '#14213D'
) -> list[Image.Image]:
    """
    Generates a list of thumbnails for an image asset, each positioned differently on a canvas of specified size and
    color, with an optional border around each canvas. The nine thumbnails represent all possible alignments of the
    asset on the canvas: top-left, top-center, top-right, center-left, center, center-right, bottom-left,
    bottom-center, and bottom-right.

    :param asset: Image asset to be used for creating thumbnails.
    :type asset: Image.Image
    :param canvas_size: Size of the square canvas in pixels.
    :type canvas_size: int
    :param canvas_color: Background color of the canvas in a web-compatible color format.
    :type canvas_color: str
    :param border_color: Color of the border being added around each canvas in a web-compatible color format.
    :type border_color: str

    :return: List of thumbnail images containing the asset positioned on a canvas with the specified size and colors.
    :rtype: list[Image.Image]
    """
    positions = get_relative_positions(asset.size, canvas_size)

    thumbnails: list[Image.Image] = []
    for position in positions:
        canvas = Image.new('RGBA', (canvas_size, canvas_size), canvas_color)
        canvas.paste(asset, position, asset)
        bordered_canvas = ImageOps.expand(canvas, border=1, fill=border_color)
        thumbnails.append(bordered_canvas)

    return thumbnails


def get_relative_positions(asset_size: tuple[int, int], canvas_size: int) -> list[tuple[int, int]]:
    """
    Get the relative positions of the asset on a canvas.

    :param asset_size: Size of the asset in pixels.
    :type asset_size: tuple[int, int]
    :param canvas_size: Size of the canvas in pixels.
    :type canvas_size: int

    :return: Positions of the asset on the canvas.
    :rtype: tuple[int, int]
    """
    asset_width, asset_height = asset_size

    return [
        (0, 0),
        ((canvas_size - asset_width) // 2, 0),
        (canvas_size - asset_width, 0),

        (0, (canvas_size - asset_height) // 2),
        ((canvas_size - asset_width) // 2, (canvas_size - asset_height) // 2),
        (canvas_size - asset_width, (canvas_size - asset_height) // 2),

        (0, canvas_size - asset_height),
        ((canvas_size - asset_width) // 2, canvas_size - asset_height),
        (canvas_size - asset_width, canvas_size - asset_height)
    ]


def get_thumbnail_position_name(idx: int) -> str:
    """
    Get the corresponding position name for a thumbnail index.

    :param idx: Thumbnail index.
    :type idx: int

    :return: Position name.
    :rtype: str
    """
    if idx == 0:
        return 'Top Left'
    elif idx == 1:
        return 'Top Center'
    elif idx == 2:
        return 'Top Right'
    elif idx == 3:
        return 'Middle Left'
    elif idx == 4:
        return 'Middle Center'
    elif idx == 5:
        return 'Middle Right'
    elif idx == 6:
        return 'Bottom Left'
    elif idx == 7:
        return 'Bottom Center'
    else:
        return 'Bottom Right'


st.set_page_config(page_title='Layout Preferences', layout='wide', initial_sidebar_state='collapsed')

if 'poster' not in st.session_state:
    st.switch_page('pages/Assets_Page.py')

NUM_SUPPORT_IMAGES = sum(1 for image in st.session_state['poster']['assets']['support_images'] if image is not None)

PAGES = 2 + NUM_SUPPORT_IMAGES
OPTIONS_PER_PAGE = 9

# Ensure choices list size matches PAGES
if not st.session_state['poster']['layout']['choices'] or len(st.session_state['poster']['layout']['choices']) != PAGES:
    st.session_state['poster']['layout']['choices'] = [None] * PAGES

page_labels = generate_page_labels(NUM_SUPPORT_IMAGES)
options_text = generate_page_headings(NUM_SUPPORT_IMAGES)

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
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown(
        """<h1 style="text-align: center;">Layout Preference</h1>
        <p style='text-align: center; color: #5D6D7E; font-size: 1.1em;'>Choose your favorite layouts from a 3x3
            matrix.</p>""",
        unsafe_allow_html=True
    )

    st.divider()

with st.container():
    left, middle, right = st.columns([1, 8, 1])

    with middle:
        st.markdown(
            f'<h3 style="text-align: center; margin-bottom: 30px;">{page_labels[st.session_state["poster"]["layout"]["page"]]}</h3>',
            unsafe_allow_html=True
        )

        grid: list[DeltaGenerator] = [
            *st.columns(OPTIONS_PER_PAGE // 3, gap='large', vertical_alignment='center'),
            *st.columns(OPTIONS_PER_PAGE // 3, gap='large', vertical_alignment='center'),
            *st.columns(OPTIONS_PER_PAGE // 3, gap='large', vertical_alignment='center')
        ]


        def render_option(asset: Optional[Image.Image]):
            if asset is None:
                st.warning('Asset not uploaded.')
                return

            asset_thumbnail = asset.copy()
            asset_thumbnail.thumbnail((100, 100))

            option_thumbnails = create_option_thumbnails(asset_thumbnail)
            for i in range(OPTIONS_PER_PAGE):
                with grid[i]:
                    _, m, _ = st.columns([1, 9, 1])
                    with m:
                        st.image(option_thumbnails[i])

                    if st.button(
                            'Slot Occupied' if i in st.session_state['poster']['layout']['choices'] else
                            get_thumbnail_position_name(i),
                            key=f'option_{st.session_state["poster"]["layout"]["page"]}_{i}', type='primary',
                            use_container_width=True, disabled=i in st.session_state['poster']['layout']['choices']
                    ):
                        st.session_state['poster']['layout']['choices'][
                            st.session_state['poster']['layout']['page']] = i
                        st.rerun()


        page = st.session_state['poster']['layout']['page']

        if page == 0:
            render_option(st.session_state['poster']['assets']['hero_image'])
        elif page == 1:
            render_option(st.session_state['poster']['assets']['logo_image'])
        elif page == 2:
            render_option(st.session_state['poster']['assets']['support_images'][0])
        else:
            render_option(st.session_state['poster']['assets']['support_images'][1])

    with left:
        def go_to_previous_page():
            if st.session_state['poster']['layout']['page'] > 0:
                st.session_state['poster']['layout']['page'] -= 1


        if st.session_state['poster']['layout']['page'] > 0:
            st.button(
                '<- Back', key='back_btn', help='Previous', on_click=go_to_previous_page, use_container_width=True
            )

    with right:
        def go_to_next_page():
            if st.session_state['poster']['layout']['page'] < PAGES - 1:
                st.session_state['poster']['layout']['page'] += 1


        def finalize():
            st.session_state['poster']['layout']['finalized'] = True


        if st.session_state['poster']['layout']['page'] < PAGES - 1:
            st.button('Next ->', key='next_btn', help='Next', on_click=go_to_next_page, use_container_width=True)
        else:
            st.button('Finish ✔', key='finish_btn', help='Finalize', on_click=finalize, use_container_width=True)

with st.container():
    st.divider()

    st.subheader('Current Poster Preview')

    CANVAS_SIZE = 500
    canvas = Image.new('RGBA', (CANVAS_SIZE, CANVAS_SIZE), '#E5E5E5')


    def overlay_asset(asset: Image.Image, choice_idx: int, canvas_size: int):
        if asset is None or choice_idx is None:
            return

        asset_copy = asset.copy()
        asset_copy.thumbnail((canvas_size // 2, canvas_size // 2))

        positions = get_relative_positions(asset_copy.size, canvas_size)
        if 0 <= choice_idx < len(positions):
            position = positions[choice_idx]
            canvas.paste(asset_copy, position, asset_copy)


    for idx, choice in enumerate(st.session_state['poster']['layout']['choices']):
        if choice is None:
            continue

        if idx == 0:
            overlay_asset(st.session_state['poster']['assets']['hero_image'], choice, CANVAS_SIZE)

        elif idx == 1:
            overlay_asset(st.session_state['poster']['assets']['logo_image'], choice, CANVAS_SIZE)

        elif idx == 2:
            overlay_asset(st.session_state['poster']['assets']['support_images'][0], choice, CANVAS_SIZE)

        else:
            overlay_asset(st.session_state['poster']['assets']['support_images'][1], choice, CANVAS_SIZE)

    _, middle, _ = st.columns([1, 2, 1])
    with middle:
        st.image(canvas, caption='Poster Preview', use_container_width=True)

    if st.session_state['poster']['layout']['finalized']:
        st.divider()
        st.info('Your layout preferences have been saved.')

        st.session_state['poster']['preview']['raw_poster_image'] = canvas
        if st.button('Finalize & Generate', type='primary', use_container_width=True):
            st.switch_page('pages/Poster_Validation_Page.py')
