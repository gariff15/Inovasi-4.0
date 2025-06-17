import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

# Inject Lottie player script once for confetti effect
st.components.v1.html("""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
function fireConfetti() {
    var duration = 5 * 1000;
    var animationEnd = Date.now() + duration;
    var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 1000 };

    function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    var interval = setInterval(function() {
        var timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            return clearInterval(interval);
        }

        var particleCount = 50 * (timeLeft / duration);
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0, 1), y: Math.random() - 0.2 } }));
    }, 250);
}
</script>
""", height=0)

# CSS styling for neat layout and effects
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        color: #222;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .result-box {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 16px;
        padding: 1.5em;
        margin-top: 1em;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        transition: all 0.5s ease;
    }
    h1, h2, h3 {
        text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Stresformance - Reverse Performance Meter Colors")
st.markdown("Answer the questions and click **Assess** to see your results with reversed performance meter colors!")

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

# --- Stress Level Section ---
st.header("😰 Stress Level Questions")
stress_answers = []
for i, q in enumerate(stress_questions):
    ans = st.radio(q, options, key=f"stress_q{i+1}", horizontal=True, index=None)
    stress_answers.append(ans)
stress_assess = st.button("Assess Stress Level")

if stress_assess:
    if None in stress_answers:
        st.warning("Please answer all stress questions.")
    else:
        scores = [option_to_score(a) for a in stress_answers]
        mean_stress = sum(scores) / len(scores)
        stress_class = classify_stress_level(mean_stress)

        st.markdown('<div id="stress_result" class="result-box">', unsafe_allow_html=True)
        st.subheader(f"Stress Level: {stress_class} (Mean: {mean_stress:.2f})")

        # Stress meter: normal color scale (green = low stress)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mean_stress,
            domain={'x': [0,1], 'y':[0,1]},
            title={'text': "Stress Meter"},
            gauge={
                'axis': {'range': [1,5]},
                'bar': {'color': "royalblue"},
                'steps': [
                    {'range': [1,1.5], 'color': "#b3ffd9"},  # greenish low stress
                    {'range': [1.5,2], 'color': "#ccffcc"},
                    {'range': [2,3], 'color': "#ffffcc"},
                    {'range': [3,4], 'color': "#ffd6b3"},
                    {'range': [4,5], 'color': "#ffb3b3"},  # reddish high stress
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_to("stress_result")

        if stress_class in ["High", "Very High"]:
            st.markdown("<h3 style='color:#d32f2f; text-shadow: 0 0 10px #ff0000;'>⚠️ High Stress Detected! Please take care!</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:#388e3c; text-shadow: 0 0 10px #00ff00;'>🎉 Low Stress! Keep it up!</h3>", unsafe_allow_html=True)
            trigger_confetti()

# --- Performance Level Section ---
st.markdown("---")
st.header("🚀 Performance Level Questions")
performance_answers = []
for i, q in enumerate(performance_questions):
    ans = st.radio(q, options, key=f"perf_q{i+6}", horizontal=True, index=None)
    performance_answers.append(ans)
performance_assess = st.button("Assess Performance Level")

if performance_assess:
    if None in performance_answers:
        st.warning("Please answer all performance questions.")
    else:
        scores = [option_to_score(a) for a in performance_answers]
        mean_perf = sum(scores) / len(scores)
        perf_class = classify_performance_level(mean_perf)

        st.markdown('<div id="perf_result" class="result-box">', unsafe_allow_html=True)
        st.subheader(f"Performance Level: {perf_class} (Mean: {mean_perf:.2f})")

        # Performance meter: reversed color scale (green = low performance, red = high performance)
        # So invert colors: low values (good performance) red, high values (bad) green
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mean_perf,
            domain={'x': [0,1], 'y':[0,1]},
            title={'text': "Performance Meter"},
            gauge={
                'axis': {'range': [1,5]},
                'bar': {'color': "crimson"},
                'steps': [
                    {'range': [1,1.5], 'color': "#ffb3b3"},  # red = very high performance (good)
                    {'range': [1.5,2], 'color': "#ffd6b3"},
                    {'range': [2,3], 'color': "#fffcb3"},
                    {'range': [3,4], 'color': "#ccffcc"},
                    {'range': [4,5], 'color': "#b3ffd9"},  # green = very low performance (bad)
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_to("perf_result")

        # Reverse animation color logic:
        # High/Very High performance (mean low) => celebration (confetti)
        # Low/Very Low performance (mean high) => caution message, no confetti
        if perf_class in ["Very High", "High"]:
            st.markdown("<h3 style='color:#d32f2f; text-shadow: 0 0 10px #ff0000;'>🎉 Outstanding Performance! Keep shining!</h3>", unsafe_allow_html=True)
            trigger_confetti()
        else:
            st.markdown("<h3 style='color:#388e3c; text-shadow: 0 0 10px #006400;'>😞 Performance is low. Stay motivated!</h3>", unsafe_allow_html=True)
