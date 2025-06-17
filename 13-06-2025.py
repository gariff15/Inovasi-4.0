import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

# Inject Lottie player script once
st.components.v1.html("""
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
""", height=0)

# CSS styling to minimize gaps and style results and animations
st.markdown("""
    <style>
    .result-box {
        background: #f0f4ff;
        border-radius: 12px;
        padding: 1em 1em 0.5em 1em;
        margin-top: 1em;
        box-shadow: 0 2px 8px rgba(79, 139, 249, 0.15);
        text-align: center;
    }
    .animation-container {
        margin-top: -35px !important;
        margin-bottom: 0.5em !important;
        text-align: center;
    }
    .celebration-container {
        margin-top: -45px !important;
        margin-bottom: 1em !important;
        display: flex;
        justify-content: center;
        gap: 15px;
    }
    .celebration-container lottie-player {
        width: 100px !important;
        height: 100px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Stresformance with Animations")
st.markdown("Answer the questions and click **Assess** to see your results with lively animations!")

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

def show_animation(animation_key, celebration=False):
    animations = {
        "stress_high": "https://assets3.lottiefiles.com/packages/lf20_1pxqjqps.json",  # Disaster / Stressful fire animation
        "stress_low": "https://assets3.lottiefiles.com/packages/lf20_jbrw3hcz.json",   # Calm celebration
        "perf_high": "https://assets3.lottiefiles.com/packages/lf20_touohxv0.json",   # Party/confetti
        "perf_low": "https://assets3.lottiefiles.com/packages/lf20_4kx2q32n.json"     # Sad gloomy
    }
    balloon = "https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"  # Balloon
    clap = "https://assets8.lottiefiles.com/packages/lf20_3rwasyjy.json"      # Clap

    url = animations.get(animation_key)
    if url:
        html(f"""
        <div class="animation-container">
            <lottie-player src="{url}" background="transparent" speed="1" style="width: 250px; height: 250px;" loop autoplay></lottie-player>
        </div>
        """, height=260)
    if celebration:
        html(f"""
        <div class="celebration-container">
            <lottie-player src="{balloon}" background="transparent" speed="1" loop autoplay></lottie-player>
            <lottie-player src="{clap}" background="transparent" speed="1" loop autoplay></lottie-player>
        </div>
        """, height=120)

# --- Stress Level Section ---
st.header("😰 Stress Level Questions")
stress_answers = []
for i, q in enumerate(stress_questions):
    ans = st.radio(q, options, key=f"stress_q{i+1}", horizontal=True)
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

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mean_stress,
            domain={'x': [0,1], 'y':[0,1]},
            title={'text': "Stress Meter"},
            gauge={
                'axis': {'range': [1,5]},
                'bar': {'color': "royalblue"},
                'steps': [
                    {'range': [1,1.5], 'color': "#cce5ff"},
                    {'range': [1.5,2], 'color': "#b3ffd9"},
                    {'range': [2,3], 'color': "#fffcb3"},
                    {'range': [3,4], 'color': "#ffd6b3"},
                    {'range': [4,5], 'color': "#ffb3b3"},
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_to("stress_result")

        if stress_class in ["High", "Very High"]:
            show_animation("stress_high")
            st.markdown("##########⚠️ Stress is high! Take care of yourself!")
        else:
            show_animation("stress_low", celebration=True)
            st.markdown("##########🎉 Stress is low! Keep up the good work!")

# --- Performance Level Section ---
st.markdown("---")
st.header("🚀 Performance Level Questions")
performance_answers = []
for i, q in enumerate(performance_questions):
    ans = st.radio(q, options, key=f"perf_q{i+6}", horizontal=True)
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

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mean_perf,
            domain={'x': [0,1], 'y':[0,1]},
            title={'text': "Performance Meter"},
            gauge={
                'axis': {'range': [1,5]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [1,1.5], 'color': "#b3ffd9"},
                    {'range': [1.5,2], 'color': "#cce5ff"},
                    {'range': [2,3], 'color': "#fffcb3"},
                    {'range': [3,4], 'color': "#ffd6b3"},
                    {'range': [4,5], 'color': "#ffb3b3"},
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_to("perf_result")

        if perf_class in ["Very High", "High"]:
            show_animation("perf_high", celebration=True)
            st.markdown("##########🎉 Excellent performance! Keep shining!")
        else:
            show_animation("perf_low")
            st.markdown("##########😞 Performance is low. Don't give up!")
