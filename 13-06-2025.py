import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html
from typing import List, Dict, Optional

# ========== CONSTANTS ==========
STRESS_QUESTIONS = [
    "🧠 1. In the last 1-4 weeks, I found it hard to wind down.",
    "⚡ 2. In the last 1-4 weeks, I tended to over-react to situations.",
    "🌀 3. In the last 1-4 weeks, I felt restless.",
    "🔥 4. In the last 1-4 weeks, I felt easily agitated.",
    "🌪️ 5. In the last 1-4 weeks, I felt difficult to relax."
]

PERFORMANCE_QUESTIONS = [
    "📉 6. During the past 1-4 weeks, how often was your performance lower than most workers?",
    "⏸️ 7. During the past 1-4 weeks, how often did you do no work when you should?",
    "⚠️ 8. During the past 1-4 weeks, how often did you not work carefully?",
    "🔍 9. During the past 1-4 weeks, how often was your work quality low?",
    "🧩 10. During the past 1-4 weeks, how often did you not fully concentrate?",
    "🏥 11. During the past 1-4 weeks, how often did health problems limit your work?"
]

OPTIONS = ["🌟 Very Rare", "✨ Rare", "💫 Moderate", "⚡ Frequent", "🔥 Very Frequent"]
OPTION_SCORES = {
    "🌟 Very Rare": 1, 
    "✨ Rare": 2, 
    "💫 Moderate": 3, 
    "⚡ Frequent": 4, 
    "🔥 Very Frequent": 5
}

def setup_page():
    """Configure premium page settings"""
    st.set_page_config(
        page_title="STRESFORMANCE   TRACKER",
        page_icon="🧠💼",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <script>
    function fireConfetti() {{
        confetti({{
            particleCount: 200,
            spread: 90,
            origin: {{ y: 0.6 }},
            colors: ['#8A2BE2', '#00CED1', '#FFD700', '#FF6347'],
            shapes: ['circle', 'square', 'star']
        }});
    }}
    </script>
    <style>
    :root {{
        --primary: #8A2BE2;
        --secondary: #00CED1;
        --accent: #FFD700;
        --text: #000000;
        --bg: #0A0A1A;
    }}
    </style>
    """, height=0)
    st.markdown(f"""
    <style>
    body, .stApp {{
        font-family: 'Poppins', sans-serif;
        background: var(--bg);
        color: var(--text);
        background-image: radial-gradient(circle at 10% 20%, rgba(138, 43, 226, 0.1) 0%, rgba(0, 206, 209, 0.05) 90%);
    }}
    .custom-title{{
    font-size: 1.1rem;
    white-space:nowrap;
    overflow: hidden;
    text-overflow:ellipsis;
    width:100%;
    display:block;
    text-align:center;
    line-height:1.2;
    margin-bottom:0.3rem;
    }}
    h2 {{
        color: var(--secondary);
        font-weight: 600;
        font-size: 1.8rem;
        text-shadow: 0 0 8px rgba(0, 206, 209, 0.5);
        margin-top: 1.8rem;
        border-bottom: 2px solid var(--accent);
        padding-bottom: 0.5rem;
    }}
    .stRadio > div {{
        flex-direction: row;
        gap: 1.5rem;
    }}
    .stRadio > label {{
        font-size: 1.1rem;
        color: var(--text) !important;
    }}
    .stButton button {{
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: black;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
    }}
    .stMarkdown p {{
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--text) !important;
    }}
    .stMetric {{
        background: rgba(10, 10, 30, 0.7);
        border-radius: 16px;
        padding: 1rem;
        border-left: 4px solid var(--accent);
    }}
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def trigger_confetti():
    html("<script>fireConfetti();</script>", height=0)

def calculate_mean(scores: List[int]) -> float:
    return sum(scores) / len(scores) if scores else 0

def classify_stress_level(mean: float) -> str:
    if mean < 1.5: return "Very Low"
    elif mean < 2.5: return "Low"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "High"
    return "Very High"

def classify_performance_level(mean: float) -> str:
    if mean < 1.5: return "Very High"
    elif mean < 2.5: return "High"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "Low"
    return "Very Low"

def plot_dynamic_gauge(value: float, title: str, is_stress: bool):
    bar_color = "#8A2BE2" if is_stress else "#FFD700"
    steps = [
        {'range': [1, 2], 'color': '#A3E4D7' if is_stress else '#F5B7B1'},
        {'range': [2, 3], 'color': '#FAD7A0' if is_stress else '#FAD7A0'},
        {'range': [3, 4], 'color': '#F5B7B1' if is_stress else '#A3E4D7'},
        {'range': [4, 5], 'color': '#8B0000' if is_stress else '#27AE60'}
    ]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': 'black', 'family': "Poppins"}},
        gauge={
            'axis': {'range': [1, 5], 'tickvals': [1, 2, 3, 4, 5], 'tickcolor': 'black', 'tickfont': {'color': 'black', 'size': 12}},
            'bar': {'color': bar_color},
            'bgcolor': 'rgba(255,255,255,0.8)',
            'borderwidth': 1,
            'bordercolor': "gray",
            'steps': steps,
            'threshold': {'line': {'color': bar_color, 'width': 4}, 'thickness': 0.75, 'value': value}
        }
    ))
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(255,255,255,0.9)', font={'family': "Poppins", 'color': "black"})
    st.plotly_chart(fig, use_container_width=True)

