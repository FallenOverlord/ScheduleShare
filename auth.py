import streamlit as st
import bcrypt
import streamlit_authenticator as stauth
from db import load_users, save_user, user_exists

# Load users from database
config = {
    'credentials': load_users(),
    'cookie': {
        'expiry_days': 30,
        'name': 'some_cookie_name',
        'key': 'some_signature_key'
    },
    'preauthorized': {
        'emails': [
            'johndoe@example.com',
            'janedoe@example.com'
        ]
    }
}

# Setup the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def register_user(new_username, new_email, new_name, new_password):
    if user_exists(new_username):
        raise ValueError("Username already exists.")
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    save_user(new_username, new_email, new_name, hashed_password)
    # Refresh the config with the new user
    config['credentials'] = load_users()
    authenticator.credentials = config['credentials']

def login():
    try:
        name, authentication_status, username = authenticator.login(
            location='main',
            fields={
                'Form name': 'Login',
                'Username': 'Username',
                'Password': 'Password',
                'Login': 'Login'
            }
        )
        return name, authentication_status, username
    except KeyError as e:
        st.error(f"KeyError: {e}")
        st.stop()

def logout():
    authenticator.logout('Logout', 'main')
