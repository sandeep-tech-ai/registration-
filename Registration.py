import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# Simplified AP Data (Add more mandals as needed)
AP_DATA = {
    "Visakhapatnam": ["Gajuwaka", "Pedagantyada", "Maharani Peta", "Mulagada"],
    "NTR (Vijayawada)": ["Vijayawada Urban", "Vijayawada Rural", "Ibrahimpatnam", "Jaggayyapeta"],
    "Guntur": ["Guntur City", "Tenali", "Ponnur", "Mangalagiri"],
    "Tirupati": ["Tirupati Urban", "Tirupati Rural", "Chandragiri", "Srikalahasti"],
    "East Godavari": ["Rajahmundry", "Kadiam", "Kovvur"]
}

def show_registration():
    st.subheader("New Patient Entry")
    reg_file = "patient_registrations.csv"
    df = pd.read_csv(reg_file)

    # 1. Aadhar Search for Autofill
    with st.container(border=True):
        col_search, _ = st.columns([2, 2])
        search_aadhar = col_search.text_input("🔍 Search Aadhar Number for Auto-fill", help="Enter 12 digits")
        
        found_data = None
        if len(search_aadhar) == 12:
            match = df[df["Aadhar Number"].astype(str) == search_aadhar]
            if not match.empty:
                found_data = match.iloc[-1]
                st.success("Record found! Details auto-filled below.")

    # 2. Registration Form
    with st.form("reg_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            # MANUAL PATIENT ID Entry
            p_id = st.text_input("Patient ID *", value=found_data["Patient ID"] if found_data is not None else "")
            p_name = st.text_input("Patient Name *", value=found_data["Patient Name"] if found_data is not None else "")
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"], 
                                  index=["Male", "Female", "Other"].index(found_data["Gender"]) if found_data is not None else 0)
            
            # Handling Date of Birth conversion
            default_dob = date(2000, 1, 1)
            if found_data is not None:
                try:
                    default_dob = datetime.strptime(str(found_data["Date of Birth"]), "%Y-%m-%d").date()
                except: pass
            dob = st.date_input("Date of Birth", value=default_dob)

        with col2:
            phone = st.text_input("Phone Number *", value=found_data["Phone Number"] if found_data is not None else "")
            aadhar = st.text_input("Aadhar Number *", value=search_aadhar if search_aadhar else "")
            
            # District and Mandal Logic
            dist_list = list(AP_DATA.keys())
            dist_index = dist_list.index(found_data["District"]) if found_data is not None and found_data["District"] in dist_list else 0
            district = st.selectbox("District (Andhra Pradesh) *", dist_list, index=dist_index)
            
            mandal_list = AP_DATA.get(district, [])
            m_index = mandal_list.index(found_data["Mandal"]) if found_data is not None and found_data["Mandal"] in mandal_list else 0
            mandal = st.selectbox("Mandal *", mandal_list, index=m_index)

            reg_type = st.selectbox("Type of Registration *", ["New Patient", "Follow-up", "Emergency"])

        submitted = st.form_submit_button("✅ Save Registration", type="primary")

        if submitted:
            if not p_id or not p_name or not phone or not aadhar:
                st.error("Please fill all required fields (*)")
            else:
                new_row = {
                    "Patient ID": p_id,
                    "Patient Name": p_name.title(),
                    "Gender": gender,
                    "Date of Birth": dob,
                    "Phone Number": phone,
                    "Aadhar Number": aadhar,
                    "District": district,
                    "Mandal": mandal,
                    "Type of Registration": reg_type,
                    "Date of Registration": date.today(),
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Append data
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(reg_file, index=False)
                st.success(f"Registered {p_name} (ID: {p_id})")
                st.balloons()