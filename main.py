import pickle
import streamlit as st
import login
import signup
import start_journey
import schedule
from PIL import Image

# function to load the welcome/main screen only containing sign up/log in possibilities
def load_screen():
    # Add custom CSS
    custom_css = """
    <style>
        /* Center the title on the screen */
        .stApp {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-align: center;
            image-align: center
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
    image = Image.open("around-the-world.png")
    st.image(image, width=100)
    st.subheader(" ")
    st.title("Happy Journey")
    st.subheader(" ")
    st.button("Sign up", on_click=goto_signup)
    st.write(" ")
    st.button("Log in", on_click=goto_login)

# resets the screen session state
def goto_signup():
    st.session_state['screen'] = "signup"

# resets the screen session state
def goto_login():
    st.session_state['screen'] = "login"

# resets the screen session state
def goto_main():
    st.session_state['screen'] = "main"

# creates session state and sets it by default to the main screen
if 'screen' not in st.session_state:
    st.session_state['screen'] = 'main'

if 'users' not in st.session_state:
    st.session_state['users'] = {}


# check if the screen is main and if so, calls the main screen
if st.session_state['screen'] == "main":
    # unpickle the file to load each users' class information
    try:
        pickle_off = open("usersinfo.txt", "rb")
        st.session_state['users'] = pickle.load(pickle_off)
    except FileNotFoundError:
        pass
    except EOFError:
        pass
    load_screen()

# check if the screen is sign up and if so, calls the sign up screen
elif st.session_state['screen'] == "signup":
    signup.load_screen()

# check if the screen is log in and if so, calls the login screen and authenticator method
elif st.session_state['screen'] == "login":
    login.authenticate()

# check if the screen is start journey and if so, calls the start journey screen
elif st.session_state['screen'] == "start":
    start_journey.load_screen()

# check if the screen is menu and if so, calls the menu screen
elif st.session_state['screen'] == "menu":
    login.load_menu()

# check if the screen is menu and if so, calls the menu screen
elif st.session_state['screen'] == "schedule":
    schedule.load_menu()














