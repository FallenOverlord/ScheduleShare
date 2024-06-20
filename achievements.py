import streamlit as st
from db import load_profile
import sqlite3
import os

def get_achievements(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT achievement_money_master, achievement_leader_of_gang, achievement_loyal_guarddog, achievement_iron_determination, achievement_social_king FROM users WHERE username = ?', (username,))
    achievements = c.fetchone()
    conn.close()
    return achievements

def display_achievements(username):
    profile = load_profile(username)
    achievements = get_achievements(username)
    st.write("## Achievements")
    
    achievement_labels = {
        "achievement_money_master": "Money Master",
        "achievement_leader_of_gang": "Leader of the Gang",
        "achievement_loyal_guarddog": "Loyal Guarddog",
        "achievement_iron_determination": "Iron Determination",
        "achievement_social_king": "Social King"
    }

    # Use absolute paths to ensure Streamlit can locate the images
    script_dir = os.path.dirname(os.path.abspath(__file__))
    achievement_images = {
        "achievement_money_master": os.path.join(script_dir, "images", "MoneyMaster.png"),
        "achievement_leader_of_gang": os.path.join(script_dir, "images", "LeaderOfTheGang.png"),
        "achievement_loyal_guarddog": os.path.join(script_dir, "images", "LoyalGuarddog.png"),
        "achievement_iron_determination": os.path.join(script_dir, "images", "IronDetermination.png"),
        "achievement_social_king": os.path.join(script_dir, "images", "SocialKing.png")
    }

    if achievements:
        money_master, leader_of_gang, loyal_guarddog, iron_determination, social_king = achievements
        if money_master:
            st.write("🏆 Money Master: Get over 100 coins")
            st.image(achievement_images["achievement_money_master"], caption=achievement_labels["achievement_money_master"], width=200)
        if leader_of_gang:
            st.write("🏆 Leader of the Gang: Create a gang")
            st.image(achievement_images["achievement_leader_of_gang"], caption=achievement_labels["achievement_leader_of_gang"], width=200)
        if loyal_guarddog:
            st.write("🏆 Loyal Guarddog: Join a gang")
            st.image(achievement_images["achievement_loyal_guarddog"], caption=achievement_labels["achievement_loyal_guarddog"], width=200)
        if iron_determination:
            st.write("🏆 Iron Determination: Sign in for 3 days")
            st.image(achievement_images["achievement_iron_determination"], caption=achievement_labels["achievement_iron_determination"], width=200)
        if social_king:
            st.write("🏆 Social King: Have non-null email and Instagram")
            st.image(achievement_images["achievement_social_king"], caption=achievement_labels["achievement_social_king"], width=200)
    else:
        st.write("No achievements yet.")
