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

def contact():

    # Contact Me Section
    st.sidebar.write("## Contact Me")
    st.sidebar.markdown("""
    **Miles Wang**  
    📞 +86 18252032414  
    📞 +1 4373405941  
    📧 [nflsicmars@gmail.com](mailto:nflsicmars@gmail.com)  
    [![Instagram](https://img.icons8.com/ios-glyphs/30/000000/instagram-new.png)](https://www.instagram.com/mileswang2004/)  
    [![LinkedIn](https://img.icons8.com/ios-glyphs/30/000000/linkedin.png)](https://www.linkedin.com/in/miles-wang-177127293/)
    """, unsafe_allow_html=True)

