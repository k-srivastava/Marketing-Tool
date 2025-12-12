import streamlit as st

st.set_page_config(page_title='Poster Validation', initial_sidebar_state='collapsed')

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
        raw_poster = st.session_state.get('raw_poster_image')

        if raw_poster is not None:
            st.image(raw_poster)
        else:
            st.info('No poster generated yet.')

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

        left, right = st.columns(2)

        with left:
            st.button('Accept Changes', type='primary', use_container_width=True)

        with right:
            st.button('Reject Changes', type='secondary', use_container_width=True)
