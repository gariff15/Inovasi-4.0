import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html
from typing import List, Dict, Optional

# ========== CONSTANTS ==========
STRESS_QUESTIONS = [
    "1. In the last 1-4 weeks, I found it hard to wind down.",
    "2. In the last 1-4 weeks, I tended to over-react to situations.",
    "3. In the last 1-4 weeks, I felt restless.",
    "4. In the last 1-4 weeks, I felt easily agitated.",
    "5. In the last 1-4 weeks, I felt difficult to relax."
]

PERFORMANCE_QUESTIONS = [
    "6. During the past 1-4 weeks, how often was your performance lower than most workers?",
    "7. During the past 1-4 weeks, how often did you do no work when you should?",
    "8. During the past 1-4 weeks, how often did you not work carefully?",
    "9. During the past 1-4 weeks, how often was your work quality low?",
    "10. During the past 1-4 weeks, how often did you not fully concentrate?",
    "11. During the past 1-4 weeks, how often did health problems limit your work?"
]

OPTIONS = ["Very Rare", "Rare", "Moderate", "Frequent", "Very Frequent"]
OPTION_SCORES = {"Very Rare": 1, "Rare": 2, "Moderate": 3, "Frequent": 4, "Very Frequent": 5}

# ========== SETUP ==========
def setup_page():
    """Configure page settings and inject scripts"""
    st.set_page_config(
        page_title="Mental Health Assessment",
        page_icon="🧠",
        layout="centered"
    )
    
    # Inject confetti and Lottie scripts
    html(f"""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <script>
    function fireConfetti() {{
        confetti({{
            particleCount: 150,
            spread: 70,
            origin: {{ y: 0.6 }},
            colors: ['#bb86fc', '#03dac6', '#ffffff']
        }});
    }}
    </script>
    """, height=0)

    # Custom CSS
    st.markdown("""
    <style>
    body, .stApp {
        font-family: 'Inter', sans-serif;
        background: #121212;
        color: #E0E0E0;
    }
    h1 {
        color: #bb86fc;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #03dac6;
        margin-top: 1.5rem;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
    }
    .stButton button {
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ========== CORE FUNCTIONS ==========
def trigger_confetti():
    """Triggers confetti animation"""
    html("<script>fireConfetti();</script>", height=0)

def calculate_mean(scores: List[int]) -> float:
    """Calculate mean score with safety checks"""
    return sum(scores) / len(scores) if scores else 0

def classify_stress_level(mean: float) -> str:
    """Classify stress based on mean score"""
    if mean < 1.5: return "Very Low"
    elif mean < 2: return "Low" 
    elif mean < 3: return "Moderate"
    elif mean < 4: return "High"
    return "Very High"

def classify_performance_level(mean: float) -> str:
    """Classify performance based on mean score"""
    if mean < 1.5: return "Very High"
    elif mean < 2: return "High"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "Low"
    return "Very Low"

# ========== PAGE COMPONENTS ==========
def stress_assessment():
    """Render the stress assessment page"""
    st.title("Stress Level Assessment")
    st.write("Rate how often you've experienced these feelings:")
    
    for i, question in enumerate(STRESS_QUESTIONS):
        st.session_state.stress_answers[i] = st.radio(
            question, 
            OPTIONS,
            key=f"stress_{i}",
            index=None  # No default selection
        )
    
    if st.button("Continue to Performance", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("Please answer all questions")
        else:
            st.session_state.page = 2
            st.rerun()

def performance_assessment():
    """Render the performance assessment page"""
    st.title("Performance Level Assessment")
    st.write("Rate how often these performance issues occurred:")
    
    for i, question in enumerate(PERFORMANCE_QUESTIONS):
        st.session_state.perf_answers[i] = st.radio(
            question,
            OPTIONS,
            key=f"perf_{i}",
            index=None
        )
    
    col1, col2 = st.columns([1, 2])
    col1.button("Back", on_click=lambda: st.session_state.update(page=1))
    
    if col2.button("View Results", type="primary"):
        if None in st.session_state.perf_answers:
            st.warning("Please answer all questions")
        else:
            st.session_state.page = 3
            st.rerun()

def show_results():
    """Render the results page"""
    st.title("Assessment Results")
    trigger_confetti()
    
    # Process stress results
    stress_scores = [OPTION_SCORES[ans] for ans in st.session_state.stress_answers]
    stress_mean = calculate_mean(stress_scores)
    stress_class = classify_stress_level(stress_mean)
    
    # Process performance results
    perf_scores = [OPTION_SCORES[ans] for ans in st.session_state.perf_answers]
    perf_mean = calculate_mean(perf_scores)
    perf_class = classify_performance_level(perf_mean)
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Stress Level")
        st.metric("Classification", stress_class)
        st.metric("Average Score", f"{stress_mean:.2f}")
        plot_gauge(stress_mean, [1, 5], "Stress Meter", "#bb86fc")
    
    with col2:
        st.subheader("💼 Performance Level")
        st.metric("Classification", perf_class)
        st.metric("Average Score", f"{perf_mean:.2f}")
        plot_gauge(perf_mean, [1, 5], "Performance Meter", "#03dac6")
    
    # Celebration animation
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <lottie-player 
            src="https://assets4.lottiefiles.com/packages/lf20_5tkzkblw.json" 
            background="transparent" 
            speed="1" 
            style="width: 200px; height: 200px; margin: 0 auto;"
            autoplay>
        </lottie-player>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("Start New Assessment", on_click=lambda: (
        st.session_state.clear(),
        st.session_state.update(page=1),
        st.rerun()
    ))

def plot_gauge(value: float, range: List[float], title: str, color: str):
    """Create a Plotly gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': range},
            'bar': {'color': color},
            'steps': [
                {'range': [1, 2.5], 'color': "#2e7d32"},
                {'range': [2.5, 3.5], 'color': "#ff8f00"},
                {'range': [3.5, 5], 'color': "#c62828"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# ========== MAIN APP ==========
def main():
    """Main application flow"""
    setup_page()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "stress_answers" not in st.session_state:
        st.session_state.stress_answers = [None] * len(STRESS_QUESTIONS)
    if "perf_answers" not in st.session_state:
        st.session_state.perf_answers = [None] * len(PERFORMANCE_QUESTIONS)
    
    # Page routing
    if st.session_state.page == 1:
        stress_assessment()
    elif st.session_state.page == 2:
        performance_assessment()
    elif st.session_state.page == 3:
        show_results()

if __name__ == "__main__":
    main()
