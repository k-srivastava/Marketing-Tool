import io
import os
import sys

import streamlit as st
from PIL import Image, ImageOps
from rembg import remove

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from middleware import styles


def add_border(img, border=1, color="black"):
    return ImageOps.expand(img, border=border, fill=color)


def place_image(product, canvas_size=200, border_width=1):
    pw, ph = product.size

    positions = {
        1: (0, 0),
        2: ((canvas_size - pw) // 2, 0),
        3: (canvas_size - pw, 0),

        4: (0, (canvas_size - ph) // 2),
        5: ((canvas_size - pw) // 2, (canvas_size - ph) // 2),
        6: (canvas_size - pw, (canvas_size - ph) // 2),

        7: (0, canvas_size - ph),
        8: ((canvas_size - pw) // 2, canvas_size - ph),
        9: (canvas_size - pw, canvas_size - ph),
    }

    outputs = {}
    for i, pos in positions.items():
        blank = Image.new("RGBA", (canvas_size, canvas_size), "white")
        blank.paste(product, pos, product)
        bordered = add_border(blank, border=border_width, color="#444")

        outputs[i] = {
            "image": bordered,
            "positions": pos
        }

    return outputs


st.markdown(styles.PAGE_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .stTextArea textarea {
            color: #b9c1e8;
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
            background-color: #bcc4ea;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #FCA311;
        }

        [data-testid="stFileUploader"] small {
            color: #8D99AE;
        }

        .stButton > button {
            background-color: #081f52 !important; /* royal blue */
            color: #ade369 !important;
            border-radius: 3px !important; /* nicer rounded rectangle */
            padding: 10px 22px !important;
            text-transform: uppercase;
            font-weight: 600 !important;
            letter-spacing: 1px;
            transition: 0.2s ease-in-out;
            box-shadow: 0 4px 10px rgba(252, 163, 17, 0.3);
        }

        .stButton > button:hover {
            background-color: #081f52 !important;
            transform: translateY(-4px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        .stImage img {

            /* increase height */
            object-fit: cover;
            border-radius: 3px !important;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        }

        .stImage img:hover {
            transform: scale(1.14); /* enlarge */
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
        }


    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(layout="wide")

if 'product_pos' not in st.session_state:
    st.warning("Please select a product position")
    st.stop()

if 'logo_selected' not in st.session_state:
    st.session_state.logo_selected = None

product_position = st.session_state['product_pos']
st.title("LOGO Placement")

uploaded = st.session_state["logo_image"]
uploaded.seek(0)

logo = Image.open(io.BytesIO(remove(uploaded.read())))
st.session_state['raw_logo'] = logo
logo.thumbnail((80, 80))

results = place_image(logo, border_width=1)

st.subheader("Choose Layout")
cols = st.columns(3)

for i in range(1, 10):
    if i == product_position:
        image = st.session_state["selected"]
        with cols[(i - 1) % 3]:
            st.image(image, caption="(Product Occupied)")
            st.button("Unavailable", disabled=True)

        continue

    with cols[(i - 1) % 3]:
        st.image(results[i]['image'], caption=f"Layout {i}")

        if st.button(f"Select {i}", key=f"btn_{i}"):
            st.session_state['logo_pos'] = i
            st.session_state["logo_selected"] = results[i]['image']

if st.session_state['logo_selected'] is not None:
    st.subheader("Selected Layout Preview")
    st.image(st.session_state["logo_selected"])
    complete_preview = st.button("View Complete Preview Next ▶︎")
    if complete_preview:
        st.switch_page("pages/Additional_Placements.py")
