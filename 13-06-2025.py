import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

# --- Inject Lottie player and Confetti JS ---
st.components.v1.html("""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
function fireConfetti() {
    var duration = 2 * 1000;
    var animationEnd = Date.now() + duration;
    var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 1000 };
    function randomInRange(min, max) { return Math.random() * (max - min) + min; }
    var interval = setInterval(function() {
        var timeLeft = animationEnd - Date.now();
        if (timeLeft <= 0) { return clearInterval(interval); }
        var particleCount = 50 * (timeLeft / duration);
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.2, 0.8), y: Math.random() - 0.2 } }));
    }, 250);
}
</script>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
""", height=0)

# --- CSS Styling ---
st.markdown("""
<style>
  body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background: #121212;
    color: #E0E0E0;
  }
  h1, h2, h3, h4 {
    color: #bb86fc;
    font-weight: 900;
    letter-spacing: 1.2px;
    margin-bottom: 0.4em;
  }
  .result-title {
    margin-top: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: #03dac6;
    text-shadow: 0 0 10px #03dac6aa;
  }
  .score-text {
    margin-top: 0.5rem;
    font-size: 1.2rem;
    color: #e0e0e0cc;
  }
</style>
""", unsafe_allow_html=True)

# --- Questions and options ---
stress_questions = [
    "1. In the last 1-4 weeks, I found it hard to wind down.",
    "2. In the last 1-4 weeks, I tended to over-react to situations.",
    "3. In the last 1-4 weeks, I felt restless.",
    "4. In the last 1-4 weeks, I felt easily agitated.",
    "5. In the last 1-4 weeks, I felt difficult to relax."
]
performance_questions = [
    "6. During the past 1-4 weeks, how often was your performance lower than most workers at your workplace?",
    "7. During the past 1-4 weeks, how often did you do no work at times when you were supposed to be working?",
    "8. During the past 1-4 weeks, how often did you find yourself not working carefully as you should?",
    "9. During the past 1-4 weeks, how often was the quality of your work lower than it should be?",
    "10. During the past 1-4 weeks, how often do you not fully concentrate on your work?",
    "11. During the past 1-4 weeks, how often did health problems limit the kind or amount of work you could do?"
]
options = ["Very Rare", "Rare", "Moderate", "Frequent", "Very Frequent"]

def option_to_score(option):
    return {"Very Rare": 1, "Rare": 2, "Moderate": 3, "Frequent": 4, "Very Frequent": 5}[option]

def classify_stress_level(mean):
    if mean < 1.5:
        return "Very Low"
    elif mean < 2:
        return "Low"
    elif mean < 3:
        return "Moderate"
    elif mean < 4:
        return "High"
    else:
        return "Very High"

def classify_performance_level(mean):
    if mean < 1.5:
        return "Very High"
    elif mean < 2:
        return "High"
    elif mean < 3:
        return "Moderate"
    elif mean < 4:
        return "Low"
    else:
        return "Very Low"

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = 1
if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = [""] * len(stress_questions)
if "performance_answers" not in st.session_state:
    st.session_state.performance_answers = [""] * len(performance_questions)

# --- PAGE 1: Stress Assessment ---
if st.session_state.page == 1:
    st.title("Stress Level Assessment")
    st.markdown("### Please answer the following stress-related questions:")
    for i, q in enumerate(stress_questions):
        answer = st.radio(q, options, key=f"stress_q{i}")
        st.session_state.stress_answers[i] = answer
    if st.button("Next ➡️", type="primary"):
        if "" in st.session_state.stress_answers:
            st.warning("Please answer all stress questions before proceeding.")
        else:
            st.session_state.page = 2
            st.rerun()

# --- PAGE 2: Performance Assessment ---
elif st.session_state.page == 2:
    st.title("Performance Level Assessment")
    st.markdown("### Please answer the following performance-related questions:")
    for i, q in enumerate(performance_questions):
        answer = st.radio(q, options, key=f"perf_q{i}")
        st.session_state.performance_answers[i] = answer
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            if "" in st.session_state.performance_answers:
                st.warning("Please answer all performance questions before proceeding.")
            else:
                st.session_state.page = 3
                st.rerun()

# --- PAGE 3: Show results directly ---
elif st.session_state.page == 3:
    st.title("Results")

    # Calculate means and classifications
    stress_scores = [option_to_score(ans) for ans in st.session_state.stress_answers if ans]
    mean_stress = sum(stress_scores) / len(stress_scores) if stress_scores else 0
    stress_class = classify_stress_level(mean_stress)

    perf_scores = [option_to_score(ans) for ans in st.session_state.performance_answers if ans]
    mean_perf = sum(perf_scores) / len(perf_scores) if perf_scores else 0
    perf_class = classify_performance_level(mean_perf)

    # Trigger confetti only when results are displayed
    fireConfetti()

    # Stress Result
    st.header("Stress Level Result")
    st.markdown(f"**Stress Level:** {stress_class}")
    st.markdown(f"**Mean Score:** {mean_stress:.2f}")

    stress_anim = "https://assets4.lottiefiles.com/packages/lf20_k63yxshj.json"
    st.markdown(f'<lottie-player src="{stress_anim}" background="transparent" speed="1" style="width:180px; height:180px;" autoplay></lottie-player>', unsafe_allow_html=True)

    fig_stress = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mean_stress,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Stress Meter"},
        gauge={
            'axis': {'range': [1, 5], 'dtick': 1},
            'bar': {'color': "#bb86fc"},
            'steps': [
                {'range': [1, 1.5], 'color': "#a6f0c6"},
                {'range': [1.5, 2], 'color': "#c5e1a5"},
                {'range': [2, 3], 'color': "#fff59d"},
                {'range': [3, 4], 'color': "#ffcc80"},
                {'range': [4, 5], 'color': "#ef9a9a"},
            ],
            'threshold': {
                'line': {'color': "#bb86fc", 'width': 4},
                'thickness': 0.75,
                'value': mean_stress,
            },
        }
    ))
    st.plotly_chart(fig_stress, use_container_width=True)

    # Performance Result
    st.header("Performance Level Result")
    st.markdown(f"**Performance Level:** {perf_class}")
    st.markdown(f"**Mean Score:** {mean_perf:.2f}")

    perf_anim = "https://assets4.lottiefiles.com/packages/lf20_L5rijv.json"
    st.markdown(f'<lottie-player src="{perf_anim}" background="transparent" speed="1" style="width:180px; height:180px;" autoplay></lottie-player>', unsafe_allow_html=True)

    fig_perf = go.Figure(go.Indicator(
        mode="gauge+number",
        value=mean_perf,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Performance Meter"},
        gauge={
            'axis': {'range': [1, 5], 'dtick': 1},
            'bar': {'color': "#03dac6"},
            'steps': [
                {'range': [1, 1.5], 'color': "#ef9a9a"},
                {'range': [1.5, 2], 'color': "#ffcc80"},
                {'range': [2, 3], 'color': "#fff59d"},
                {'range': [3, 4], 'color': "#c5e1a5"},
                {'range': [4, 5], 'color': "#a6f0c6"},
            ],
            'threshold': {
                'line': {'color': "#03dac6", 'width': 4},
                'thickness': 0.75,
                'value': mean_perf,
            },
        }
    ))
    st.plotly_chart(fig_perf, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Performance Questions"):
            st.session_state.page = 2
            st.rerun()
    with col2:
        if st.button("🔄 Restart Assessment"):
            for k in ['stress_answers', 'performance_answers']:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.page = 1
            st.rerun()
