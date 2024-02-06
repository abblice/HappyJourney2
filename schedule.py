import streamlit as st

def scheduletomenu():
    st.session_state['screen'] = "menu"

def load_menu():
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
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)
    st.title("Your Journey Schedule")
    st.header(" ")

    # access user which has logged in
    user = st.session_state['users'][st.session_state['username']]

    # define schedule parameters
    time_diff = user.journey.get_time_difference()
    direction = user.journey.get_direction()
    biowake = user.get_biowake()
    asleep = user.get_asleep()
    nights = user.journey.get_nights()
    land = user.journey.get_land()

    # create the schedule
    user.journey.create_schedule(biowake, asleep, nights, land, time_diff, direction)

    st.header(" ")

    st.button("Back to menu", on_click=scheduletomenu)
