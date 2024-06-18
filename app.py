import streamlit as st
import pandas as pd
from db import save_profile, load_profile, get_user_gangs, load_gang_members
from ics_processing import extract_events, calculate_total_course_time
from visualization import plot_timetable
from comparison import plot_comparison
from course_time import get_total_course_time
from bar_chart import plot_bar_chart
from pie_chart import show_pie_chart
from gang_management import create_gang, join_gang, search_gang, generate_gang_logo, get_gang_size, get_gang_members_profiles
import time
import streamlit as st
import bcrypt
import streamlit_authenticator as stauth
from db import load_users, save_user, user_exists

# Set page configuration
st.set_page_config(page_title="Schedule Share", page_icon="📅", layout="wide")

def logout():
    authenticator.logout('Logout', 'main')

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

# Registration form
if 'register' not in st.session_state:
    st.session_state.register = False

if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = []

if st.session_state.register:
    st.title("Create a New Account")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_name = st.text_input("Full Name")
    new_password = st.text_input("Password", type="password")
    new_password_confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != new_password_confirm:
            st.error("Passwords do not match!")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            save_user(new_username, new_email, new_name, hashed_password)
            st.success("Account created successfully!")
            st.session_state.register = False

    if st.button("Go back to login"):
        st.session_state.register = False

else:
    # Login process
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
    except KeyError as e:
        st.error(f"KeyError: {e}")
        st.stop()



    if authentication_status:
        st.write(f"Welcome *{name}*")
        logout()

        # Profile Page
        st.sidebar.title("Menu")
        page = st.sidebar.selectbox("Choose a page", ["Home", "Profile", "Search Profiles", "Gang"])



        if page == "Home":
            st.title("Home")
            st.write("Welcome to Schedule Share!")

            # Load the profile and timetable for the logged-in user
            profile = load_profile(username)

            #draw the user's timetable
            if profile[4]:
                events, title = extract_events(profile[4])
                timetable_fig = plot_timetable(events, title)
                if timetable_fig:
                    st.plotly_chart(timetable_fig, use_container_width=True)

            #st.write("Loaded profile:", profile)  # Debugging
            if len(profile) > 5 and profile[5] is not None:
                logged_in_total_course_time = profile[5]
                st.session_state.comparison_data.append((username, logged_in_total_course_time))
                st.write("your total course time:", logged_in_total_course_time)  # Debugging
            
            # Generate and display the pie chart
            show_pie_chart(profile[4])



        elif page == "Profile":
            st.title("Create Your Profile")
            profile_name = st.text_input("Name", value=name)
            profile_email = st.text_input("Email", value=config['credentials']['usernames'][username]['email'])
            profile_instagram = st.text_input("Instagram Username")
            profile_timetable = st.file_uploader("Upload your timetable (.ics file)", type="ics")

            if st.button("Save Profile"):
                timetable_content = profile_timetable.read() if profile_timetable else None
                save_profile(username, profile_name, profile_email, profile_instagram, timetable_content)
                st.success("Profile created successfully!")

        elif page == "Search Profiles":
            st.title("Search for a Profile")
            search_name = st.text_input("Enter name to search")
            if st.button("Search"):
                st.write("loading ...")

                # Load the current user's profile
                myProfile = load_profile(username)

                # Load the target user's profile
                target_profile = load_profile(search_name)

                # Ensure target_profile is valid
                if target_profile:
                    st.write(f"Username: {target_profile[0]}, Name: {target_profile[1]}, Email: {target_profile[2]}, Instagram: {target_profile[3]}")

                    # Draw the target user's timetable
                    if target_profile[4]:
                        events, title = extract_events(target_profile[4])
                        timetable_fig = plot_timetable(events, title)
                        if timetable_fig:
                            st.plotly_chart(timetable_fig, use_container_width=True)

                    # Display total course time of the target user
                    searched_total_course_time = target_profile[5]

                    # Display total course time of the current user
                    if myProfile and myProfile[5] is not None:
                        logged_in_total_course_time = myProfile[5]

                        # Display Comparison Results
                        comparison_fig = plot_bar_chart(username, logged_in_total_course_time, target_profile[0], searched_total_course_time)
                        st.plotly_chart(comparison_fig, use_container_width=True)
                else:
                    st.error("Profile not found.")

        elif page == "Gang":
            st.title("Gang Management")
            action = st.radio("Choose an action", ["Create Gang", "Join Gang", "Search Gang"])

            if action == "Create Gang":
                gang_name = st.text_input("Enter gang name")
                if st.button("Create Gang"):
                    logo_url = generate_gang_logo(gang_name)
                    size = 1  # Starting size of the gang
                    create_gang(gang_name, username, logo_url, size)
                    st.success(f"Gang '{gang_name}' created successfully!")

            elif action == "Join Gang":
                gang_name = st.text_input("Enter gang name to join")
                if st.button("Join Gang"):
                    join_gang(gang_name, username)
                    st.success(f"You have joined the gang '{gang_name}'!")

            elif action == "Search Gang":
                gang_name = st.text_input("Enter gang name to search")
                if st.button("Search Gang"):
                    gang, members = search_gang(gang_name)
                    if gang:
                        st.write(f"Gang Name: {gang[0]}, Leader: {gang[1]}, Logo URL: {gang[2]}, Size: {gang[3]}")
                        st.image(gang[2], caption=f"Logo for {gang[0]}")
                        st.write("Members:")
                        for member in members:
                            st.write(member)

                        st.write("### Gang Members' Schedules and Profiles")
                        profiles = get_gang_members_profiles(gang_name)
                        for profile in profiles:
                            st.write(f"Username: {profile[0]}, Name: {profile[1]}, Email: {profile[2]}, Instagram: {profile[3]}")
                            if profile[4]:
                                events, title = extract_events(profile[4])
                                timetable_fig = plot_timetable(events, title)
                                if timetable_fig:
                                    st.plotly_chart(timetable_fig, use_container_width=True)
                    else:
                        st.error("Gang not found.")
                    
            # Display user's gangs
            st.write("### Your Gangs")
            user_gangs = get_user_gangs(username)
            if user_gangs:
                for gang in user_gangs:
                    st.write(f"Gang: {gang}")
                    members = load_gang_members(gang)
                    st.write("Members:")
                    for member in members:
                        st.write(member)
            else:
                st.write("You are not a member of any gangs.")


















    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

    if st.button("Create a new account"):
        st.session_state.register = True
