import streamlit as st
import base64
import requests
import os

BASE_URL = "http://127.0.0.1:8000/api/auth"

# --- Page Configuration ---
st.set_page_config(page_title="DelightAPI - Access", layout="wide")

# --- Function to load and encode image ---
def get_base64_image(image_path):

    if not os.path.exists(image_path):
        st.warning(f"Image not found: {image_path}")
        return ""
     
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- Load image ---
img_base64 = get_base64_image("register_login.webp")

# --- CSS Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/webp;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 3rem 2rem;
        border-radius: 1rem;
        max-width: 600px;
        margin: 5rem auto;
        box-shadow: 0 0 25px rgba(0,0,0,0.1);
    }}
    .form-title {{
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #8e44ad;
        margin-bottom: 1.5rem;
    }}
    button[kind="primary"] {{
        background-color: #e63946;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.75rem;
        margin-top: 1rem;
        width: 100%;
        border: none;
        font-size: 1rem;
    }}
    button[kind="primary"]:hover {{
        background-color: #c62828;
    }}
    a {{
        color: #007bff;
        text-decoration: none;
        font-size: 0.9rem;
    }}
    a:hover {{
        text-decoration: underline;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Session State for Page Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- Page Switchers ---
def switch_to_register():
    st.session_state.page = "register"

def switch_to_login():
    st.session_state.page = "login"

# --- Main Container ---
with st.container():
    st.markdown('<div class="form-title">🍰 DelightAPI</div>', unsafe_allow_html=True)

    if st.session_state.page == "login":
        with st.form("login_form"):
            st.subheader("Sign In")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Sign In")

            if login_submit:
                if not email.strip() or not password.strip():
                    st.error("🚫 Please enter both email and password.")
                else:
                    data = {
                        "username": email.split('@')[0],  # or whatever mapping your backend expects
                        "password": password
                    }

                    try:
                        res = requests.post(f"{BASE_URL}/login/", json=data)
                        if res.status_code == 200:
                            token = res.json().get("token")
                            st.success("✅ Login successful!")
                            st.session_state["token"] = token
                            st.session_state["logged_in"] = True
                            st.session_state["email"] = email
                            # You can navigate or render more views here
                        else:
                            st.error("❌ Invalid credentials.")
                    except Exception as e:
                        st.error(f"⚠️ Could not connect to backend: {e}")


        st.button("New user? Sign Up", on_click=switch_to_register)

    elif st.session_state.page == "register":
        with st.form("register_form"):
            st.subheader("Sign Up")
            full_name = st.text_input("Full Name")
            mobile = st.text_input("Mobile Number")
            address = st.text_area("Address")
            email = st.text_input("Email")
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            location = st.selectbox("Select Location", ["Hyderabad", "Bangalore", "Mumbai"])
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            register_submit = st.form_submit_button("Register")

            if register_submit:
                if not all([full_name.strip(), mobile.strip(), address.strip(), email.strip(), password.strip(), confirm_password.strip()]):
                    st.error("🚫 Please fill in all the required fields.")
                elif password != confirm_password:
                    st.error("🔐 Passwords do not match.")
                else:
                    # Streamlit to Django API call
                    username = email.split('@')[0]
                    data = {
                        "username": username,
                        "email": email,
                        "password": password,
                        "first_name": full_name.split()[0],
                        "last_name": " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else "",
                        "phone_number": mobile,
                        "gender": gender[0],  # M/F/O
                        "address": address
                    }

                    try:
                        res = requests.post(f"{BASE_URL}/register/", json=data)
                        if res.status_code == 200 or res.status_code == 201:
                            st.success("🎉 Registered successfully!")
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {res.json().get('error', 'Registration failed')}")
                    except Exception as e:
                        st.error(f"⚠️ Could not connect to backend: {e}")

        st.button("Already have an account? Sign In", on_click=switch_to_login)

    st.markdown('</div>', unsafe_allow_html=True)