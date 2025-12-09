import os
import sys

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from middleware import styles

st.set_page_config(page_title='Design Preferences', layout='wide', initial_sidebar_state='collapsed')

if 'page' not in st.session_state:
    st.session_state['page'] = 0

if 'choices' not in st.session_state:
    st.session_state['choices'] = [None, None, None, None]

if 'finalized' not in st.session_state:
    st.session_state['finalized'] = False

PAGES = 4
OPTIONS_PER_PAGE = 4

page_labels = [
    'Design Type: Font',
    'Design Type: Color Palette',
    'Design Type: Image',
    'Design Type: Logo'
]

options_text = [
    ['Helvetica Nueue', 'Times New Roman', 'Arial', 'Comic Sans'],
    ['Blues', 'Red', 'Oranges', 'Grays'],
    ['Hero', 'Logo', 'Support (1)', 'Support (2)'],
    ['Top-Left', 'Top-Right', 'Bottom-Left', 'Bottom-Right']
]

st.markdown(styles.PAGE_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        div.stButton > button {
            font-size: 16px;
            font-weight: 600;
            width: 100%;
            height: 120px;
            transition: all 0.2s ease-in-out;
            color: #14213D;
            border: 2px solid #E5E5E5;
            border-radius: 8px;
            background-color: #E5E5E5;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            color: #14213D;
            border-color: #14213D;
            background-color: #DCDCDC;
        }

        div.stButton > button[kind="primary"] {
            font-weight: 800;
            color: #14213D;
            border: none;
            background: #FCA311;
            box-shadow: 0 4px 10px rgba(252, 163, 17, 0.4);
        }

        div.stButton > button[kind="primary"]:hover {
            color: #000000;
            background: #E5940F;
            box-shadow: 0 6px 15px rgba(252, 163, 17, 0.5);
        }

        div[data-testid="column"] button[kind="primary"] {
        }
    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state['choices'][st.session_state['page']] is not None:
    st.markdown(
        """
        <style>
            div.stButton > button[kind="secondary"] {
                opacity: 0.6;
                color: #8D99AE;
                border-color: #F0F0F0;
                background: #F0F0F0;
            }

            div.stButton > button[kind="secondary"]:hover {
                color: #14213D;
                border-color: #14213D;
                background-color: #E5E5E5;
            }
        </style>""",
        unsafe_allow_html=True
    )

st.markdown(
    """<h1 style="text-align: center;">Design Preference</h1>
    <p style='text-align: center; color: #5D6D7E; font-size: 1.1em;'>Choose your favorite styles from a curated
        list.</p>""",
    unsafe_allow_html=True
)

st.divider()

with st.container():
    left, middle, right = st.columns([1, 8, 1])

    with middle:
        st.markdown(
            f'<h3 style="text-align: center; margin-bottom: 30px;">{page_labels[st.session_state["page"]]}</h3>',
            unsafe_allow_html=True
        )

        top_left, top_right = st.columns(2, gap='large')
        bottom_left, bottom_right = st.columns(2, gap='large')


        def render_option(col: DeltaGenerator, idx: int):
            page = st.session_state['page']
            selected = st.session_state['choices'][page]

            try:
                button_label = options_text[page][idx]
            except IndexError:
                button_label = f'Option {idx + 1}'

            key = f'option_{page}_{idx}'
            button_type = 'primary' if selected == idx else 'secondary'

            with col:
                if st.button(button_label, key=key, type=button_type, use_container_width=True):
                    st.session_state['choices'][page] = idx
                    st.rerun()


        render_option(top_left, 0)
        render_option(top_right, 1)

        render_option(bottom_left, 2)
        render_option(bottom_right, 3)

    with left:
        def go_to_previous_page():
            if st.session_state['page'] > 0:
                st.session_state['page'] -= 1


        if st.session_state['page'] > 0:
            st.markdown('<div style="height: 200px; width: 100%;">', unsafe_allow_html=True)
            st.button(
                '<- Back', key='back_btn', help='Previous', on_click=go_to_previous_page,
                disabled=st.session_state['page'] == 0, use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

    with right:
        def go_to_next_page():
            if st.session_state['page'] < PAGES - 1:
                st.session_state['page'] += 1


        def finalize():
            st.session_state['finalized'] = True


        st.markdown('<div style="height: 200px; width: 100%;">', unsafe_allow_html=True)
        if st.session_state.page < PAGES - 1:
            st.button('Next ->', key='next_btn', help='Next', on_click=go_to_next_page, use_container_width=True)
        else:
            st.button('Finish ✔', key='finish_btn', help='Finalize', on_click=finalize, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    if st.session_state['finalized']:
        st.divider()
        st.markdown('<h3 style="text-align: center;">Your Final Choices</h3>', unsafe_allow_html=True)

        _, middle, _ = st.columns([1, 2, 1])
        with middle:
            st.success('Your preferences have been saved.')

            for i, choice in enumerate(st.session_state['choices']):
                if choice is None:
                    label = 'Not selected'
                else:
                    try:
                        label = options_text[i][choice]
                    except IndexError:
                        label = f'Option {choice + 1}'

                st.markdown(
                    f"""<div style="background-color: #F0F0F0; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 6px solid #FCA311; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
        <span style="color: #14213D; font-size: 0.85em; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px;">{page_labels[i]}</span>
        <br>
        <span style="font-size: 1.2em; font-weight: 700; color: #14213D;">{label}</span>
    </div>""",
                    unsafe_allow_html=True)
