import streamlit as st
import plotly.graph_objects as go

# --- CSS for aesthetics ---
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

# --- Title and Description ---
st.title("🎯 Stresformance")
st.markdown("""
Welcome to **Stresformance**!  
Assess your stress levels and performance with our innovative, interactive tool.  
Answer the 11 questions below to get personalized feedback.
""")

# --- Questions and Options ---
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

# --- Helper Functions ---
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
        return "🟦 Very Low"
    elif 1.5 <= mean < 2:
        return "🟩 Low"
    elif 2 <= mean < 3:
        return "🟨 Moderate"
    elif 3 <= mean < 4:
        return "🟧 High"
    else:  # mean >= 4
        return "🟥 Very High"

def classify_performance_level(mean):
    if mean < 1.5:
        return "🟩 Very High"
    elif 1.5 <= mean < 2:
        return "🟨 High"
    elif 2 <= mean < 3:
        return "🟧 Moderate"
    elif 3 <= mean < 4:
        return "🟥 Low"
    else:  # mean >= 4
        return "⬛ Very Low"

# --- User Input ---
responses = []
with st.form("stress_form"):
    st.markdown("## 😰 Stress Level Questions (1-5)")
    for i, q in enumerate(stress_questions):
        selected = st.radio(q, options, key=f"q{i+1}", horizontal=True)
        responses.append(selected)
    st.markdown("---")
    st.markdown("## 🚀 Performance Level Questions (6-11)")
    for i, q in enumerate(performance_questions):
        selected = st.radio(q, options, key=f"q{i+6}", horizontal=True)
        responses.append(selected)
    submitted = st.form_submit_button("✨ Finish")

# --- Results ---
if submitted:
    scores = [option_to_score(ans) for ans in responses]
    mean_1_5 = sum(scores[:5]) / 5
    mean_6_11 = sum(scores[5:]) / 6

    result_1_5 = classify_stress_level(mean_1_5)
    result_6_11 = classify_performance_level(mean_6_11)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("🔎 Results")
    st.write(f"**😰 Stress Level (Q1–Q5):** {result_1_5}  \nMean score: {mean_1_5:.2f}")
    st.write(f"**🚀 Performance Level (Q6–Q11):** {result_6_11}  \nMean score: {mean_6_11:.2f}")

    # Gauge chart for Stress Level
    fig_stress = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = mean_1_5,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Stress Level"},
        gauge = {
            'axis': {'range': [1, 5]},
            'bar': {'color': "royalblue"},
            'steps' : [
                {'range': [1, 1.5], 'color': "#cce5ff"},
                {'range': [1.5, 2], 'color': "#b3ffd9"},
                {'range': [2, 3], 'color': "#fffcb3"},
                {'range': [3, 4], 'color': "#ffd6b3"},
                {'range': [4, 5], 'color': "#ffb3b3"}
            ]
        }
    ))
    st.plotly_chart(fig_stress, use_container_width=True)

    # Gauge chart for Performance Level
    fig_perf = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = mean_6_11,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Performance Level"},
        gauge = {
            'axis': {'range': [1, 5]},
            'bar': {'color': "green"},
            'steps' : [
                {'range': [1, 1.5], 'color': "#b3ffd9"},
                {'range': [1.5, 2], 'color': "#cce5ff"},
                {'range': [2, 3], 'color': "#fffcb3"},
                {'range': [3, 4], 'color': "#ffd6b3"},
                {'range': [4, 5], 'color': "#ffb3b3"}
            ]
        }
    ))
    st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.balloons()
else:
    st.info("Answer all questions above and click **Finish** to see your results!")

# --- Footer ---
st.markdown("""
---
<small>
Made with ❤️ for innovation and well-being.
</small>
""", unsafe_allow_html=True)