def show_header():
    st.markdown("""
    <style>
    @keyframes pulseGlow {
        0% {
            text-shadow:
                0 0 5px #00d0ff,
                0 0 10px #00d0ff,
                0 0 20px #00d0ff,
                0 0 30px #00d0ff;
        }
        50% {
            text-shadow:
                0 0 2px #00aaff,
                0 0 4px #00aaff,
                0 0 8px #00aaff,
                0 0 12px #00aaff;
        }
        100% {
            text-shadow:
                0 0 5px #00d0ff,
                0 0 10px #00d0ff,
                0 0 20px #00d0ff,
                0 0 30px #00d0ff;
        }
    }

    .custom-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        text-align: center;
        animation: pulseGlow 3s infinite ease-in-out;
        margin-bottom: 4rem;
    }
    </style>

    <div class="custom-title">STRESFORMANCE <br> TRACKER</div>
""", unsafe_allow_html=True)

def stress_assessment():
    show_header()
    st.markdown("""
    <h2 style="display: flex; align-items: center; gap: 0.5rem;">
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_gn0tojcq.json" 
            background="transparent" 
            speed="1" 
            style="width: 40px; height: 40px;"
            autoplay>
        </lottie-player>
        Your Stress Measure
    </h2>
    <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
        Rate how often you've experienced these feelings in the past month:
    </p>
    """, unsafe_allow_html=True)
    for i, question in enumerate(STRESS_QUESTIONS):
        st.session_state.stress_answers[i] = st.radio(
            question, 
            OPTIONS,
            key=f"stress_{i}",
            index=None,
            help="Select how frequently you've experienced this feeling"
        )
    if st.button("🚀 Continue to Performance Assessment", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("⚠️ Please answer all questions to proceed")
        else:
            st.session_state.page = 2
            st.rerun()

def performance_assessment():
    show_header()
    st.markdown("""
    <h2 style="display: flex; align-items: center; gap: 0.5rem;">
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_1a8dx7tj.json" 
            background="transparent" 
            speed="1" 
            style="width: 40px; height: 40px;"
            autoplay>
        </lottie-player>
        Your Performance Measure
    </h2>
    <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
        Rate how often these performance issues occurred in the past month:
    </p>
    """, unsafe_allow_html=True)
    for i, question in enumerate(PERFORMANCE_QUESTIONS):
        st.session_state.perf_answers[i] = st.radio(
            question,
            OPTIONS,
            key=f"perf_{i}",
            index=None,
            help="Select how frequently this performance issue occurred"
        )
    col1, col2 = st.columns([1, 2])
    col1.button("🔙 Back", on_click=lambda: st.session_state.update(page=1))
    if col2.button("📊 View My Results", type="primary"):
        if None in st.session_state.perf_answers:
            st.warning("⚠️ Please answer all questions to see your results")
        else:
            st.session_state.page = 3
            st.rerun()

# ---- 18-category pairing logic ----
def get_pairing_recommendation(stress_level, perf_level):
    # Map (stress_level, perf_level) to recommendation and employer action
    pairs = {
        ("Very Low", "Very Low"): ("NEEDS TRAINING", "EMPLOYER ACTION"),
        ("Very Low", "Low"): ("NEEDS TRAINING", "EMPLOYER ACTION"),
        ("Very Low", "Moderate"): ("NEEDS TRAINING", "EMPLOYER ACTION"),
        ("Very Low", "High"): ("GOOD", ""),
        ("Very Low", "Very High"): ("EXCELLENT", ""),
        ("Low", "Very Low"): ("NEEDS TRAINING", "EMPLOYER ACTION"),
        ("Low", "Low"): ("NEEDS TRAINING", "EMPLOYER ACTION"),
        ("Low", "Moderate"): ("NEEDS TRAINING", "EMPLOYER ACTION"),
        ("Low", "High"): ("GOOD", ""),
        ("Low", "Very High"): ("EXCELLENT", ""),
        ("Moderate", "Very Low"): ("NEEDS MONITORING AND TRAINING", "EMPLOYER ACTION"),
        ("Moderate", "Low"): ("NEEDS MONITORING AND TRAINING", "EMPLOYER ACTION"),
        ("Moderate", "Moderate"): ("NEEDS MONITORING AND TRAINING", "EMPLOYER ACTION"),
        ("High", "Very High"): ("EXCELLENT BUT NEEDS COUNSELING", ""),
        ("Very High", "Very Low"): ("NEEDS COUNSELING AND TRAINING", "EMPLOYER ACTION"),
        ("Very High", "Low"): ("NEEDS COUNSELING AND TRAINING", "EMPLOYER ACTION"),
        ("Very High", "Moderate"): ("NEEDS COUNSELING AND TRAINING", "EMPLOYER ACTION"),
        ("Very High", "High"): ("GOOD BUT NEEDS COUNSELING", "")
    }
    return pairs.get((stress_level, perf_level), ("-", ""))

def show_results():
    # Calculate mean scores
    stress_scores = [OPTION_SCORES[ans] for ans in st.session_state.stress_answers]
    stress_mean = calculate_mean(stress_scores)
    stress_level = classify_stress_level(stress_mean).split(" - ")[0].strip().title()

    perf_scores = [OPTION_SCORES[ans] for ans in st.session_state.perf_answers]
    perf_mean = calculate_mean(perf_scores)
    perf_level = classify_performance_level(perf_mean).split(" - ")[0].strip().title()

    # Pairing map for employer actions
    pairing_map = {
        ("Very Low", "Very Low"): "Mental Health is excellent, but performance needs training",
        ("Very Low", "Low"): "Mental Health is excellent, but performance needs training",
        ("Very Low", "Moderate"): "Mental Health is excellent, but performance needs monitoring",
        ("Very Low", "High"): "Mental Health is excellent, and performance is good",
        ("Very Low", "Very High"): "Mental Health is excellent, and performance is excellent",
        ("Low", "Very Low"): "Mental Health is good, but performance needs training",
        ("Low", "Low"): "Mental Health is good, but performance needs training",
        ("Low", "Moderate"): "Mental Health is good, but performance needs monitoring",
        ("Low", "High"): "Mental health and performance are good",
        ("Low", "Very High"): "Mental health is good and performance is excellent",
        ("Moderate", "Very Low"): "Mental health needs monitoring, and performance needs training",
        ("Moderate", "Low"): "Mental health needs monitoring, and performance needs training",
        ("Moderate", "Moderate"): "Mental health and performance need monitoring",
        ("Moderate", "High"): "EXCELLENT BUT NEEDS COUNSELING",
        ("Very High", "Very Low"): "NEEDS COUNSELING AND TRAINING",
        ("Very High", "Low"): "NEEDS COUNSELING AND TRAINING",
        ("Very High", "Moderate"): "NEEDS COUNSELING AND TRAINING",
        ("Very High", "High"): "GOOD BUT NEEDS COUNSELING",
        ("Very High", "Very High"): "Mental health needs counselling, but performance is excellent"
    }

    employer_action = pairing_map.get((stress_level, perf_level), "NO RECOMMENDATION")

    # Display results in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="padding:1rem; border-radius:12px; 
                    background:#f0f8ff; border-left:4px solid #1e90ff">
            <h3>🧠 Stress Level</h3>
            <p style="font-size:1.5rem; font-weight:bold; margin:0;">{stress_level}</p>
            <p style="font-size:1.2rem;">Mean Value: {stress_mean:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="padding:1rem; border-radius:12px; 
                    background:#fff0f5; border-left:4px solid #ff69b4">
            <h3>💼 Performance Level</h3>
            <p style="font-size:1.5rem; font-weight:bold; margin:0;">{perf_level}</p>
            <p style="font-size:1.2rem;">Mean Value: {perf_mean:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Visual Gauges for Mean Values ---
    fig1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress_mean,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [1, 5]},
            'bar': {'color': "#8A2BE2"},
            'steps': [
                {'range': [1, 2.5], 'color': "#ff9a9a"},
                {'range': [2.5, 3.5], 'color': "#fff59d"},
                {'range': [3.5, 5], 'color': "#a6f0c6"},
            ]}
    ))
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=perf_mean,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [1, 5]},
            'bar': {'color': "#00CED1"},
            'steps': [
                {'range': [1, 2.5], 'color': "#ff9a9a"},
                {'range': [2.5, 3.5], 'color': "#fff59d"},
                {'range': [3.5, 5], 'color': "#a6f0c6"},
            ]}
    ))
    st.plotly_chart(fig2, use_container_width=True)

    # Show Employer Action below results
    st.markdown(f"""
    <div style="margin-top:2rem; padding:1.5rem; background:#f5f5dc; 
                border-radius:12px; border-left:4px solid #FFD700">
        <h3>Recommended Employer Action:</h3>
        <p style='font-size:1.4rem;color:#3700B3;font-weight:bold'>{employer_action}</p>
    </div>
    """, unsafe_allow_html=True)

    # Restart button
    if st.button("🔄 Start New Assessment"):
        st.session_state.clear()
        st.session_state.page = 1
        st.rerun()





# --- App state ---
setup_page()
if "page" not in st.session_state:
    st.session_state.page = 1
if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = [None]*5
if "perf_answers" not in st.session_state:
    st.session_state.perf_answers = [None]*6

if st.session_state.page == 1:
    stress_assessment()
elif st.session_state.page == 2:
    performance_assessment()
elif st.session_state.page == 3:
    show_results()

