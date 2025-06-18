import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

# Inject confetti JS and Lottie player script once
st.components.v1.html("""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
function fireConfetti() {
    var duration = 3 * 1000;
    var animationEnd = Date.now() + duration;
    var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 1000 };
    function randomInRange(min, max) { return Math.random() * (max - min) + min; }
    var interval = setInterval(function() {
        var timeLeft = animationEnd - Date.now();
        if (timeLeft <= 0) { return clearInterval(interval); }
        var particleCount = 50 * (timeLeft / duration);
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0, 1), y: Math.random() - 0.2 } }));
    }, 250);
}
</script>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
""", height=0)

# CSS styling
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
    color: #222;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.result-box {
    background: rgba(255,255,255,0.95);
    border-radius: 16px;
    padding: 1.5em 1em 1em 1em;
    margin-top: 1em;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    text-align: center;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    transition: all 0.5s ease;
}
.giftbox-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 60px;
    margin-bottom: 2em;
    margin-top: 1em;
}
.giftbox {
    background: rgba(255,255,255,0.85);
    border-radius: 14px;
    padding: 1em 1em 2em 1em;
    box-shadow: 0 4px 18px rgba(0,0,0,0.10);
    text-align: center;
    width: 320px;
    min-height: 380px;
    position: relative;
}
.giftbox h3 {
    margin-bottom: 0.3em;
}
.open-animation {
    margin-top: -35px;
    margin-bottom: 0.5em;
    text-align: center;
}
.slot-label {
    font-size: 1.1em;
    font-weight: bold;
    color: #4f8bf9;
    margin-bottom: 0.2em;
}
</style>
""", unsafe_allow_html=True)

# Questions
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
    return {"Very Rare":1, "Rare":2, "Moderate":3, "Frequent":4, "Very Frequent":5}[option]

def classify_stress_level(mean):
    if mean < 1.5: return "Very Low"
    elif mean < 2: return "Low"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "High"
    else: return "Very High"

def classify_performance_level(mean):
    if mean < 1.5: return "Very High"
    elif mean < 2: return "High"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "Low"
    else: return "Very Low"

def scroll_to(id_name):
    js = f"""
    <script>
    const el = window.parent.document.getElementById('{id_name}');
    if(el) {{
        el.scrollIntoView({{behavior: 'smooth'}});
    }}
    </script>
    """
    html(js, height=0)

def trigger_confetti():
    html("<script>fireConfetti();</script>", height=0)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 1
if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = [None]*5
if "performance_answers" not in st.session_state:
    st.session_state.performance_answers = [None]*6
if "stress_opened" not in st.session_state:
    st.session_state.stress_opened = False
if "perf_opened" not in st.session_state:
    st.session_state.perf_opened = False

# Page 1: Stress Questions
if st.session_state.page == 1:
    st.title("Page 1: Stress Level Assessment")
    st.markdown("#### Please answer all stress questions below:")

    for i, q in enumerate(stress_questions):
        st.session_state.stress_answers[i] = st.radio(
            q, options, key=f"stress_q{i+1}", horizontal=True, index=None
        )
    if st.button("Next ➡️", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("Please answer all stress questions before proceeding.")
        else:
            st.session_state.page = 2
            st.experimental_rerun()

# Page 2: Performance Questions
elif st.session_state.page == 2:
    st.title("Page 2: Performance Level Assessment")
    st.markdown("#### Please answer all performance questions below:")

    for i, q in enumerate(performance_questions):
        st.session_state.performance_answers[i] = st.radio(
            q, options, key=f"perf_q{i+6}", horizontal=True, index=None
        )
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("⬅️ Back", key="back1"):
            st.session_state.page = 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ➡️", key="next2", type="primary"):
            if None in st.session_state.performance_answers:
                st.warning("Please answer all performance questions before proceeding.")
            else:
                st.session_state.page = 3
                st.experimental_rerun()

# Page 3: Results with Gift Boxes
elif st.session_state.page == 3:
    st.title("Page 3: 🎁 Your Results!")
    st.markdown("#### Click each gift box to reveal your result!")

    # Calculate results
    stress_scores = [option_to_score(a) for a in st.session_state.stress_answers]
    mean_stress = sum(stress_scores) / len(stress_scores)
    stress_class = classify_stress_level(mean_stress)

    perf_scores = [option_to_score(a) for a in st.session_state.performance_answers]
    mean_perf = sum(perf_scores) / len(perf_scores)
    perf_class = classify_performance_level(mean_perf)

    # Lottie URLs
    giftbox_lottie = "https://assets9.lottiefiles.com/packages/lf20_5ngs2ksb.json"  # gift box closed
    openbox_lottie = "https://assets9.lottiefiles.com/packages/lf20_2ksqv5tq.json"  # gift box opening
    sparkle_lottie = "https://assets9.lottiefiles.com/packages/lf20_0yfsb3a1.json"  # sparkle effect

    st.markdown('<div class="giftbox-container">', unsafe_allow_html=True)

    # Stress Gift Box
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="giftbox">', unsafe_allow_html=True)
        st.markdown('<div class="slot-label">Stress Level</div>', unsafe_allow_html=True)
        if not st.session_state.stress_opened:
            html(f"""
            <div class="open-animation">
                <lottie-player src="{giftbox_lottie}" background="transparent" speed="1" style="width: 180px; height: 180px;" loop autoplay></lottie-player>
            </div>
            """, height=190)
            if st.button("🎁 Assess Stress Level", key="open_stress"):
                st.session_state.stress_opened = True
                trigger_confetti()
                st.experimental_rerun()
        else:
            html(f"""
            <div class="open-animation" style="position: relative;">
                <lottie-player src="{openbox_lottie}" background="transparent" speed="1" style="width: 180px; height: 180px;" autoplay></lottie-player>
                <lottie-player src="{sparkle_lottie}" background="transparent" speed="1" style="width: 80px; height: 80px; position: absolute; top: 10px; left: 50%; transform: translateX(-50%);" autoplay></lottie-player>
            </div>
            """, height=180)
            st.subheader(f"Stress Level: {stress_class}")
            st.write(f"Mean Score: **{mean_stress:.2f}**")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=mean_stress,
                domain={'x': [0,1], 'y':[0,1]},
                title={'text': "Stress Meter"},
                gauge={
                    'axis': {'range': [1,5]},
                    'bar': {'color': "royalblue"},
                    'steps': [
                        {'range': [1,1.5], 'color': "#b3ffd9"},
                        {'range': [1.5,2], 'color': "#ccffcc"},
                        {'range': [2,3], 'color': "#ffffcc"},
                        {'range': [3,4], 'color': "#ffd6b3"},
                        {'range': [4,5], 'color': "#ffb3b3"},
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Performance Gift Box
    with col2:
        st.markdown('<div class="giftbox">', unsafe_allow_html=True)
        st.markdown('<div class="slot-label">Performance Level</div>', unsafe_allow_html=True)
        if not st.session_state.perf_opened:
            html(f"""
            <div class="open-animation">
                <lottie-player src="{giftbox_lottie}" background="transparent" speed="1" style="width: 180px; height: 180px;" loop autoplay></lottie-player>
            </div>
            """, height=190)
            if st.button("🎁 Assess Performance", key="open_perf"):
                st.session_state.perf_opened = True
                trigger_confetti()
                st.experimental_rerun()
        else:
            html(f"""
            <div class="open-animation" style="position: relative;">
                <lottie-player src="{openbox_lottie}" background="transparent" speed="1" style="width: 180px; height: 180px;" autoplay></lottie-player>
                <lottie-player src="{sparkle_lottie}" background="transparent" speed="1" style="width: 80px; height: 80px; position: absolute; top: 10px; left: 50%; transform: translateX(-50%);" autoplay></lottie-player>
            </div>
            """, height=180)
            st.subheader(f"Performance Level: {perf_class}")
            st.write(f"Mean Score: **{mean_perf:.2f}**")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=mean_perf,
                domain={'x': [0,1], 'y':[0,1]},
                title={'text': "Performance Meter"},
                gauge={
                    'axis': {'range': [1,5]},
                    'bar': {'color': "crimson"},
                    'steps': [
                        {'range': [1,1.5], 'color': "#ffb3b3"},
                        {'range': [1.5,2], 'color': "#ffd6b3"},
                        {'range': [2,3], 'color': "#fffcb3"},
                        {'range': [3,4], 'color': "#ccffcc"},
                        {'range': [4,5], 'color': "#b3ffd9"},
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation buttons
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("⬅️ Back to Performance Questions", key="back2"):
            st.session_state.page = 2
            st.session_state.stress_opened = False
            st.session_state.perf_opened = False
            st.experimental_rerun()
    with col2:
        if st.button("🔄 Restart", key="restart"):
            for k in ["stress_answers", "performance_answers", "stress_opened", "perf_opened"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.page = 1
            st.experimental_rerun()
