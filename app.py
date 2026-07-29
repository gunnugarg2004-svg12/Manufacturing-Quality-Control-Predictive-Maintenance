import streamlit as st
import pandas as pd
import joblib


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Manufacturing Predictive Maintenance",
    page_icon="🏭",
    layout="wide"
)

st.markdown("""
<style>

/* Hide + and - buttons of number input */

button[title="Increment"]{
    display:none;
}

button[title="Decrement"]{
    display:none;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# Load Model
# =====================================================

model = joblib.load("Models/random_forest.pkl")

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("🏭 Manufacturing AI")

st.sidebar.markdown("---")

st.sidebar.subheader("Project Overview")

st.sidebar.info("""
Predictive Maintenance System

Predict whether a machine is likely to fail within the next 7 days using a trained Random Forest Machine Learning model.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("Machine Learning Model")

st.sidebar.success("Random Forest Classifier")

st.sidebar.markdown("---")

st.sidebar.subheader("Input Features")

st.sidebar.write("""
• Temperature

• Vibration

• Pressure

• Oil Level

• Voltage

• Current

• RPM

• Sound Level

• Machine Health Score
""")

st.sidebar.markdown("---")

st.sidebar.caption("Developed by Annu Garg")

# =====================================================
# Title
# =====================================================

st.title("🏭 Manufacturing Predictive Maintenance System")

st.markdown("""
Predict whether a machine is likely to fail within the next **7 days**
using a trained **Random Forest Machine Learning Model**.
""")

st.divider()

# =====================================================
# Input Section
# =====================================================

st.subheader("📊 Machine Sensor Readings")

col1, col2 = st.columns(2)

with col1:

    temperature = st.number_input(
        "🌡 Temperature (°C)",
        value=100.0,
        step=1.0,
        format="%.1f"
    )

    vibration = st.number_input(
        "📈 Vibration (mm/s)",
        value=3.0,
        step=1.0,
        format="%.1f"
    )

    pressure = st.number_input(
        "⚙ Pressure (bar)",
        value=6.0,
        step=1.0,
        format="%.1f"
    )

    oil_level = st.number_input(
        "🛢 Oil Level (%)",
        value=75.0,
        step=1.0,
        format="%.1f"
    )

    voltage = st.number_input(
        "⚡ Voltage (V)",
        value=415.0,
        step=1.0,
        format="%.1f"
    )

with col2:

    current = st.number_input(
        "🔌 Current (A)",
        value=40.0,
        step=1.0,
        format="%.1f"
    )

    rpm = st.number_input(
        "🔄 RPM",
        value=1400.0,
        step=50.0,
        format="%.1f"
    )

    sound = st.number_input(
        "🔊 Sound Level (dB)",
        value=70.0,
        step=1.0,
        format="%.1f"
    )

    health_score = st.number_input(
        "💚 Machine Health Score",
        value=85.0,
        step=1.0,
        format="%.1f"
    )

# =====================================================
# Prediction
# =====================================================
if st.button("🔍 Predict Machine Failure", use_container_width=True):

    # -----------------------------
    # Prepare Input
    # -----------------------------
    sample = pd.DataFrame({
        "temperature_c": [temperature],
        "vibration_mm_s": [vibration],
        "pressure_bar": [pressure],
        "oil_level_percent": [oil_level],
        "voltage_v": [voltage],
        "current_amp": [current],
        "rpm": [rpm],
        "sound_level_db": [sound],
        "machine_health_score": [health_score]
    })

    prediction = model.predict(sample)[0]
    probabilities = model.predict_proba(sample)[0]

    failure_probability = probabilities[1]
    confidence = max(probabilities)

    risk = (
        "🔴 High" if failure_probability >= 0.70
        else "🟡 Medium" if failure_probability >= 0.30
        else "🟢 Low"
    )

    machine_status = (
        "⚠️ Failure Expected"
        if prediction == 1
        else "✅ Healthy"
    )

    # -----------------------------
    # Prediction Result
    # -----------------------------
    st.divider()

    st.subheader("🤖 Prediction Result")

    if prediction == 1:
        st.error("⚠️ Machine Failure Expected Within 7 Days")
    else:
        st.success("✅ Machine is Operating Normally")

    # -----------------------------
    # KPI Cards
    # -----------------------------
    st.subheader("📊 Prediction Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🤖 Status", machine_status)

    with c2:
        st.metric("🚨 Risk", risk)

    with c3:
        st.metric(
            "📈 Failure Probability",
            f"{failure_probability*100:.2f}%"
        )

    with c4:
        st.metric(
            "🎯 Confidence",
            f"{confidence*100:.2f}%"
        )

    # -----------------------------
    # Probability Chart
    # -----------------------------
    import plotly.express as px

    chart = pd.DataFrame({
        "Prediction": ["No Failure", "Failure"],
        "Probability": [
            probabilities[0]*100,
            probabilities[1]*100
        ]
    })

    fig = px.bar(
        chart,
        x="Prediction",
        y="Probability",
        text="Probability",
        title="Prediction Probability"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Sensor Summary
    # -----------------------------
    st.subheader("📋 Input Sensor Summary")

    summary = pd.DataFrame({
        "Sensor":[
            "Temperature",
            "Vibration",
            "Pressure",
            "Oil Level",
            "Voltage",
            "Current",
            "RPM",
            "Sound",
            "Health Score"
        ],
        "Value":[
            temperature,
            vibration,
            pressure,
            oil_level,
            voltage,
            current,
            rpm,
            sound,
            health_score
        ]
    })

    st.dataframe(
        summary,
        hide_index=True,
        use_container_width=True
    )

    # -----------------------------
    # Maintenance Recommendation
    # -----------------------------
    st.subheader("🛠 Maintenance Recommendation")

    if failure_probability >= 0.70:

        st.warning("""
- Inspect machine immediately.
- Check lubrication.
- Check vibration.
- Schedule preventive maintenance.
- Monitor continuously.
""")

    elif failure_probability >= 0.30:

        st.info("""
- Monitor machine closely.
- Schedule inspection.
- Review sensor readings.
""")

    else:

        st.success("""
- Machine is operating normally.
- Continue routine maintenance.
""")

    # -----------------------------
    # Prediction Details
    # -----------------------------
    from datetime import datetime

    prediction_time = datetime.now()

    st.subheader("🕒 Prediction Details")

    st.info(
        f"""
Prediction Date : {prediction_time.strftime("%d %B %Y")}

Prediction Time : {prediction_time.strftime("%I:%M:%S %p")}
"""
    )

    # -----------------------------
    # Download Report
    # -----------------------------
    report = pd.DataFrame({
        "Machine Status":[machine_status],
        "Risk Level":[risk],
        "Failure Probability (%)":[round(failure_probability*100,2)],
        "Confidence (%)":[round(confidence*100,2)]
    })

    st.download_button(
        "⬇ Download Prediction Report",
        report.to_csv(index=False),
        "prediction_report.csv",
        "text/csv",
        use_container_width=True
    )

    #---------------------
    # Footer 
    #---------------------

    st.divider()

st.markdown(
    """
<div style="text-align:center; color:gray; font-size:15px;">

🏭 <b>Manufacturing Predictive Maintenance System</b><br>

🤖 Machine Learning Model: <b>Random Forest Classifier</b><br>

Developed by <b>Annu Garg</b> | © 2026

</div>
""",
    unsafe_allow_html=True
)