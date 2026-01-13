# 🌍 EcoChain AI: Supply Chain Carbon Calculator

![Status](https://img.shields.io/badge/Status-Success-green?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Google_Gemini-8E75B2?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-Streamlit_FastAPI-blue?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Climate_Tech-00C853?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-FBC02D?style=for-the-badge)

**EcoChain AI** is an intelligent logistics tool that helps companies automate carbon footprint analysis. It replaces manual spreadsheet work by using **AI** to read PDF invoices and **Geospatial Engines** to calculate precise shipment routes.

---

## 🚀 Key Features

* **📄 AI Invoice Extraction:** Uses **Google Gemini 1.5** to extract Origin, Destination, Weight, and Mode from raw PDF files.
* **🗺️ Smart Routing Logic:**
    * **Trucks:** Queries **OSRM (Open Source Routing Machine)** for real road distances.
    * **Planes/Ships:** Calculates **Geodesic (Great Circle)** distance for air/sea routes.
* **📊 Live Visualization:** Displays the shipment route on an interactive map.
* **🌱 ISO-Compliant Math:** Calculates CO2e emissions using mode-specific emission factors.

---

## 🛠️ Technology Stack

* **Frontend:** Streamlit (Python)
* **Backend:** FastAPI
* **AI Model:** Google Gemini 1.5 Flash
* **Mapping:** Geopy, OSRM API, Pandas
* **Deployment:** Localhost

---

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/onkaryadav2541/EcoChain_AI.git](https://github.com/onkaryadav2541/EcoChain_AI.git)
    cd EcoChain_AI
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Backend (Terminal 1)**
    ```bash
    uvicorn main:app --reload
    ```

4.  **Run the Frontend (Terminal 2)**
    ```bash
    streamlit run app.py
    ```

---

## 📸 How It Works
1.  **Upload:** User drags & drops a logistics invoice (PDF).
2.  **Analyze:** AI extracts the city names and weight.
3.  **Route:** The app calculates the exact km (Road vs Air) and shows it on a map.
4.  **Result:** The precise Carbon Footprint (kg CO2) is displayed.

---
**Author:** Onkar | *Built during the 10-Day AI Engineer Challenge*