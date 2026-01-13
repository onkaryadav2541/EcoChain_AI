import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="EcoChain AI", page_icon="🌍")
st.title("🌍 EcoChain AI: Supply Chain Carbon Calculator")

# 2. Sidebar for API Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", "http://127.0.0.1:8000")
    st.info("Ensure your FastAPI backend is running!")

# 3. Main Input Section
tab1, tab2 = st.tabs(["📝 Manual Input", "📄 Upload Invoice (AI)"])

with tab1:
    st.subheader("Calculate Single Shipment")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, value=1000.0)
    with col2:
        dist = st.number_input("Distance (km)", min_value=1.0, value=500.0)
    with col3:
        mode = st.selectbox("Transport Mode", ["truck", "train", "ship", "plane"])
        
    if st.button("Calculate CO2", type="primary"):
        payload = {"weight_kg": weight, "distance_km": dist, "mode": mode}
        try:
            response = requests.post(f"{api_url}/calculate", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"🌱 Carbon Footprint: {result['co2_kg']} kg CO2")
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

with tab2:
    st.subheader("AI Invoice Extractor (Coming Soon)")
    st.write("This module will automatically read PDFs using the OpenAI service we built on Day 6.")