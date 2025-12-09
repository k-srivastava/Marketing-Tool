import io

import streamlit as st
from PIL import Image, ImageOps
from rembg import remove

defaults = {
    "img1_selected": None,
    "img1_pos": None,
    "img2_selected": None,
    "img2_pos": None,
    "extra_imgs": [],
    "product_pos": None,
    "logo_pos": None,
    "selected": None,
    "logo_selected": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


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


# CODE FOR PUTTING IN BLOCKED POSITIONS
product_position = st.session_state['product_pos']
logo_position = st.session_state['logo_pos']
blocked_positions = dict()
blocked_positions[product_position] = st.session_state["selected"]
blocked_positions[logo_position] = st.session_state["logo_selected"]

# IMAGE 1
if len(st.session_state.extra_imgs) >= 1:

    img1 = st.session_state.extra_imgs[0]
    img1.seek(0)

    img1 = Image.open(io.BytesIO(remove(img1.read())))
    st.session_state['raw_img1'] = img1
    img1.thumbnail((80, 80))

    results = place_image(img1, border_width=1)

    st.subheader("Choose Layout for SUPPORT IMAGE1")
    cols = st.columns(3)
    for i in range(1, 10):
        if i in blocked_positions:
            image = blocked_positions[i]
            with cols[(i - 1) % 3]:
                st.image(image, caption="(Product Occupied)")
                st.button("Unavailable for selection", disabled=True, key=f"img1_unavailable_{i}")
            continue

        with cols[(i - 1) % 3]:
            st.image(results[i]['image'], caption=f"Layout {i}")

            if st.button(f"Select {i}", key=f"img1_btn_{i}"):
                st.session_state['img1_pos'] = i
                st.session_state["img1_selected"] = results[i]['image']

    blocked_positions[st.session_state['img1_pos']] = st.session_state["img1_selected"]

# CODE FOR SHOWING SUPPORT IMAGE 1 PREVIEW
if st.session_state['img1_selected'] is not None:
    st.subheader("Selected Layout Preview")
    st.image(st.session_state["img1_selected"])
    if len(st.session_state.extra_imgs) == 2:

        if st.button("go for second support image"):
            st.session_state["open_img2"] = True

    # IMAGE 2
    if st.session_state.get("open_img2", False):

        img2 = st.session_state.extra_imgs[1]
        img2.seek(0)

        img2 = Image.open(io.BytesIO(remove(img2.read())))
        st.session_state['raw_img2'] = img2
        img2.thumbnail((80, 80))

        results = place_image(img2, border_width=1)

        st.subheader("Choose Layout for SUPPORT IMAGE2")
        cols = st.columns(3)

        for i in range(1, 10):

            if i in blocked_positions:
                image = blocked_positions[i]
                with cols[(i - 1) % 3]:
                    st.image(image, caption="(Product Occupied)")
                    st.button("Unavailable for selection", disabled=True, key=f"img2_unavailable_{i}")
                continue

            with cols[(i - 1) % 3]:
                st.image(results[i]['image'], caption=f"Layout {i}")

                if st.button(f"Select {i}", key=f"img2_btn_{i}"):
                    st.session_state['img2_pos'] = i
                    st.session_state["img2_selected"] = results[i]['image']

    # CODE FOR SHOWING SUPPORT IMAGE 2
    if st.session_state["img2_selected"] is not None:
        st.subheader("Selected Layout Preview — Support Image 2")
        st.image(st.session_state["img2_selected"])
