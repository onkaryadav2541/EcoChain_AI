import streamlit as st
import requests
import tempfile
import os
from services.ai_extractor import extract_logistics_data
from utils import extract_text_from_pdf

# --- NEW: INTERNAL DISTANCE DATABASE ---
def get_estimated_distance(origin, destination):
    # A simple database of distances between common German cities (in km)
    # real road distances approx.
    routes = {
        ("berlin", "munich"): 585,
        ("munich", "berlin"): 585,
        ("berlin", "hamburg"): 289,
        ("hamburg", "berlin"): 289,
        ("munich", "hamburg"): 775,
        ("hamburg", "munich"): 775,
        ("cologne", "berlin"): 575,
        ("berlin", "cologne"): 575,
        ("frankfurt", "munich"): 393,
        ("munich", "frankfurt"): 393
    }
    
    # Normalize text (lowercase, strip spaces) to match our database
    o = origin.lower().strip()
    d = destination.lower().strip()
    
    return routes.get((o, d))

# ---------------------------------------

# 1. Page Configuration
st.set_page_config(page_title="EcoChain AI", page_icon="🌍")
st.title("🌍 EcoChain AI: Supply Chain Carbon Calculator")

# 2. Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", "http://127.0.0.1:8000")
    st.info("Ensure your FastAPI backend is running!")

# 3. Main Tabs
tab1, tab2 = st.tabs(["📝 Manual Input", "📄 Upload Invoice (AI)"])

# --- TAB 1: Manual Calculation ---
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

# --- TAB 2: AI Invoice Extractor ---
with tab2:
    st.subheader("AI Invoice Extractor")
    uploaded_file = st.file_uploader("Upload Logistics Invoice (PDF)", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Analyze Invoice"):
            with st.spinner("🤖 AI is reading your invoice..."):
                try:
                    # 1. Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # 2. Extract Text
                    text_content = extract_text_from_pdf(tmp_path)
                    
                    # 3. Send to AI
                    ai_data = extract_logistics_data(text_content)
                    
                    if ai_data:
                        st.subheader("1. Extracted Data")
                        st.json(ai_data)
                        
                        # --- SMART LOGIC STARTS HERE ---
                        weight = ai_data.get("weight_kg", 0)
                        distance = ai_data.get("distance_km", 0)
                        origin = ai_data.get("origin", "")
                        destination = ai_data.get("destination", "")
                        mode = ai_data.get("transport_mode", "truck").lower()

                        # If AI missed the distance, we calculate it automatically
                        if distance == 0 and origin and destination:
                            calculated_dist = get_estimated_distance(origin, destination)
                            if calculated_dist:
                                distance = calculated_dist
                                st.info(f"📍 AI Auto-Detected Route: {origin} ➝ {destination} ({distance} km)")
                            else:
                                distance = 500 # Only use default if city is unknown
                                st.warning("⚠️ Route unknown. Using default: 500 km")
                        
                        # Prepare data for backend
                        payload = {
                            "weight_kg": weight,
                            "distance_km": distance,
                            "mode": mode
                        }
                        
                        try:
                            # 4. Calculate Emissions
                            response = requests.post(f"{api_url}/calculate", json=payload)
                            
                            if response.status_code == 200:
                                result = response.json()
                                co2 = result['co2_kg']
                                
                                # SUCCESS
                                st.success(f"🌱 Calculated Carbon Footprint: {co2} kg CO2")
                                st.balloons()
                            else:
                                st.warning("Could not calculate CO2.")
                                st.write(response.text)
                                
                        except Exception as e:
                            st.error(f"Backend Connection Failed: {e}")
                    
                    else:
                        st.error("AI returned empty data.")

                    # Cleanup
                    os.unlink(tmp_path)

                except Exception as e:
                    st.error(f"An error occurred: {e}")