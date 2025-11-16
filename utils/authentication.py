import streamlit as st
import hashlib
import json
import os

class AuthenticationSystem:
    def __init__(self):
        self.users_file = "data/users.json"
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "role": "admin",
                    "email": "admin@safetroute.ai"
                },
                "user": {
                    "password": self._hash_password("user123"),
                    "role": "user",
                    "email": "user@example.com"
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f)
    
    def _hash_password(self, password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users and users[username]['password'] == self._hash_password(password):
                return {
                    'authenticated': True,
                    'username': username,
                    'role': users[username]['role'],
                    'email': users[username]['email']
                }
        except Exception as e:
            st.error(f"Authentication error: {e}")
        
        return {'authenticated': False}
    
    def register_user(self, username, password, email, role="user"):
        """Register new user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users:
                return False, "Username already exists"
            
            users[username] = {
                "password": self._hash_password(password),
                "role": role,
                "email": email
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f)
            
            return True, "User registered successfully"
            
        except Exception as e:
            return False, f"Registration failed: {e}"
    
    def render_login_sidebar(self):
        """Render login form in sidebar"""
        st.sidebar.title("ðŸ” Authentication")
        
        if 'user' not in st.session_state:
            st.session_state.user = None
        
        if st.session_state.user is None:
            # Login form
            with st.sidebar.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    auth_result = self.authenticate_user(username, password)
                    if auth_result['authenticated']:
                        st.session_state.user = auth_result
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            # Registration expander
            with st.sidebar.expander("New User? Register Here"):
                with st.form("register_form"):
                    new_username = st.text_input("New Username")
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    new_email = st.text_input("Email")
                    registered = st.form_submit_button("Register")
                    
                    if registered:
                        if new_password != confirm_password:
                            st.error("Passwords don't match")
                        else:
                            success, message = self.register_user(new_username, new_password, new_email)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
        else:
            # User is logged in
            user = st.session_state.user
            st.sidebar.success(f"Welcome, {user['username']}!")
            st.sidebar.write(f"Role: {user['role'].title()}")
            
            if st.sidebar.button("Logout"):
                st.session_state.user = None
                st.rerun()
            
            return user
        
        return None
