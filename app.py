import streamlit as st
import pandas as pd
from db import save_profile, load_profile, get_user_gangs, load_gang_members
from ics_processing import extract_events, calculate_total_course_time
from visualization import plot_timetable
from bar_chart import plot_bar_chart
from pie_chart import show_pie_chart
from gang_management import create_gang, join_gang, search_gang, generate_gang_logo, get_gang_size, get_gang_members_profiles, calculate_gang_overlaps, get_top_gangs
import time
import streamlit as st
import bcrypt
import streamlit_authenticator as stauth
from db import load_users, save_user, user_exists
from overlaps import get_overlapping_courses
from coins import initialize_coins, get_coins, daily_sign_in, add_coins, use_coins
from ads import show_ad
import streamlit.components.v1 as components
from achievements import display_achievements
from schedule_creator import schedule_creator
from about import about_page

# Set page configuration
st.set_page_config(page_title="Schedule Share", page_icon="📅", layout="wide")
#st.write("Welcome to Schedule Share.")



# Custom CSS
st.markdown("""
        <style>
        /* Background */
        .stApp {
            background: linear-gradient(135deg, #FF6F61 10%, #92A8D1 100%);
            color: #FFFFFF;
        }
        /* Sidebar */
        .css-1d391kg {
            background-color: #6B5B95;
            color: #FFFFFF;
        }
        .css-1d391kg .css-1y4p8pa {
            color: #FFFFFF;
        }
        .css-1d391kg .css-1y4p8pa:hover {
            color: #F7CAC9;
        }
        .css-1d391kg .css-1v3fvcr {
            color: #FFFFFF;
        }
        .css-1d391kg .css-1v3fvcr:hover {
            color: #F7CAC9;
        }
        /* Sidebar title */
        .css-1d391kg .css-1j9dxys {
            font-size: 20px;
            font-weight: bold;
        }
        /* Sidebar header */
        .css-1d391kg .css-1v3fvcr {
            font-size: 18px;
            font-weight: bold;
        }
        /* Sidebar text */
        .css-1d391kg .css-1y4p8pa {
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def set_page(page):
    st.session_state.page = page
    

def refresh_credentials():
    config['credentials'] = load_users()
    # Ensure there are no empty keys
    if '' in config['credentials']['usernames']:
        del config['credentials']['usernames']['']
    authenticator.credentials = config['credentials']
    st.write(f"Loaded credentials: {config['credentials']}")
    st.write(f"Authenticator credentials after refresh: {authenticator.credentials}")

# Function to clear session state
def clear_session_state():
    keys_to_clear = ['authentication_status', 'username', 'name', 'register', 'comparison_data']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def logout():
    
    authenticator.logout('Logout', 'main')
    
    #clear_session_state()

def show_overlaps(timetable1, timetable2):
    # Find and visualize overlaps
    overlaps = get_overlapping_courses(timetable1, timetable2)
    if overlaps:
        st.write("### Overlapping Courses")
        overlap_fig = plot_timetable(overlaps, "Overlapping Courses")
        st.plotly_chart(overlap_fig, use_container_width=True)
    else:
        st.write("No overlapping courses found.")

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

# Initialize session state
if 'register' not in st.session_state:
    st.session_state.register = False

if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = []

if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = None

if 'username' not in st.session_state:
    st.session_state.username = None

if 'name' not in st.session_state:
    st.session_state.name = None

if 'logout' not in st.session_state:
    st.session_state.logout = False

if st.session_state.register:
    st.title("Create a New Account")
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_name = st.text_input("Full Name")
    new_password = st.text_input("Password", type="password")
    new_password_confirm = st.text_input("Confirm Password", type="password")   

    if st.button("Register"):
        if not new_username.islower():
            st.error("Username must be in all non-capital letters.")
        elif new_password != new_password_confirm:
            st.error("Passwords do not match!")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            save_user(new_username, new_email, new_name, hashed_password)
            initialize_coins(new_username)
            st.success("Account created successfully!")
            #add_coins(new_username, 100)
            st.session_state.register = False

    if st.button("Go back to login"):
        st.session_state.register = False
    
        # Show ads on the registration page
    #show_ads()

else:
    #refresh_credentials()
    #clear_session_state()
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

        # Daily sign-in bonus
        daily_sign_in(username)

        # Profile Page
        st.sidebar.title("Menu")
        st.sidebar.write(f"Coins: {get_coins(username)}")  # Display coins in the sidebar
        page = st.sidebar.selectbox("Choose a page", ["Home", "Create Schedule", "Profile", "Search Profiles", "Gang", "About"])


        if page == "Home":
            st.title("Home")
            st.write("Welcome to Schedule Share! 🏠")

            # Load the profile and timetable for the logged-in user
            profile = load_profile(username)

            try:
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
            
            except:
                st.write("Please upload your timetable in the 'Profile' section. 🫡")
                st.write("Don't have an .ics files yet? We've got u covered! Create a new schedule NOW! 💘")

            # Display achievements
            display_achievements(username)
        
        elif page == "Create Schedule":
            schedule_creator()





        elif page == "Profile":
            st.title("Create Your Profile")
            profile_name = st.text_input("Name", value=name)
            profile_email = st.text_input("Email", value=config['credentials']['usernames'][username]['email'])
            profile_instagram = st.text_input("Instagram Username")
            profile_timetable = st.file_uploader("Upload your timetable (.ics file)", type="ics")

            if st.button("Save Profile"):
                try:
                    timetable_content = profile_timetable.read() if profile_timetable else None
                    save_profile(username, profile_name, profile_email, profile_instagram, timetable_content)
                    st.success("Profile created successfully!")
                except:
                    profile_timetable = None

        elif page == "Search Profiles":
            st.title("Search for a Profile")
            search_name = st.text_input("Enter name to search")
            if st.button("Search"):

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

                        show_overlaps(myProfile[4], target_profile[4])

                else:
                    st.error("Profile not found.")

        elif page == "About":
            about_page()
            

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
                        try:
                            #create gang logo
                            st.write(f"Leader: {gang[1]}, Size: {gang[3]}")
                            st.image(gang[2], caption=f"Logo for {gang[0]}")
                        except:
                            st.write(f"This gang currently have no logo. 😰")

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

                    # Add a button to show overlaps
                    if st.button(f"Show overlaps for {gang}"):
                        all_overlaps = calculate_gang_overlaps(gang)
                        st.write(f"### Overlapping Courses in {gang}")
                        overlap_fig = plot_timetable(all_overlaps, "Overlapping Courses in Gang")
                        st.plotly_chart(overlap_fig, use_container_width=True)

            else:
                st.write("You are not a member of any gangs.")

            # Display top gangs
            st.write("### Top Gangs")
            top_gangs = get_top_gangs()
            if top_gangs:
                for gang in top_gangs:
                    st.write(f"Gang Name: {gang[0]}, Size: {gang[1]}")
            else:
                st.write("No gangs found.")












    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

    if st.button("Create a new account"):
        st.session_state.register = True