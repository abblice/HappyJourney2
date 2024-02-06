import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import pandas as pd
import numpy as np

def logtomain():
    st.session_state['screen'] = "main"

# when called, sets the session state to start journey for that screen to load from the menu
def menutostart():
    st.session_state['screen'] = "start"

def menutomenu():
    st.session_state['screen'] = "menu"

# loads menu screen where user will be able to start a new/resume a journey
def load_menu():

    col1, col2 = st.columns(2)
    image = Image.open("around-the-world.png")
    col1.image(image, width=150)
    col2.title("Welcome to Happy Journey " + name + "!")

    st.header(" ")

    if st.session_state['username']:

        user = st.session_state['users'][st.session_state['username']]

        coordinates = user.get_coordinates()

        st.text("Explore the map to see where you have travelled with HappyJourney...")

        if coordinates:
            # getting the data from the coordinates into two separate lat and long columns
            coordinates_array = np.array(coordinates, dtype=float)
            df = pd.DataFrame(coordinates_array, columns=['latitude', 'longitude'])

            st.map(df)

        else:
            df = pd.DataFrame(data=coordinates, columns=['latitude', 'longitude'])
            st.map(df)

    with st.sidebar:

        st.subheader("Departing tomorrow?")
        st.button("Get your schedule here!", on_click=menutostart)

        st.header(" ")

        # log out button (not completely functioning yet)
        authenticator.logout("Logout", "main")


def authenticate():
    global authenticator, name, username

    st.button("Back to main", on_click=logtomain)
    st.subheader(" ")
    # read through text file containing user info
    users = []
    filename = "users.txt"
    with open(filename, "r") as file:
        lines = file.readlines()

        for l in lines:
            # split every line and every comma
            d = l.strip("\n").split(", ")

            #  append each user info (name, username, password) to users list
            users.append(d)

    # create the credentials "dictionary" and add all usernames, names and passwords in three separate credentials
    credentials = {"usernames": {}}
    for u in users:
        credentials["usernames"][u[1]] = {}
        credentials["usernames"][u[1]]["name"] = u[0]
        credentials["usernames"][u[1]]["password"] = u[2]

    # create authenticator
    authenticator = stauth.Authenticate(credentials, "sales_dashboard", "abcdef", cookie_expiry_days=30)

    # assign all the logged in user information to the authenticator and make log in interface
    name, authentication_status, username = authenticator.login("Login", "main")

    # check the authentication_status to know what message to output
    if authentication_status == False:
        st.error("Username/password is incorrect, please re-enter")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    # check if log in was successful, if yes then set screen to menu which will call the load menu function from main file
    if authentication_status:
        st.session_state['screen'] = "menu"

