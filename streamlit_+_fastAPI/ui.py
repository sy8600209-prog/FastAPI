import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"   # AWS par deploy ho to yahan public URL/domain daalna

st.title("Patient Management")

tab1, tab2, tab3 = st.tabs(["All Patients", "Search by ID", "Add Patient"])

# ---------- Tab 1: saare patients ----------
with tab1:
    if st.button("Load patients"):
        try:
            res = requests.get(f"{API_URL}/patients")
            data = res.json()
            rows = [{"id": pid, **info} for pid, info in data.items()]
            st.dataframe(rows)
        except requests.exceptions.ConnectionError:
            st.error("FastAPI server band hai. Pehle uvicorn chalao.")

# ---------- Tab 2: ek patient ----------
with tab2:
    pid = st.text_input("Patient ID (jaise P001)")
    if st.button("Search"):
        try:
            res = requests.get(f"{API_URL}/patients/{pid}")
            if res.status_code == 200:
                st.json(res.json())
            else:
                st.warning(res.json()["detail"])
        except requests.exceptions.ConnectionError:
            st.error("FastAPI server band hai. Pehle uvicorn chalao.")

# ---------- Tab 3: naya patient ----------
with tab3:
    new_id = st.text_input("ID", placeholder="P006")
    name = st.text_input("Name")
    city = st.text_input("City")
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["male", "female", "other"])
    height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, value=1.70)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0)

    if st.button("Add patient"):
        payload = {
            "id": new_id,
            "name": name,
            "city": city,
            "age": int(age),
            "gender": gender,
            "height": height,
            "weight": weight,
        }
        try:
            res = requests.post(f"{API_URL}/patients", json=payload)
            if res.status_code == 200:
                st.success(res.json())
            else:
                st.error(res.json()["detail"])
        except requests.exceptions.ConnectionError:
            st.error("FastAPI server band hai. Pehle uvicorn chalao.")