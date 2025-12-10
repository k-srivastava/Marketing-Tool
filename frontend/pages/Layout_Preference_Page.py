from typing import Optional

import rembg
import streamlit as st
from PIL import Image
from streamlit.delta_generator import DeltaGenerator

from frontend.middleware import layouts, styles

st.set_page_config(page_title='Layout Preferences', layout='wide', initial_sidebar_state='collapsed')

_num_support_images = len(st.session_state.get('support_images', []))

PAGES = 2 + _num_support_images
OPTIONS_PER_PAGE = 9

if 'layout_idx' not in st.session_state:
    st.session_state['layout_idx'] = 0

if 'choices' not in st.session_state:
    st.session_state['choices'] = [None] * PAGES

if 'layout_finalized' not in st.session_state:
    st.session_state['layout_finalized'] = False

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
            render_option(rembg.remove(st.session_state.get('support_images')[0]))
        else:
            render_option(rembg.remove(st.session_state.get('support_images')[1]))

    with left:
        def go_to_previous_page():
            st.session_state['layout_idx'] -= 1


        if st.session_state['layout_idx'] > 0:
            st.button(
                '<- Back', key='back_btn', help='Previous', on_click=go_to_previous_page, use_container_width=True
            )

    with right:
        def go_to_next_page():
            st.session_state['layout_idx'] += 1


        def finalize():
            st.session_state['layout_finalized'] = True


        if st.session_state['layout_idx'] < PAGES - 1:
            st.button('Next ->', key='next_btn', help='Next', on_click=go_to_next_page, use_container_width=True)
        else:
            st.button('Finish ✔', key='finish_btn', help='Finalize', on_click=finalize, use_container_width=True)
