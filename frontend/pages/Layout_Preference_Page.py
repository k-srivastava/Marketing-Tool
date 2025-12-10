from typing import Optional

import streamlit as st
from PIL import Image
from streamlit.delta_generator import DeltaGenerator

from frontend.middleware import layouts, styles

st.set_page_config(page_title='Layout Preferences', layout='wide', initial_sidebar_state='collapsed')

_num_support_images = int('support_image_1' in st.session_state) + int('support_image_2' in st.session_state)

PAGES = 2 + _num_support_images
OPTIONS_PER_PAGE = 9

if 'layout_idx' not in st.session_state:
    st.session_state['layout_idx'] = 0

if 'choices' not in st.session_state:
    st.session_state['choices'] = [None] * PAGES

if 'layout_finalized' not in st.session_state:
    st.session_state['layout_finalized'] = False

if 'raw_poster_image' not in st.session_state:
    st.session_state['raw_poster_image'] = None

page_labels = layouts.generate_page_labels(_num_support_images)
options_text = layouts.generate_page_headings(_num_support_images)

st.markdown(styles.TEXT_CSS, unsafe_allow_html=True)

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
            f'<h3 style="text-align: center; margin-bottom: 30px;">{page_labels[st.session_state["layout_idx"]]}</h3>',
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

            option_thumbnails = layouts.create_option_thumbnails(asset_thumbnail)
            for i in range(OPTIONS_PER_PAGE):
                with grid[i]:
                    _, m, _ = st.columns([1, 9, 1])
                    with m:
                        st.image(option_thumbnails[i])

                    if st.button(
                            'Slot Occupied' if i in st.session_state['choices'] else
                            layouts.get_thumbnail_position_name(i),
                            key=f'option_{st.session_state["layout_idx"]}_{i}', type='primary',
                            use_container_width=True, disabled=i in st.session_state['choices']
                    ):
                        st.session_state['choices'][st.session_state['layout_idx']] = i
                        st.rerun()


        page = st.session_state['layout_idx']

        if page == 0:
            render_option(st.session_state.get('hero_image'))
        elif page == 1:
            render_option(st.session_state.get('logo_image'))
        elif page == 2:
            render_option(st.session_state.get('support_image_1'))
        else:
            render_option(st.session_state.get('support_image_2'))

    with left:
        def go_to_previous_page():
            if st.session_state['layout_idx'] > 0:
                st.session_state['layout_idx'] -= 1
                st.info(st.session_state['layout_idx'])


        if st.session_state['layout_idx'] > 0:
            st.button(
                '<- Back', key='back_btn', help='Previous', on_click=go_to_previous_page, use_container_width=True
            )

    with right:
        def go_to_next_page():
            if st.session_state['layout_idx'] < PAGES:
                st.session_state['layout_idx'] += 1


        def finalize():
            st.session_state['layout_finalized'] = True


        if st.session_state['layout_idx'] < PAGES - 1:
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

        positions = layouts.get_relative_positions(asset_copy.size, canvas_size)
        if 0 <= choice_idx < len(positions):
            position = positions[choice_idx]
            canvas.paste(asset_copy, position, asset_copy)


    for idx, choice in enumerate(st.session_state['choices']):
        if choice is None:
            continue

        if idx == 0:
            overlay_asset(st.session_state.get('hero_image'), choice, CANVAS_SIZE)

        elif idx == 1:
            overlay_asset(st.session_state.get('logo_image'), choice, CANVAS_SIZE)

        elif idx == 2:
            overlay_asset(st.session_state.get('support_image_1'), choice, CANVAS_SIZE)

        else:
            overlay_asset(st.session_state.get('support_image_2'), choice, CANVAS_SIZE)

    _, middle, _ = st.columns([1, 2, 1])
    with middle:
        st.image(canvas, caption='Poster Preview', use_container_width=True)

    if st.session_state['layout_finalized']:
        st.divider()
        st.info('Your layout preferences have been saved.')

        st.session_state['raw_poster_image'] = canvas
        if st.button('Finalize & Generate', type='primary', use_container_width=True):
            st.switch_page('pages/Poster_Validation_Page.py')
