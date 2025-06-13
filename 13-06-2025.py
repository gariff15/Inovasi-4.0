import streamlit as st

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
Answer the 8 questions below to get personalized feedback.
""")

# --- Questions and Options ---
questions = [
    "1. In the last 1- 4 weeks, I found it hard to wind down.",
    "2. In the last 1- 4 weeks, I tended to over-react to situations.",
    "3. In the last 1- 4 weeks, I felt restless.",
    "4. In the last 1- 4 weeks, I felt easily agitated.",
    "5. In the last 1-4 weeks, I felt difficult to relax.",
    "6. During the past 1 - 4 weeks, How often did you find yourself not working carefully as you should?",
    "7. During the past 1 - 4 weeks, how often was the quality of your work lower than it should be?",
    "8. During the past 1 - 4 weeks, how often do you not fully concentrate on your work?"
]

options = ["Very Rare", "Rare", "Moderate", "Frequent", "Very Frequent"]

# --- User Input ---
responses = []
with st.form("stress_form"):
    for i, q in enumerate(questions):
        selected = st.radio(q, options, key=f"q{i+1}", horizontal=True)
        responses.append(selected)
    submitted = st.form_submit_button("✨ Finish")

# --- Helper Functions ---
def option_to_score(option):
    return {
        "Very Rare": 1,
        "Rare": 2,
        "Moderate": 3,
        "Frequent": 4,
        "Very Frequent": 5
    }[option]

def classify(mean):
    if mean < 1.5:
        return "🟦 Very Low"
    elif 1.5 <= mean < 2.5:
        return "🟩 Low"
    elif 2.5 <= mean < 3:
        return "🟨 Moderate"
    elif 3 <= mean <= 4:
        return "🟧 High"
    else:  # mean > 4
        return "🟥 Very High"

# --- Results ---
if submitted:
    scores = [option_to_score(ans) for ans in responses]
    mean_1_5 = sum(scores[:5]) / 5
    mean_6_8 = sum(scores[5:]) / 3

    result_1_5 = classify(mean_1_5)
    result_6_8 = classify(mean_6_8)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("🔎 Results")
    st.write(f"**Stress Level (Q1–Q5):** {result_1_5}  \nMean score: {mean_1_5:.2f}")
    st.write(f"**Performance & Well-being (Q6–Q8):** {result_6_8}  \nMean score: {mean_6_8:.2f}")

    # Add a gauge chart for extra flair
    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = mean_1_5,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Stress Level"},
        gauge = {
            'axis': {'range': [1, 5]},
            'bar': {'color': "royalblue"},
            'steps' : [
                {'range': [1, 1.5], 'color': "#cce5ff"},
                {'range': [1.5, 2.5], 'color': "#b3ffd9"},
                {'range': [2.5, 3], 'color': "#fffcb3"},
                {'range': [3, 4], 'color': "#ffd6b3"},
                {'range': [4, 5], 'color': "#ffb3b3"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

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
