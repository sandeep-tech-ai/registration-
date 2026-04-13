import streamlit as st
import pandas as pd
from datetime import date, datetime

# ====================== CONFIG ======================
st.set_page_config(
    page_title="Patient Registration Form",
    page_icon="🏥",
    layout="wide"
)

DATA_FILE = "patient_registrations.csv"

# Load or create data
if "df" not in st.session_state:
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "S.No.", "Patient Name", "Gender", "Date of Birth",
            "Phone Number", "Aadhar Number", "Type of Registration",
            "Date of Registration", "Timestamp"
        ])
    st.session_state.df = df

# ====================== TITLE ======================
st.title("🏥 Patient Registration System")
st.markdown("### Simple & Clean Registration Form (Built with Streamlit + Python)")

# ====================== REGISTRATION FORM ======================
with st.form("registration_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name *", placeholder="Enter full name")
        gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth", value=date(2000, 1, 1))

    with col2:
        phone = st.text_input("Phone Number *", placeholder="10-digit mobile number")
        aadhar = st.text_input("Aadhar Number", placeholder="12-digit Aadhar number")
        reg_type = st.selectbox(
            "Type of Registration *",
            ["New Patient", "Follow-up", "Emergency", "Referral", "Insurance"]
        )

    reg_date = st.date_input("Date of Registration", value=date.today())

    # Submit button
    submitted = st.form_submit_button("✅ Submit Registration", type="primary", use_container_width=True)

    if submitted:
        # Basic validation
        if not patient_name.strip():
            st.error("❌ Patient Name is required!")
        elif not phone.strip():
            st.error("❌ Phone Number is required!")
        else:
            # Create new row
            new_row = {
                "S.No.": len(st.session_state.df) + 1,
                "Patient Name": patient_name.strip().title(),
                "Gender": gender,
                "Date of Birth": dob,
                "Phone Number": phone.strip(),
                "Aadhar Number": aadhar.strip(),
                "Type of Registration": reg_type,
                "Date of Registration": reg_date,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Add to dataframe
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])], 
                ignore_index=True
            )

            # Save to CSV
            st.session_state.df.to_csv(DATA_FILE, index=False)

            st.success(f"🎉 Patient **{patient_name.strip().title()}** registered successfully!")
            st.balloons()

# ====================== VIEW ALL REGISTRATIONS ======================
st.divider()
st.subheader("📋 All Registered Patients")

if len(st.session_state.df) > 0:
    # Display table
    st.dataframe(
        st.session_state.df,
        use_container_width=True,
        hide_index=True
    )

    # Download button
    csv = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Data as CSV",
        data=csv,
        file_name="patient_registrations.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Optional: Clear all data button (with confirmation)
    if st.button("🗑️ Clear All Records", type="secondary"):
        if st.checkbox("Are you sure? This cannot be undone!"):
            st.session_state.df = pd.DataFrame(columns=st.session_state.df.columns)
            st.session_state.df.to_csv(DATA_FILE, index=False)
            st.success("All records cleared!")
            st.rerun()
else:
    st.info("No registrations yet. Fill the form above to get started!")

# ====================== FOOTER ======================
st.caption("Built with ❤️ using Streamlit + Python | Data saved locally in `patient_registrations.csv`")