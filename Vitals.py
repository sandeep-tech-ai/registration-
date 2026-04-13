import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_vitals():
    reg_file = "patient_registrations.csv"
    vit_file = "vitals.csv"

    if not os.path.exists(reg_file):
        st.warning("No data found.")
        return

    df_patients = pd.read_csv(reg_file)

    st.subheader("Enter Vitals")
    
    # Patient Selection via ID Search (Removed the list view)
    col_search, _ = st.columns([2, 2])
    search_id = col_search.text_input("Enter Patient ID or Aadhar Number to begin")
    
    target_patient = None
    if search_id:
        # Search by ID or Aadhar
        match = df_patients[(df_patients["Patient ID"] == search_id) | 
                            (df_patients["Aadhar Number"].astype(str) == search_id)]
        if not match.empty:
            target_patient = match.iloc[-1]
            st.info(f"Adding vitals for: **{target_patient['Patient Name']}**")
        else:
            st.error("Patient not found. Please register them first.")

    if target_patient is not None:
        with st.form("vitals_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                bp = st.text_input("Blood Pressure (mmHg)")
                pulse = st.number_input("Pulse Rate (bpm)", 0, 250)
                temp = st.number_input("Temp (°C)", 0.0, 50.0)
            with c2:
                spo2 = st.number_input("SpO2 (%)", 0, 100)
                weight = st.number_input("Weight (kg)", 0.0, 300.0)
                height = st.number_input("Height (cm)", 0.0, 250.0)
            
            notes = st.text_area("Observations")
            
            if st.form_submit_button("💾 Save Vitals"):
                new_vital = {
                    "Patient ID": target_patient["Patient ID"],
                    "Patient Name": target_patient["Patient Name"],
                    "Date Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Blood Pressure": bp, "Pulse": pulse, "Temperature": temp,
                    "SpO2": spo2, "Weight": weight, "Height": height, "Notes": notes
                }
                
                if os.path.exists(vit_file):
                    df_v = pd.read_csv(vit_file)
                    df_v = pd.concat([df_v, pd.DataFrame([new_vital])], ignore_index=True)
                else:
                    df_v = pd.DataFrame([new_vital])
                
                df_v.to_csv(vit_file, index=False)
                st.success("Vitals saved!")
                st.rerun()

    # History Table at bottom
    st.divider()
    if os.path.exists(vit_file):
        st.subheader("Recent Vitals Records")
        st.dataframe(pd.read_csv(vit_file).iloc[::-1], use_container_width=True, hide_index=True)