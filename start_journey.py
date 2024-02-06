import streamlit as st
import pickle


def starttomenu():
    st.session_state['screen'] = "menu"


def submit():
    # access user which has logged in
    user = st.session_state['users'][st.session_state['username']]

    # add a journey to the user
    user.add_journey(departing_city, arriving_city, land, nights)

    # checking if the cities are valid and with different time zones
    user.journey.city_info()
    if user.journey.city_valid():
        user.journey.time_info()
        if user.journey.time_valid():

            print(user.journey.get_time_difference())

            # add the latitude and longitude of the journey to save it in the "travelled to" destinations
            user.add_coordinates()

            # save the user's updated journey info to the pickle file
            with open('usersinfo.txt', 'wb') as fh:
                    pickle.dump(st.session_state['users'], fh)

            st.session_state['screen'] = "schedule"

def load_screen():
    global departing_city, arriving_city, land, nights

    st.header("Then tell us about your trip!")
    st.header(" ")
    st.button("Back to menu", on_click=starttomenu)
    st.subheader(" ")

    departing_city = st.text_input("What city are you travelling from?")

    arriving_city = st.text_input("What city are you travelling to?")

    land = st.time_input("At what local time will you be landing at you destination?")
    # get it as a string
    h_land = land.strftime("%H:%M:%S")
    # put in list
    h_l_list = h_land.split(":")
    # get the time in minutes
    land = int(h_l_list[0])*60 + int(h_l_list[1])
    # convert it to the graphing hour unit (ex: 10.5 instead of 630)
    min = land % 60
    if min == 0:
        min = 0.0
    elif min == 15:
        min = 0.25
    elif min == 30:
        min = 0.5
    elif min == 45:
        min = 0.75
    # get land as a double
    land = int(land/60) + min

    nights = st.number_input("How many nights will you be staying at your destination?", min_value=1, max_value=7, step=1)

    st.write(" ")

    st.button("Get my schedule!", on_click=submit)

