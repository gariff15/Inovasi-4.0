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
    margin: 0;
  }
  h1, h2, h3, h4 {
    color: #bb86fc;
    font-weight: 900;
    letter-spacing: 1.2px;
    margin-bottom: 0.4em;
  }
  .giftbox-row {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin: 2.5rem 0 3rem 0;
    flex-wrap: wrap;
  }
  .giftbox-game {
    background: linear-gradient(145deg, #2c2c38, #212129);
    border-radius: 24px;
    box-shadow:
      0 4px 8px rgba(0,0,0,0.6),
      inset 0 0 8px #7b52e3aa;
    padding: 2rem 2rem 2.5rem 2rem;
    width: 340px;
    min-height: 480px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    filter: drop-shadow(0 0 12px #7b52e3cc);
    cursor: default;
    user-select: none;
  }
  .giftbox-game:hover {
    transform: scale(1.05);
    filter: drop-shadow(0 0 20px #bb86fc);
    transition: all 0.3s ease;
  }
  .slot-label {
    font-size: 1.5rem;
    color: #bb86fc;
    font-weight: 800;
    margin-bottom: 1rem;
    text-shadow: 0 0 6px #bb86fcaa;
    text-align: center;
  }
  .result-title {
    margin-top: 1rem;
    font-size: 1.3rem;
    font-weight: 700;
    color: #03dac6;
    text-shadow: 0 0 10px #03dac6aa;
    text-align: center;
  }
  .score-text {
    margin-top: 0.3rem;
    font-size: 1.1rem;
    color: #e0e0e0cc;
    text-align: center;
  }
  .assess-btn-wrapper {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  .assess-btn {
    background: linear-gradient(90deg, #bb86fc, #3700b3);
    color: white;
    font-weight: 700;
    font-size: 1.25rem;
    padding: 0.8rem 2rem;
    border: none;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(187,134,252,0.7);
    cursor: pointer;
    transition: background 0.3s ease;
  }
  .assess-btn:hover {
    background: linear-gradient(90deg, #3700b3, #bb86fc);
  }
  /* Responsive adjustments */
  @media (max-width: 750px) {
    .giftbox-row {
      flex-direction: column;
      align-items: center;
      gap: 40px;
    }
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

def trigger_confetti():
    html("<script>fireConfetti();</script>", height=0)

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = 1
if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = [None] * len(stress_questions)
if "performance_answers" not in st.session_state:
    st.session_state.performance_answers = [None] * len(performance_questions)
if "stress_revealed" not in st.session_state:
    st.session_state.stress_revealed = False
if "perf_revealed" not in st.session_state:
    st.session_state.perf_revealed = False

# --- PAGE 1: Stress Assessment ---
if st.session_state.page == 1:
    st.title("Stress Level Assessment")
    st.markdown("### Please answer the following stress-related questions:")
    for i, q in enumerate(stress_questions):
        # Use radio with no default selection manually handled
        selected = st.radio(q, options, key=f"stress_q{i}")
        st.session_state.stress_answers[i] = selected if selected != '' else None
    if st.button("Next ➡️", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("Please answer all stress questions before proceeding.")
        else:
            st.session_state.page = 2
            st.rerun()

# --- PAGE 2: Performance Assessment ---
elif st.session_state.page == 2:
    st.title("Performance Level Assessment")
    st.markdown("### Please answer the following performance-related questions:")
    for i, q in enumerate(performance_questions):
        selected = st.radio(q, options, key=f"perf_q{i}")
        st.session_state.performance_answers[i] = selected if selected != '' else None
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            if None in st.session_state.performance_answers:
                st.warning("Please answer all performance questions before proceeding.")
            else:
                st.session_state.page = 3
                st.session_state.stress_revealed = False
                st.session_state.perf_revealed = False
                st.rerun()

# --- PAGE 3: Results with centered 'Assess' buttons in boxes ---
elif st.session_state.page == 3:
    st.title("Results")
    st.markdown("#### Click the 'Assess' button inside each box to reveal the result.")

    stress_scores = [option_to_score(ans) for ans in st.session_state.stress_answers]
    mean_stress = sum(stress_scores) / len(stress_scores)
    stress_class = classify_stress_level(mean_stress)

    perf_scores = [option_to_score(ans) for ans in st.session_state.performance_answers]
    mean_perf = sum(perf_scores) / len(perf_scores)
    perf_class = classify_performance_level(mean_perf)

    anim_open_stress = "https://assets4.lottiefiles.com/packages/lf20_k63yxshj.json"
    anim_open_perf = "https://assets4.lottiefiles.com/packages/lf20_L5rijv.json"

    st.markdown('<div class="giftbox-row">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Stress box
    with col1:
        st.markdown('<div class="giftbox-game">', unsafe_allow_html=True)
        st.markdown('<div class="slot-label">Stress Measure Result</div>', unsafe_allow_html=True)

        if not st.session_state.stress_revealed:
            if st.button("Assess Stress Level", key="assess_stress"):
                st.session_state.stress_revealed = True
                trigger_confetti()
                st.rerun()
        else:
            st.markdown(f'''
            <lottie-player src="{anim_open_stress}" background="transparent" speed="1" style="width:180px; height:180px; margin: 0 auto 1rem auto;" autoplay></lottie-player>
            <div class="result-title">Stress Level: {stress_class}</div>
            <div class="score-text">Mean Score: <strong>{mean_stress:.2f}</strong></div>
            ''', unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
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
                },
            )).update_layout(margin=dict(l=0, r=0, t=15, b=15), height=280)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Performance box
    with col2:
        st.markdown('<div class="giftbox-game">', unsafe_allow_html=True)
        st.markdown('<div class="slot-label">Performance Measure Result</div>', unsafe_allow_html=True)

        if not st.session_state.perf_revealed:
            if st.button("Assess Performance Level", key="assess_perf"):
                st.session_state.perf_revealed = True
                trigger_confetti()
                st.rerun()
        else:
            st.markdown(f'''
            <lottie-player src="{anim_open_perf}" background="transparent" speed="1" style="width:180px; height:180px; margin: 0 auto 1rem auto;" autoplay></lottie-player>
            <div class="result-title">Performance Level: {perf_class}</div>
            <div class="score-text">Mean Score: <strong>{mean_perf:.2f}</strong></div>
            ''', unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
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
                },
            )).update_layout(margin=dict(l=0, r=0, t=15, b=15), height=280)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation buttons
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("⬅️ Back to Performance Questions"):
            st.session_state.page = 2
            # Reset reveal flags for reattempt
            st.session_state.stress_revealed = False
            st.session_state.perf_revealed = False
            st.rerun()
    with nav_col2:
        if st.button("🔄 Restart Assessment"):
            for key in ['stress_answers', 'performance_answers', 'stress_revealed', 'perf_revealed']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.page = 1
            st.rerun()

