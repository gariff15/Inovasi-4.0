import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

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
    st.set_page_config(
        page_title="STRESFORMANCE TRACKER",
        page_icon="🧠💼",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    html("""
    <style>
    .big-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 900;
        color: #8A2BE2;
        margin-bottom: 0.2em;
        letter-spacing: 2px;
        line-height: 1.1;
        text-shadow: 0 4px 18px rgba(138, 43, 226, 0.25), 0 1px 0 #fff, 0 0 40px #FFD700;
    }
    </style>
    """, height=0)

def show_header():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <lottie-player 
            src="https://assets9.lottiefiles.com/packages/lf20_5tkzkblw.json" 
            background="transparent" 
            speed="1" 
            style="width: 120px; height: 120px; margin: 0 auto;"
            autoplay>
        </lottie-player>
        <div class="big-title">STRESFORMANCE<br>TRACKER</div>
    </div>
    """, unsafe_allow_html=True)

def trigger_confetti():
    html("""
    <script>
    if (window.fireConfetti) { fireConfetti(); }
    </script>
    """, height=0)

def calculate_mean(scores):
    return sum(scores) / len(scores) if scores else 0

def classify_stress_level(mean):
    if mean < 1.5: return "🌊 Very Low - Excellent Resilience"
    elif mean < 2: return "🌤️ Low - Good Balance" 
    elif mean < 3: return "🌓 Moderate - Needs Attention"
    elif mean < 4: return "🌋 High - Significant Stress"
    return "🔥 Very High - Critical Levels"

def classify_performance_level(mean):
    if mean < 1.5: return "🚀 Very High - Peak Performance"
    elif mean < 2: return "🏆 High - Strong Output"
    elif mean < 3: return "🔄 Moderate - Room for Improvement"
    elif mean < 4: return "⚠️ Low - Needs Support"
    return "😢 Very Low - Very Unproductive"

def plot_dynamic_gauge(value, title, is_stress):
    bar_color = "#8A2BE2" if is_stress else "#FFD700"
    steps = [
        {'range': [1, 2], 'color': '#A3E4D7' if is_stress else '#F5B7B1'},
        {'range': [2, 3], 'color': '#FAD7A0'},
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
            question, OPTIONS, key=f"stress_{i}", index=None
        )
    if st.button("🚀 Continue to Performance Assessment", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("⚠️ Please answer all questions to proceed")
        else:
            st.session_state.page = 2
            st.rerun()

def performance_assessment():
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
            question, OPTIONS, key=f"perf_{i}", index=None
        )
    col1, col2 = st.columns([1, 2])
    col1.button("🔙 Back", on_click=lambda: st.session_state.update(page=1))
    if col2.button("📊 View My Results", type="primary"):
        if None in st.session_state.perf_answers:
            st.warning("⚠️ Please answer all questions to see your results")
        else:
            st.session_state.page = 3
            st.rerun()

def show_results():
    trigger_confetti()
    stress_scores = [OPTION_SCORES[ans] for ans in st.session_state.stress_answers]
    stress_mean = calculate_mean(stress_scores)
    stress_class = classify_stress_level(stress_mean)
    perf_scores = [OPTION_SCORES[ans] for ans in st.session_state.perf_answers]
    perf_mean = calculate_mean(perf_scores)
    perf_class = classify_performance_level(perf_mean)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>Your Assessment Results</h2>
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_olc8tpeq.json" 
            background="transparent" 
            speed="1" 
            style="width: 200px; height: 200px; margin: -2rem auto;"
            autoplay>
        </lottie-player>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #f7f3ff; border-radius: 18px; padding: 1.5rem 1.2rem; margin-bottom: 2rem; box-shadow: 0 3px 18px rgba(138, 43, 226, 0.13); border-left: 5px solid #8A2BE2;">
            <h3 style="color: #8A2BE2;">🧠 Stress Analysis</h3>
            <div style="font-size: 1.2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Level:</span>
                    <span style="font-weight: 600;">{stress_class.split(' - ')[0]}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Score:</span>
                    <span style="font-weight: 600;">{stress_mean:.2f}/5.00</span>
                </div>
            </div>
            <p style="color: #FFD700; font-style: italic;">{stress_class.split(' - ')[1]}</p>
        </div>
        """, unsafe_allow_html=True)
        plot_dynamic_gauge(stress_mean, "🧠 Stress Meter", is_stress=True)
    with col2:
        st.markdown(f"""
        <div style="background: #fffbe5; border-radius: 18px; padding: 1.5rem 1.2rem; margin-bottom: 2rem; box-shadow: 0 3px 18px rgba(255, 215, 0, 0.13); border-left: 5px solid #FFD700;">
            <h3 style="color: #FFD700;">💼 Performance Analysis</h3>
            <div style="font-size: 1.2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Level:</span>
                    <span style="font-weight: 600;">{perf_class.split(' - ')[0]}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Score:</span>
                    <span style="font-weight: 600;">{perf_mean:.2f}/5.00</span>
                </div>
            </div>
            <p style="color: #8A2BE2; font-style: italic;">{perf_class.split(' - ')[1]}</p>
        </div>
        """, unsafe_allow_html=True)
        plot_dynamic_gauge(perf_mean, "💼 Performance Meter", is_stress=False)
    st.markdown("---")
    col3, col4 = st.columns([1,1])
    with col3:
        if st.button("⬅️ Back to Performance Questions", key="back2"):
            st.session_state.page = 2
            st.rerun()
    with col4:
        if st.button("🔄 Restart", key="restart"):
            for k in ["stress_answers", "perf_answers"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.page = 1
            st.rerun()

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
