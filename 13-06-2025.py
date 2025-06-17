import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

# CSS styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    .stButton>button {
        background-color: #4f8bf9;
        color: white;
        border-radius: 8px;
        padding: 0.5em 2em;
        font-size: 1.2em;
        font-weight: bold;
        transition: 0.2s;
        margin-top: 0.5em;
    }
    .stButton>button:hover {
        background-color: #2357b3;
    }
    .result-box {
        background: #f0f4ff;
        border-radius: 12px;
        padding: 1.5em;
        margin-top: 1em;
        box-shadow: 0 2px 8px rgba(79, 139, 249, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Stresformance")
st.markdown("""
Welcome to **Stresformance**!  
Answer the questions and click **Assess** to see your results and hear sound effects automatically.
""")

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
    return {
        "Very Rare": 1,
        "Rare": 2,
        "Moderate": 3,
        "Frequent": 4,
        "Very Frequent": 5
    }[option]

def classify_stress_level(mean):
    if mean < 1.5:
        return "Very Low"
    elif 1.5 <= mean < 2:
        return "Low"
    elif 2 <= mean < 3:
        return "Moderate"
    elif 3 <= mean < 4:
        return "High"
    else:
        return "Very High"

def classify_performance_level(mean):
    if mean < 1.5:
        return "Very High"
    elif 1.5 <= mean < 2:
        return "High"
    elif 2 <= mean < 3:
        return "Moderate"
    elif 3 <= mean < 4:
        return "Low"
    else:
        return "Very Low"

def scroll_to(id_name):
    scroll_js = f"""
    <script>
    const element = window.parent.document.getElementById('{id_name}');
    if (element) {{
        element.scrollIntoView({{behavior: 'smooth'}});
    }}
    </script>
    """
    html(scroll_js, height=0)

def play_sound_automatic(audio_url):
    audio_html = f"""
    <audio autoplay>
        <source src="{audio_url}" type="audio/mpeg" />
        
    </audio>
    """
    html(audio_html, height=0)

# Google Drive direct links for your sounds
HAPPY_SOUND_URL = "https://drive.google.com/file/d/1nKTjeW0TFpFmT5R-caEzhrgCswGroVeU/view?usp=sharing"
DISAPPOINTING_SOUND_URL = "https://drive.google.com/file/d/1yUT3DTbfxinbknPI7wNj2eZqizqYw6d-/view?usp=sharing"

# Stress Level Section
st.markdown("## 😰 Stress Level Questions (1-5)")
stress_answers = []
for i, q in enumerate(stress_questions):
    ans = st.radio(q, options, key=f"stress_q{i+1}", horizontal=True, index=None)
    stress_answers.append(ans)
stress_assess = st.button("Assess Stress Level")

if stress_assess:
    if None in stress_answers:
        st.warning("Please answer all Stress Level questions before assessing.")
    else:
        scores = [option_to_score(a) for a in stress_answers]
        mean_stress = sum(scores) / len(scores)
        stress_class = classify_stress_level(mean_stress)

        st.markdown('<div id="stress_result" class="result-box">', unsafe_allow_html=True)
        st.subheader(f"Stress Level: {stress_class} (Mean: {mean_stress:.2f})")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mean_stress,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Stress Meter"},
            gauge={
                'axis': {'range': [1, 5]},
                'bar': {'color': "royalblue"},
                'steps': [
                    {'range': [1, 1.5], 'color': "#cce5ff"},
                    {'range': [1.5, 2], 'color': "#b3ffd9"},
                    {'range': [2, 3], 'color': "#fffcb3"},
                    {'range': [3, 4], 'color': "#ffd6b3"},
                    {'range': [4, 5], 'color': "#ffb3b3"},
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_to("stress_result")

        if stress_class in ["Very Low", "Low"]:
            play_sound_automatic(HAPPY_SOUND_URL)
        else:
            play_sound_automatic(DISAPPOINTING_SOUND_URL)

# Performance Level Section
st.markdown("---")
st.markdown("## 🚀 Performance Level Questions (6-11)")
performance_answers = []
for i, q in enumerate(performance_questions):
    ans = st.radio(q, options, key=f"perf_q{i+6}", horizontal=True, index=None)
    performance_answers.append(ans)
performance_assess = st.button("Assess Performance Level")

if performance_assess:
    if None in performance_answers:
        st.warning("Please answer all Performance Level questions before assessing.")
    else:
        scores = [option_to_score(a) for a in performance_answers]
        mean_perf = sum(scores) / len(scores)
        perf_class = classify_performance_level(mean_perf)

        st.markdown('<div id="perf_result" class="result-box">', unsafe_allow_html=True)
        st.subheader(f"Performance Level: {perf_class} (Mean: {mean_perf:.2f})")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=mean_perf,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Performance Meter"},
            gauge={
                'axis': {'range': [1, 5]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [1, 1.5], 'color': "#b3ffd9"},
                    {'range': [1.5, 2], 'color': "#cce5ff"},
                    {'range': [2, 3], 'color': "#fffcb3"},
                    {'range': [3, 4], 'color': "#ffd6b3"},
                    {'range': [4, 5], 'color': "#ffb3b3"},
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        scroll_to("perf_result")

        # Reverse logic for performance sounds
        if perf_class in ["Very High", "High"]:
            play_sound_automatic(HAPPY_SOUND_URL)
        else:
            play_sound_automatic(DISAPPOINTING_SOUND_URL)
