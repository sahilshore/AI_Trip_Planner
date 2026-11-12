import streamlit as st
import requests
import datetime

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Wanderly | AI Trip Planner",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

        :root {
            --ink: #1d2925;
            --muted: #6b7771;
            --paper: #fbfaf6;
            --sage: #dce8df;
            --deep-sage: #315947;
            --coral: #e8795f;
            --line: #e5e8e1;
        }

        .stApp {
            background: var(--paper);
            color: var(--ink);
            font-family: 'DM Sans', sans-serif;
        }

        [data-testid='stSidebar'] {
            background: #eef3ed;
            border-right: 1px solid var(--line);
        }

        [data-testid='stSidebar'] .block-container {
            padding: 2rem 1.35rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: .65rem;
            color: var(--deep-sage);
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: .02em;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            background: var(--deep-sage);
            color: #fff;
        }

        .eyebrow {
            color: var(--coral);
            font-size: .73rem;
            font-weight: 700;
            letter-spacing: .16em;
            text-transform: uppercase;
            margin-bottom: .65rem;
        }

        .hero h1 {
            color: var(--ink);
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.4rem, 5vw, 4.8rem);
            line-height: 1.02;
            margin: 0;
            max-width: 760px;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.6;
            margin: 1.15rem 0 2rem;
            max-width: 600px;
        }

        .prompt-box {
            background: var(--sage);
            border: 1px solid #c9dbce;
            border-radius: 14px;
            padding: 1.2rem 1.25rem .4rem;
            margin: 1.25rem 0 2.5rem;
        }

        .prompt-label {
            color: var(--deep-sage);
            font-size: .8rem;
            font-weight: 700;
            letter-spacing: .04em;
            text-transform: uppercase;
        }

        .plan-meta {
            color: var(--muted);
            font-size: .82rem;
            margin-bottom: 1rem;
        }

        .stTextInput input {
            background: #fff;
            border: 1px solid #c9d6cb;
            border-radius: 8px;
            color: var(--ink);
        }

        .stFormSubmitButton button {
            background: var(--coral);
            border: 0;
            border-radius: 8px;
            color: #fff;
            font-weight: 700;
            min-height: 2.6rem;
        }

        .stFormSubmitButton button:hover {
            background: #d7654e;
            color: #fff;
        }

        .stButton button {
            border: 1px solid #cbd9ce;
            border-radius: 8px;
            color: var(--deep-sage);
            font-size: .88rem;
        }

        .section-rule {
            border-top: 1px solid var(--line);
            margin: 1rem 0 2rem;
        }

        .sidebar-caption {
            color: var(--muted);
            font-size: .82rem;
            line-height: 1.5;
            margin: .55rem 0 1.5rem;
        }

        .sidebar-heading,
        .sidebar-note {
            color: #000;
        }

        .sidebar-heading {
            font-size: 1rem;
            font-weight: 700;
            margin: 1.5rem 0 .75rem;
        }

        .sidebar-note {
            font-size: .8rem;
            margin-top: 1rem;
        }

        @media (max-width: 700px) {
            .hero h1 { font-size: 2.7rem; }
            .hero-copy { font-size: .98rem; }
            .prompt-box { padding: 1rem .85rem .25rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "plans" not in st.session_state:
    st.session_state.plans = []

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">✦</span> Wanderly Travel</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sidebar-caption">A thoughtful itinerary, shaped around the way you actually want to travel.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-heading">Start with an idea</div>', unsafe_allow_html=True)
    examples = [
        "A slow 4-day food trip to Jaipur",
        "A budget-friendly Goa escape for 5 days",
        "A weekend nature trip near Bengaluru",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state["trip_brief"] = example

    st.markdown("---")
    st.markdown('<div class="sidebar-note">Your plans stay in this session only.</div>', unsafe_allow_html=True)
    if st.session_state.plans and st.button("Clear plans", use_container_width=True):
        st.session_state.plans = []
        st.rerun()

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">Your next good idea</div>', unsafe_allow_html=True)
st.markdown("<h1>Go somewhere<br>worth remembering.</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="hero-copy">Tell Wanderly where you want to go, how long you have, and what kind of days you want to fill. We will turn the rough idea into a practical plan.</p>',
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

with st.container(border=False):
    st.markdown('<div class="prompt-box">', unsafe_allow_html=True)
    st.markdown('<div class="prompt-label">Build your itinerary</div>', unsafe_allow_html=True)
    with st.form(key="query_form", clear_on_submit=False):
        user_input = st.text_input(
            "Trip brief",
            key="trip_brief",
            label_visibility="collapsed",
            placeholder="e.g. Plan a relaxed 5-day trip to Goa with beaches and local food",
        )
        submit_button = st.form_submit_button("Create my plan  →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button and user_input.strip():
    try:
        with st.spinner("Mapping out the good parts..."):
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": user_input.strip()},
                timeout=120,
            )

        if response.ok:
            answer = response.json().get("answer", "No answer returned.")
            st.session_state.plans.insert(
                0,
                {
                    "question": user_input.strip(),
                    "answer": answer,
                    "created": datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
                },
            )
        else:
            st.error("Wanderly could not finish that plan. Please try again in a moment.")
    except requests.RequestException as error:
        st.error("The planner is temporarily unavailable. Please try again in a moment.")
    except Exception:
        st.error("Something went wrong while creating your plan. Please try again.")

if st.session_state.plans:
    st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
    for plan in st.session_state.plans:
        st.markdown(f"### {plan['question'].title()}")
        st.markdown(
            f'<div class="plan-meta">✦ Created {plan["created"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(plan["answer"])
        st.caption("Check prices, opening hours, weather, and travel requirements before you go.")
        st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)