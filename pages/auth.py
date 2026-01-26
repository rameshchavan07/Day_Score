import streamlit as st
import requests
import re
from firebase_web_config import FIREBASE_CONFIG

def is_valid_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def show():
    st.set_page_config(page_title="Login - DayScore+", layout="centered")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;'>
        <h1 style='font-size: 3em; margin: 0; color: white;'>🧠 DayScore+</h1>
        <p style='font-size: 1.1em; margin-top: 20px; opacity: 0.9;'>Gamifying Student Well-Being with AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Tab selection
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Welcome Back!")
        
        login_email = st.text_input("Email", key="login_email", placeholder="your@email.com")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True, key="login_btn"):
            if not login_email or not login_password:
                st.error("❌ Please fill in all fields")
            elif not is_valid_email(login_email):
                st.error("❌ Invalid email format")
            else:
                try:
                    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_CONFIG['apiKey']}"
                    
                    payload = {
                        "email": login_email,
                        "password": login_password,
                        "returnSecureToken": True
                    }
                    
                    response = requests.post(rest_api_url, json=payload)
                    
                    if response.status_code == 200:
                        user_data = response.json()
                        st.session_state.user_id = user_data.get("localId")
                        st.session_state.user_email = login_email
                        st.session_state.id_token = user_data.get("idToken")
                        st.session_state.logged_in = True
                        
                        st.success("✅ Login successful!")
                        st.balloons()
                        
                        import time
                        time.sleep(1)
                        st.switch_page("pages/landing.py")
                    else:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', 'Invalid credentials')
                        st.error(f"❌ Login failed: {error_msg}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    with tab2:
        st.subheader("Create Your Account")
        
        signup_name = st.text_input("Full Name", key="signup_name", placeholder="John Doe")
        signup_email = st.text_input("Email", key="signup_email", placeholder="your@email.com")
        signup_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Sign Up", use_container_width=True, key="signup_btn"):
            if not signup_name or not signup_email or not signup_password or not signup_confirm:
                st.error("❌ Please fill in all fields")
            elif not is_valid_email(signup_email):
                st.error("❌ Invalid email format")
            elif len(signup_password) < 6:
                st.error("❌ Password must be at least 6 characters")
            elif signup_password != signup_confirm:
                st.error("❌ Passwords don't match")
            else:
                try:
                    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_CONFIG['apiKey']}"
                    
                    payload = {
                        "email": signup_email,
                        "password": signup_password,
                        "returnSecureToken": True
                    }
                    
                    response = requests.post(rest_api_url, json=payload)
                    
                    if response.status_code == 200:
                        user_data = response.json()
                        user_id = user_data.get("localId")
                        
                        # Save user info to Firestore
                        try:
                            from firebase_config import db
                            db.collection("users").document(user_id).set({
                                "name": signup_name,
                                "email": signup_email,
                                "created_at": __import__('firebase_admin').firestore.SERVER_TIMESTAMP
                            })
                        except Exception as fs_error:
                            st.warning(f"Account created but couldn't save profile: {fs_error}")
                        
                        st.session_state.user_id = user_id
                        st.session_state.user_email = signup_email
                        st.session_state.user_name = signup_name
                        st.session_state.id_token = user_data.get("idToken")
                        st.session_state.logged_in = True
                        
                        st.success("✅ Account created successfully!")
                        st.balloons()
                        
                        import time
                        time.sleep(1)
                        st.switch_page("pages/landing.py")
                    else:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', 'Signup failed')
                        if "EMAIL_EXISTS" in error_msg:
                            st.error("❌ Email already registered")
                        else:
                            st.error(f"❌ Signup failed: {error_msg}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    st.info("📝 Sign up or log in to get started!")
