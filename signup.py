import streamlit as st
from generate_keys import *
from User import *
import pickle


user_name = ""
user_username = ""
user_password = ""

def signtomain():
    st.session_state['screen'] = "main"

# method to get the biological wake up chronotype of that user
def get_biowake(h_weekday, h_weekend, h_holiday):
    # formula to calculate biological wake up time
    biowake = min(h_holiday, h_weekend)

    if h_weekend > h_holiday:
        # the 0.3 is because sleep deprivation should shift the bio clock of around 30%
        biowake = biowake + 0.3*(h_weekend - h_holiday)

    if h_weekday < h_holiday:
        # the 0.1 is because artificial alarm wake up time should shift bio clock of around 10%
        biowake = biowake - 0.1*(h_holiday - h_weekday)

    # rounding the biowake and converting it to the right unit for the graph (ex: 10.5 instead of 630)
    bio_min = biowake % 60
    # rounding the bio minutes
    if bio_min != 0 or bio_min != 15 or bio_min != 30 or bio_min != 45:
        if bio_min >= 53:
            bio_min = 60
        elif bio_min >= 38:
            bio_min = 45
        elif bio_min >= 23:
            bio_min = 30
        elif bio_min >= 8:
            bio_min = 15
        else:
            bio_min = 0
    # converting the biowake time
    if bio_min == 0:
        bio_min = 0.0
    elif bio_min == 15:
        bio_min = 0.25
    elif bio_min == 30:
        bio_min = 0.5
    elif bio_min == 45:
        bio_min = 0.75

    # getting the converted biowake
    biowake = int(biowake/60) + bio_min

    return biowake


def submittomain():
    st.session_state['screen'] = "main"
    one_pw = [user_password]
    hashed_pw = stauth.Hasher(one_pw).generate()
    # Open a file with access mode 'a'
    file_object = open('users.txt', 'a')
    # Append data of that user at the end of file
    file_object.write(user_name + ", " + user_username + ", " + hashed_pw[0] + "\n")
    # Close the file
    file_object.close()

    print("Your biological wake up time is " + str(biowake) + " !")

    # creates a User object for the signed up User
    user = User(user_username, biowake, asleep)
    st.session_state['users'][user_username] = user

    # save the user to the pickle file
    with open('usersinfo.txt', 'wb') as fh:
        pickle.dump(st.session_state['users'], fh)

# creates the interface for sign up screen
def load_screen():
    global user_name, user_username, user_password, biowake, asleep
    st.title("Sign Up")
    st.subheader(" ")
    st.button("Back to main", on_click=signtomain)
    st.subheader(" ")
    st.subheader("Create a new account")
    st.write(" ")

    user_name = st.text_input("Name")
    user_username = st.text_input("Username")
    user_password = st.text_input("Password")

    st.write(" ")
    st.subheader("Sleep-Wake profile")
    st.write(" ")

    h_weekday = st.time_input("What time do you wake up on a weekday?")
    # get it as a string
    h_weekday = h_weekday.strftime("%H:%M:%S")
    # put in list
    h_wd_list = h_weekday.split(":")
    # get the time in minutes
    h_weekday = int(h_wd_list[0])*60 + int(h_wd_list[1])

    h_weekend = st.time_input("What time do you wake up on a weekend?")
    # get it as a string
    h_weekend = h_weekend.strftime("%H:%M:%S")
    # put in list
    h_we_list = h_weekend.split(":")
    # get the time in minutes
    h_weekend = int(h_we_list[0])*60 + int(h_we_list[1])

    h_holiday = st.time_input("What time do you wake up during a holiday?")
    # get it as a string
    h_holiday = h_holiday.strftime("%H:%M:%S")
    # put in list
    h_hd_list = h_holiday.split(":")
    # get the time in minutes
    h_holiday = int(h_hd_list[0])*60 + int(h_hd_list[1])

    biowake = get_biowake(h_weekday, h_weekend, h_holiday)

    asleep = st.number_input("How many hours of sleep do you need to feel well rested?", min_value=4, max_value=12, step=1)

    st.subheader(" ")
    # submit button which if called, calls
    st.button("Submit Account", on_click=submittomain)




