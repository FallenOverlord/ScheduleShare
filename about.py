import streamlit as st

def about_page():

    st.header("About the Author")

    st.markdown("""
    **Miles Wang**

    say hi to me on
    - [GitHub](https://github.com/FallenOverlord)
    - [Instagram](https://www.instagram.com/mileswang2004/)
    - [Discord](https://www.discordapp.com/users/miles_wang)
    - [LinkedIn](https://www.linkedin.com/in/miles-wang-177127293/)
    """)

    # Embed a video
    st.video("https://youtu.be/D0UnqGm_miA?si=_i3UsmxluIG8SK8g")
    st.image("https://media.giphy.com/media/3o7TKtnuHOHHUjR38Y/giphy.gif")

