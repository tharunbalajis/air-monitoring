import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="Air Audit Monitoring System",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# HEADER AND LOGO
# -----------------------------
col1, col2 = st.columns([1,5])

with col1:
    try:
        logo = Image.open("assets/logo.png")
        st.image(logo, width=120)
    except FileNotFoundError:
        st.warning("Logo file not found! Please place `logo.png` inside the `assets/` folder.")

with col2:
    st.title("💨 Air Audit Monitoring System")
    st.markdown("""
    **Developed by:** SHRIRAM H  
    **Company:** ELGi Equipments Ltd  
    **Objective:** Detect air pressure loss between delivery and application to identify possible leakages.
    """)

st.markdown("---")

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    df = pd.read_csv("data/air_pressure_data.csv")
except FileNotFoundError:
    st.error("❌ Dataset not found! Please place `air_pressure_data.csv` inside the `data/` folder.")
    st.stop()

# -----------------------------
# DATA PREPARATION
# -----------------------------
df["Pressure Difference (bar)"] = df["Inlet Pressure (bar)"] - df["Outlet Pressure (bar)"]
df["Status"] = df["Pressure Difference (bar)"].apply(
    lambda x: "✅ Normal Flow" if x < 0.2 else ("⚠️ Slight Loss" if x < 0.5 else "❌ Possible Leak")
)

# -----------------------------
# DISPLAY DATA
# -----------------------------
st.subheader("📊 Pressure Data Overview")
st.dataframe(df, use_container_width=True)

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📈 Pressure Trends")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df["Timestamp"], df["Inlet Pressure (bar)"], label="Inlet Pressure", marker="o", color='green')
ax.plot(df["Timestamp"], df["Outlet Pressure (bar)"], label="Outlet Pressure", marker="s", color='red')
ax.set_xlabel("Time")
ax.set_ylabel("Pressure (bar)")
ax.set_title("Inlet vs Outlet Pressure Over Time")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# -----------------------------
# LEAK ANALYSIS SUMMARY
# -----------------------------
st.subheader("⚠️ Leak Detection Summary")
total_points = len(df)
normal = len(df[df["Status"] == "✅ Normal Flow"])
minor = len(df[df["Status"] == "⚠️ Slight Loss"])
major = len(df[df["Status"] == "❌ Possible Leak"])

col1, col2, col3 = st.columns(3)
col1.metric("✅ Normal Flow", normal)
col2.metric("⚠️ Slight Loss", minor)
col3.metric("❌ Major Leak", major)

# -----------------------------
# FILTER OPTION
# -----------------------------
st.subheader("🔍 Filter by Flow Condition")
selected_status = st.selectbox("Choose a flow condition:", df["Status"].unique())
filtered = df[df["Status"] == selected_status]
st.dataframe(filtered, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("**Project Summary:** This system continuously monitors inlet and outlet air pressure, detects abnormal pressure drops, and helps identify possible leaks in pneumatic systems.")
st.caption("© 2025 SHRIRAM H | ELGi Internship Project")
