import streamlit as st
import pandas as pd
import os
from passlib.context import CryptContext
from datetime import datetime

# MUST be the first Streamlit command
st.set_page_config(page_title="BHSPL Patient System", page_icon="🏥", layout="wide")

# ====================== PASSWORD HASHING ======================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    if len(password) > 72: password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if len(plain_password) > 72: plain_password = plain_password[:72]
        return pwd_context.verify(plain_password, hashed_password)
    except Exception: return False

# ====================== DATA FILES ======================
USERS_FILE = "users.csv"
REG_FILE = "patient_registrations.csv"

def init_files():
    if not os.path.exists(USERS_FILE):
        hashed = hash_password("admin123")
        pd.DataFrame({
            "username": ["admin"], "password": [hashed],
            "role": ["admin"], "name": ["Administrator"]
        }).to_csv(USERS_FILE, index=False)
    
    if not os.path.exists(REG_FILE):
        pd.DataFrame(columns=[
            "Patient ID", "Patient Name", "Gender", "Date of Birth",
            "Phone Number", "Aadhar Number", "District", "Mandal", 
            "Type of Registration", "Date of Registration", "Timestamp"
        ]).to_csv(REG_FILE, index=False)

init_files()

# ====================== SESSION STATE ======================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = ""

# ====================== LOGIN PAGE ======================
if not st.session_state.logged_in:
    st.title("🏥 BHSPL Patient Management System")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login", type="primary"):
            users_df = pd.read_csv(USERS_FILE)
            user_row = users_df[users_df["username"] == username]
            if not user_row.empty and verify_password(password, user_row.iloc[0]["password"]):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = user_row.iloc[0]["role"]
                st.rerun()
            else:
                st.error("Invalid credentials")
    st.stop()

# ====================== SIDEBAR ======================
st.sidebar.success(f"Logged in: **{st.session_state.username}**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

nav_options = ["Registration", "Vitals Entry"]
if st.session_state.role == "admin":
    nav_options += ["View All Data", "Manage Users"]

page = st.sidebar.radio("Navigation", nav_options)

# ====================== PAGE ROUTING ======================
if page == "Registration":
    from pages import Registration as reg
    reg.show_registration()
elif page == "Vitals Entry":
    from pages import Vitals as vit
    vit.show_vitals()
# ... Rest of admin pages logic remains the same