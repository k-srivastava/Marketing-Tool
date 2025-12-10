import streamlit as st

st.set_page_config(page_title="Creative Studio", layout="wide")

st.markdown("""
            <style>

                body, html, [class*="css"] {
                    font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
                }

                /* Main gradient background */
                .hero-section {
                    background: linear-gradient(135deg, #4e09bd, #081f52);
                    border-bottom-left-radius: 150px;
                    border-bottom-right-radius: 150px;
                    padding: 80px 40px;
                }

                .hero-title-top {
                    font-size: 42px;
                    font-weight: 700;
                    color: #041942;
                    margin-bottom: 30px;
                    letter-spacing: 1px;
                    text-align: center;
                    text
                }

                /* Centered Split Animated Title */
                .hero-title-wrapper {
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    margin-top: 40px;
                }

                .split-text-container {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 4rem;
                    text-shadow: .1em .1em 0 hsl(39, 94%, 6%);
                    font-family: 'Helvetica',serif;
                    font-weight: 700;
                    text-transform: uppercase;
                    color: #f1a604; 
                    overflow: hidden;
                    letter-spacing: 3px;
                    text-align: center;
                }

                .text-part {
                    display: inline-block;
                    position: relative;
                    animation-duration: 1.8s;
                    animation-timing-function: ease-out;
                    animation-fill-mode: forwards;
                    opacity: 0;
                }

                .text-part.left {
                    transform: translateX(-200%);
                    animation-name: slide-in-left;
                }

                .text-part.right {
                    transform: translateX(200%);
                    animation-name: slide-in-right;
                }

                @keyframes slide-in-left {
                    0% {
                        transform: translateX(-200%);
                        opacity: 0;
                    }
                    100% {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes slide-in-right {
                    0% {
                        transform: translateX(200%);
                        opacity: 0;
                    }
                    100% {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                /* Title styling */
                
                
                .hero-title {
                    font-size: 65px;
                    font-weight: 800;
                    color: #111;
                }

                .hero-subtitle {
                    font-size: 40px;
                    color: #777;
                    margin-top: -20px;
                }

                /* Paragraph */
                .hero-text {
                    font-size: 18px;
                    color: #444;
                    line-height: 1.6;
                    max-width: 500px;
                }


            </style>
            """, unsafe_allow_html=True)

st.markdown("""
<div class='hero-section'>
    <div class="hero-title-wrapper">
        <div class="split-text-container">
            <div class="text-part left">WORD OF </div>
            <div style="width: 28px;"></div>
            <div class="text-part right">MARKETING</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='content-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='hero-title'>Create Fast, Save Time</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>From concept to campaign in minutes</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='hero-text'>
        Save hours of designing and formatting. Our marketing tool generates ready to use, platform-specific creatives in just a few clicks.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='hero-title'>Create Fast, Save Time</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Guidelines and Creativity adhered</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='hero-text'>
            Generate marketing posters that adhere to both retailer and brand guidelines automatically. Customize freely while staying within safe, professional boundaries ensuring your campaigns always look polished.
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>How Our Tool Works</h2>", unsafe_allow_html=True)

card_css = """
           <style>
               .step-card {
                   background-color: #f5af28;
                   padding: 20px;
                   border-radius: 15px;
                   text-align: center;
                   box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);


                   height: 350px;
                   display: flex;
                   flex-direction: column;
                   justify-content: center; /* vertical center */
                   align-items: center; /* horizontal center */
               }

               .step-title {
                   margin: 10px 0 5px 0;
                   font-size: 18px;
                   font-weight: 600;
               }

               .step-sub {
                   margin: 0;
                   font-size: 14px;
                   color: #555;
               }
           </style> \
           """
st.markdown(card_css, unsafe_allow_html=True)

steps = [
    {"title": "Input Campaign Details",
     "subtitle": "Tell us your product and goals. Drop Packshots of Logo and Product", "icon": "❖"},
    {"title": "Choose Design Preference", "subtitle": "Fonts, Background Colour, Layout ", "icon": "❖"},
    {"title": "Customize And Refactor", "subtitle": "Review and Reformat according to your liking.", "icon": "❖"},
    {"title": "Export Your Poster", "subtitle": "Download your platform-ready creatives", "icon": "❖"}
]

arrow_img_path = "icons/arrow-right-solid-full.svg"

cols = st.columns(7)
for i in range(len(steps)):

    with cols[i * 2]:
        st.markdown(
            f"""
               <div class="step-card">
                   <div style="width:60px; margin-bottom:12px;">{steps[i]['icon']}</div>
                   <div class="step-title">{steps[i]['title']}</div>
                   <p class="step-sub">{steps[i]['subtitle']}</p>
               </div>
               """,
            unsafe_allow_html=True,
        )

    if i < len(steps) - 1:
        with cols[i * 2 + 1]:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.image(arrow_img_path, width=90)

st.divider()
_, mid, _ = st.columns([1, 2, 1])
with mid:
    if st.button("Start Designing", use_container_width=True):
        st.switch_page("pages/Assets_Page.py")
