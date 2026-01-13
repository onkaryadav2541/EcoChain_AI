import streamlit as st
import requests
import tempfile
import os
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from services.ai_extractor import extract_logistics_data
from utils import extract_text_from_pdf

# --- 🌍 NEW: LIVE DISTANCE ENGINE ---
def get_coordinates(city_name):
    """Convert 'Berlin' to (52.52, 13.40)"""
    # We identify ourselves to the map service
    geolocator = Nominatim(user_agent="ecochain_student_project_v1")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        return None
    except:
        return None

def get_real_distance(origin, destination, mode):
    """Decides between Road (Truck) or Air (Plane) logic"""
    
    # 1. Get Coordinates
    coords_1 = get_coordinates(origin)
    coords_2 = get_coordinates(destination)
    
    if not coords_1 or not coords_2:
        return 0, None, None

    # 2. CHOICE A: TRUCK (Follow the Roads)
    if mode.lower() == "truck":
        # Ask OpenStreetMap for driving distance
        url = f"http://router.project-osrm.org/route/v1/driving/{coords_1[1]},{coords_1[0]};{coords_2[1]},{coords_2[0]}?overview=false"
        try:
            r = requests.get(url)
            data = r.json()
            if data.get("code") == "Ok":
                # Convert meters to km
                distance_km = data["routes"][0]["distance"] / 1000
                return round(distance_km, 2), coords_1, coords_2
        except:
            pass # If road server fails, fallback to direct line

    # 3. CHOICE B: PLANE / SHIP (Direct Math)
    direct_distance = geodesic(coords_1, coords_2).kilometers
    
    if mode.lower() == "ship":
        # Add 20% for water routes
        return round(direct_distance * 1.2, 2), coords_1, coords_2 
    
    return round(direct_distance, 2), coords_1, coords_2

# ---------------------------------------

st.set_page_config(page_title="EcoChain AI", page_icon="🌍")
st.title("🌍 EcoChain AI: Supply Chain Carbon Calculator")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", " https://ecochain-backend-api.onrender.com")
    st.info("Ensure FastAPI is running!")

tab1, tab2 = st.tabs(["📝 Manual Input", "📄 Upload Invoice (AI)"])

# --- Tab 1: Manual ---
with tab1:
    st.subheader("Calculate Single Shipment")
    w = st.number_input("Weight (kg)", 1000)
    d = st.number_input("Distance (km)", 500)
    m = st.selectbox("Mode", ["truck", "train", "ship", "plane"])
    if st.button("Calculate CO2"):
        try:
            res = requests.post(f"{api_url}/calculate", json={"weight_kg": w, "distance_km": d, "mode": m})
            if res.status_code == 200:
                st.success(f"🌱 Emission: {res.json()['co2_kg']} kg CO2")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Tab 2: AI + MAPS ---
with tab2:
    st.subheader("AI Invoice Extractor")
    uploaded_file = st.file_uploader("Upload Invoice (PDF)", type="pdf")
    
    if uploaded_file and st.button("Analyze Invoice"):
        with st.spinner("🤖 AI reading & Map calculating..."):
            try:
                # 1. File Handling
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                # 2. AI Extraction
                text = extract_text_from_pdf(tmp_path)
                data = extract_logistics_data(text)
                
                if data:
                    st.subheader("1. AI Extraction")
                    st.json(data)
                    
                    # 3. LIVE MAP CALCULATION
                    origin = data.get("origin", "")
                    dest = data.get("destination", "")
                    mode = data.get("transport_mode", "truck").lower()
                    
                    dist = 0
                    if origin and dest:
                        dist, c1, c2 = get_real_distance(origin, dest, mode)
                        
                        if dist > 0:
                            st.info(f"📍 Route: {origin} ➝ {dest}")
                            st.metric("Real Distance", f"{dist} km")
                            
                            # SHOW THE MAP
                            if c1 and c2:
                                map_df = pd.DataFrame([c1, c2], columns=['lat', 'lon'])
                                st.map(map_df)
                        else:
                            dist = 500 # Default fallback
                            st.warning("⚠️ Could not find route. Using 500km.")

                    # 4. Final Calculation
                    payload = {
                        "weight_kg": data.get("weight_kg", 0), 
                        "distance_km": dist, 
                        "mode": mode
                    }
                    
                    res = requests.post(f"{api_url}/calculate", json=payload)
                    if res.status_code == 200:
                        st.success(f"🌱 Calculated Carbon Footprint: {res.json()['co2_kg']} kg CO2")
                        st.balloons()
                    
                os.unlink(tmp_path)
            except Exception as e:
                st.error(f"Error: {e}")