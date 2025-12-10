import streamlit as st

st.set_page_config(page_title='Creative Studio', layout='wide', initial_sidebar_state='collapsed')

st.markdown("""
            <style>

                h1, h2, h3, h4, h5, p, div, label, span {
                    font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
                }

                /* Main gradient background */
                .hero-section {
                    margin-bottom: 50px;
                    padding: 60px 20px 80px 20px;
                    border-bottom-right-radius: 80px;
                    border-bottom-left-radius: 80px;
                    background: linear-gradient(135deg, #4e09bd, #081f52);
                    box-shadow: 0 10px 30px rgba(20, 33, 61, 0.15);
                }

                .hero-title-top {
                    font-size: 42px;
                    font-weight: 700;
                    margin-bottom: 30px;
                    text-align: center;
                    letter-spacing: 1px;
                    color: #14213D;
                }

                /* Centered Split Animated Title */
                .hero-title-wrapper {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 100%;
                }

                .split-text-container {
                    font-size: 5rem;
                    font-weight: 800;
                    display: flex;
                    overflow: hidden;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    letter-spacing: 2px;
                    text-transform: uppercase;
                    color: #FCA311;
                    text-shadow: 2px 2px 0 #000000;
                }

                .text-part {
                    display: inline-block;
                    animation-duration: 1.2s;
                    animation-timing-function: cubic-bezier(0.25, 0.1, 0.25, 1);
                    opacity: 0;
                    animation-fill-mode: forwards;
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
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes slide-in-right {
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                /* Title styling */
                .hero-title {
                    font-size: 48px;
                    font-weight: 800;
                    text-align: center;
                    color: #14213D;
                }

                .hero-subtitle {
                    font-size: 32px;
                    font-weight: 700;
                    margin-bottom: 15px;
                    color: #FCA311;
                }

                /* Paragraph */
                .hero-text {
                    font-size: 18px;
                    font-style: italic;
                    line-height: 1.6;
                    max-width: 90%;
                    color: #14213D;
                }

                .step-card {
                    display: flex;
                    align-items: center;
                    flex-direction: column;
                    justify-content: center;
                    width: 200px;
                    height: 350px;
                    padding: 30px 20px;
                    transition: transform 0.5s ease-in-out;
                    text-align: center;
                    border: 2px solid #E5E5E5;
                    border-radius: 12px;
                    background-color: #FCA311;
                    box-shadow: 0 10px 30px rgba(20, 33, 61, 0.15);
                }

                .step-card:hover {
                    transform: translateY(-5px);
                    border-color: #14213D;
                    box-shadow: 0 20px 40px rgba(20, 33, 61, 0.25);
                }

                .step-icon {
                    font-size: 40px;
                    color: #14213D;
                }

                .step-title {
                    font-size: 20px;
                    font-weight: 700;
                    margin-bottom: 20px;
                    color: #14213D;
                }

                .step-sub {
                    font-size: 15px;
                    margin: 0;
                    color: #14213D;
                }

                .arrow-container {
                    font-size: 40px;
                    font-weight: bolder;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-top: 125px;
                }

                div.stButton > button {
                    font-size: 28px;
                    font-weight: 800;
                    padding: 15px 30px;
                    transition: all 0.3s ease;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    color: #14213D;
                    border: none;
                    border-radius: 8px;
                    background-color: #FCA311;
                    box-shadow: 0 10px 30px rgba(252, 163, 17, 0.4);
                }

                div.stButton > button:hover {
                    transform: translateY(-2px);
                    color: #000000;
                    background-color: #E5940F;
                    box-shadow: 0 6px 20px rgba(252, 163, 17, 0.5);
                }

                div.stButton > button:focus {
                    border: none;
                    outline: none;
                }
            </style>
            """, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero-section">
        <div class="hero-title-wrapper">
            <div class="split-text-container">
                <div class="text-part left">WORD OF</div>
                <div style="width: 30px;"></div>
                <div class="text-part right">MARKETING</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="hero-title">Create Fast, Save Time</div>', unsafe_allow_html=True)
st.markdown('<div style="height: 40px;"/>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap='large')

with col1:
    st.markdown('<div class="hero-subtitle">From concept to campaign in minutes</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-text">
            Save hours of designing and formatting. Our marketing tool generates ready to use, platform-specific
            creatives in just a few clicks.
        </div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown('<div class="hero-subtitle">Guidelines and Creativity adhered</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-text">
            Generate marketing posters that adhere to both retailer and brand guidelines automatically. Customize freely
            while staying within safe, professional boundaries ensuring your campaigns always look polished.
        </div>""",
        unsafe_allow_html=True
    )

st.divider()

st.markdown('<h2 style="text-align:center; font-weight: 800;">How Our Tool Works</h2>', unsafe_allow_html=True)
st.markdown('<div style="height: 40px;"/>', unsafe_allow_html=True)

steps = [
    {
        'title': 'Input Campaign Details',
        'subtitle': 'Tell us your product and goals. Drop Packshots of Logo and Product',
        'icon': '❖'
    },

    {
        'title': 'Choose Design Preference',
        'subtitle': 'Fonts, Background Colour, Layout ',
        'icon': '❖'
    },

    {
        'title': 'Customize And Refactor',
        'subtitle': 'Review and Reformat according to your liking.',
        'icon': '❖'
    },

    {
        'title': 'Export Your Poster',
        'subtitle': 'Download your platform-ready creatives',
        'icon': '❖'
    }
]

cols = st.columns(7)
for i in range(len(steps)):
    with cols[i * 2]:
        st.markdown(
            f"""<div class="step-card">
    <div class="step-icon">{steps[i]['icon']}</div>
    <div class="step-title">{steps[i]['title']}</div>
    <p class="step-sub">{steps[i]['subtitle']}</p>
</div>""",
            unsafe_allow_html=True,
        )

    if i < len(steps) - 1:
        with cols[i * 2 + 1]:
            st.markdown('<div class="arrow-container">→</div>', unsafe_allow_html=True)

st.divider()

_, mid, _ = st.columns([1, 2, 1])
with mid:
    st.markdown('<div style="height: 20px;"</div>', unsafe_allow_html=True)
    if st.button('Start Designing', use_container_width=True):
        st.switch_page('pages/Assets_Page.py')
