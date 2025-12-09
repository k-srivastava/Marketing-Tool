import io

import streamlit as st
from PIL import Image, ImageOps
from rembg import remove

from frontend.middleware import styles


# 1. Format the code.
# 2. All strings should be single-quoted except multi-line markdown strings.
# 3. Follow the color scheme from the Assets_Page.py file.


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


st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Hero Image Placement</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(styles.TEXT_CSS, unsafe_allow_html=True)

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
uploaded = st.session_state["hero_image"]
uploaded.seek(0)

product = Image.open(io.BytesIO(remove(uploaded.read())))
st.session_state["raw_hero"] = product
product.thumbnail((80, 80))

results = place_image(product, border_width=1)

st.subheader("Choose Layout")
st.markdown("<hr>", unsafe_allow_html=True)
cols = st.columns(3)

for i in range(1, 10):
    with cols[(i - 1) % 3]:

        st.image(results[i]["image"], caption=f"Layout {i}")

        if st.button(f"Select {i}", key=f"btn_{i}", use_container_width=True):
            st.session_state['product_pos'] = i
            st.session_state["selected"] = results[i]["image"]

if "selected" in st.session_state:
    st.subheader("Selected Layout Preview")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.image(st.session_state["selected"])

_, middle, _ = st.columns([1, 2, 1])
with middle:
    submit_logo = st.button("Choose Logo Placement Next ▶︎", type='primary', use_container_width=True)
    if submit_logo:
        st.switch_page("pages/Logo_Layout.py")
