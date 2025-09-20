import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="🏥 Patient Info Finder", layout="centered")
st.markdown("<h1 style='text-align: center;'>🏥 Hospital Patient Record Lookup System</h1>", unsafe_allow_html=True)
st.caption("🔍 Search for patient records using Patient ID")

# --- Dummy Patient Data ---
if "patient_data" not in st.session_state:
    st.session_state.patient_data = pd.DataFrame({
        "PatientID": ["P1001", "P1002", "P1003", "P1004", "P1005"],
        "Name": ["Amit Kumar", "Sneha Patel", "Rahul Singh", "Meena Gupta", "Tanzil Raza"],
        "Age": [25, 32, 45, 29, 36],
        "Disease": ["Typhoid", "Fracture", "Diabetes", "Migraine", "Covid-19"],
        "Doctor": ["Dr. Reddy", "Dr. Sen", "Dr. Mehta", "Dr. Bose", "Dr. Khanna"],
        "Room": ["202A", "105B", "303C", "210A", "Isolation-1"],
        "Status": ["Admitted", "Discharged", "Admitted", "Admitted", "Discharged"]
    })

# --- Search History States ---
if "search_history" not in st.session_state:
    st.session_state.search_history = []

if "search_log" not in st.session_state:
    st.session_state.search_log = []

data = st.session_state.patient_data

# --- Patient Search Section ---
st.markdown("### 🔍 Search Patient Record by ID")
patient_input = st.text_input("🔑 Enter Patient ID (e.g., P1001):").upper().strip()

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔎 Find"):
        if patient_input == "":
            st.warning("⚠️ Please enter a valid Patient ID.")
        else:
            result = data[data["PatientID"] == patient_input]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.search_history.append(patient_input)
            st.session_state.search_log.append({
                "PatientID": patient_input,
                "Timestamp": timestamp
            })

            if not result.empty:
                patient = result.iloc[0]
                st.success("✅ Record Found!")
                st.markdown(f"""
                    <div style="background-color: #e8f5e9; padding: 15px; border-left: 5px solid green; border-radius: 10px;">
                    <h4>👤 Name: <b>{patient['Name']}</b></h4>
                    <p>🆔 Patient ID: {patient['PatientID']}</p>
                    <p>🎂 Age: {patient['Age']}</p>
                    <p>🩺 Disease: {patient['Disease']}</p>
                    <p>👨‍⚕️ Doctor: {patient['Doctor']}</p>
                    <p>🏨 Room No: {patient['Room']}</p>
                    <p>📌 Status: <b>{patient['Status']}</b></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ No record found for this Patient ID.")

# --- Admin Add New Patient Section ---
st.markdown("---")
st.markdown("### 🛠️ Admin Panel – Add New Patient")
with st.form("admin_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_id = st.text_input("🆔 Patient ID").upper().strip()
        new_name = st.text_input("👤 Name")
        new_age = st.number_input("🎂 Age", min_value=0, max_value=120)
    with col2:
        new_disease = st.text_input("🩺 Disease")
        new_doctor = st.text_input("👨‍⚕️ Doctor Name")
        new_room = st.text_input("🏨 Room No.")
        new_status = st.selectbox("📌 Status", ["Admitted", "Discharged"])
    
    add_button = st.form_submit_button("➕ Add Patient")

    if add_button:
        if new_id == "" or new_name == "" or new_disease == "" or new_doctor == "" or new_room == "":
            st.warning("⚠️ Please fill all fields.")
        elif new_id in data["PatientID"].values:
            st.error("❌ Patient ID already exists.")
        else:
            new_entry = pd.DataFrame({
                "PatientID": [new_id],
                "Name": [new_name],
                "Age": [new_age],
                "Disease": [new_disease],
                "Doctor": [new_doctor],
                "Room": [new_room],
                "Status": [new_status]
            })
            st.session_state.patient_data = pd.concat([data, new_entry], ignore_index=True)
            st.success(f"✅ New record added for {new_name}")

# --- View Data ---
st.markdown("---")
with st.expander("📋 View Full Patient Data"):
    st.dataframe(st.session_state.patient_data, use_container_width=True)

# --- Download CSV ---
st.markdown("### 📥 Download Patient Records")
csv = st.session_state.patient_data.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download as CSV", data=csv, file_name="patient_records.csv", mime="text/csv")

# --- Search History Section ---
if st.session_state.search_history:
    st.markdown("### 🕘 Search History")
    st.write(pd.DataFrame(st.session_state.search_history, columns=["Searched Patient IDs"]))
    if st.button("🧹 Clear History"):
        st.session_state.search_history = []
        st.success("🧼 History cleared.")

# --- Search Log (Timestamped) ---
if st.session_state.search_log:
    st.markdown("### 📅 Search Log (With Timestamp)")
    log_df = pd.DataFrame(st.session_state.search_log)
    st.dataframe(log_df, use_container_width=True)
    if st.button("🧼 Clear Log"):
        st.session_state.search_log = []
        st.success("🧼 Log cleared.")

# --- Live Stats Section ---
st.markdown("---")
st.markdown("### 📊 Live Dashboard")
total = len(st.session_state.patient_data)
admitted = (st.session_state.patient_data["Status"] == "Admitted").sum()
discharged = total - admitted
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Patients", total)
col2.metric("🏨 Admitted", admitted)
col3.metric("✅ Discharged", discharged)
