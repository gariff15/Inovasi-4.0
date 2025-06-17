import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html

# Inject Lottie player script once
st.components.v1.html("""
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
""", height=0)

# CSS styling to reduce gap
st.markdown("""
    <style>
    .result-box {
        background: #f0f4ff;
        border-radius: 12px;
        padding: 1.5em 1em 0.5em 1em;
        margin-top: 1em;
        box-shadow: 0 2px 8px rgba(79, 139, 249, 0.15);
        text-align: center;
    }
    .animation-container {
        margin-top: -10px;
        margin-bottom: 0.5em;
        text-align: center;
    }
    .balloon-container {
        margin-top: -40px;
        margin-bottom: 0.5em;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def show_animation(animation_key, celebration=False):
    animations = {
        "perf_high": "https://assets3.lottiefiles.com/packages/lf20_touohxv0.json",   # Party/confetti
        "perf_low": "https://assets3.lottiefiles.com/packages/lf20_4kx2q32n.json",    # Sad gloomy
    }
    balloon = "https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"  # Balloon
    clap = "https://assets8.lottiefiles.com/packages/lf20_3rwasyjy.json"      # Clap

    url = animations.get(animation_key)
    if url:
        html(f"""
        <div class="animation-container">
            <lottie-player src="{url}" background="transparent" speed="1" style="width: 220px; height: 220px;" loop autoplay></lottie-player>
        </div>
        """, height=230)
    if celebration:
        # Add balloons and clap for celebration
        html(f"""
        <div class="balloon-container">
            <lottie-player src="{balloon}" background="transparent" speed="1" style="width: 120px; height: 120px;" loop autoplay></lottie-player>
            <lottie-player src="{clap}" background="transparent" speed="1" style="width: 120px; height: 120px;" loop autoplay></lottie-player>
        </div>
        """, height=130)

# Example for performance section
st.header("🚀 Performance Level Example")
mean_perf = 4.2  # Example value
perf_class = "Low"  # Example class

st.markdown('<div class="result-box">', unsafe_allow_html=True)
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

# Show animation right after the gauge, with minimal gap
if perf_class in ["Very High", "High"]:
    show_animation("perf_high", celebration=True)
    st.markdown("### 🎉 Excellent performance! Keep shining!")
else:
    show_animation("perf_low")
    st.markdown("### 😞 Performance is low. Don't give up!")
