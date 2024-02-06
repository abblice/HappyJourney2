# importing modules
import streamlit as st
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches


class Journey:

    def __init__(self, Dcity, Acity, land, nights):
        self.Dcity = Dcity
        self.Acity = Acity
        self.land = land
        self.nights = nights

    def get_Dcity(self):
        return self.Dcity

    def get_Acity(self):
        return self.Acity

    def get_land(self):
        return self.land

    def get_nights(self):
        return self.nights

    def city_info(self):
        global location_departing, location_arriving, departing, arriving

        # initialize Nominatim API
        geolocator = Nominatim(user_agent="GeoLoc")

        # DEPARTING CITY
        departing = self.Dcity

        # getting latitude and longitude of departing city
        location_departing = geolocator.geocode(departing)

        # ARRIVAL CITY
        arriving = self.Acity

        # getting latitude and longitude of arriving city
        location_arriving = geolocator.geocode(arriving)

    def city_valid(self):
        # check if the departing city is not valid
        if location_departing is None or location_arriving is None:
            st.error("Departing/Arriving city is not valid, please re-enter")
            return False
        else:
            return True

    def time_info(self):
        global departing_list, arriving_list, date_departing, date_arriving

        # create timezone object
        obj = TimezoneFinder()

        # pass the latitude and longitude into a timezone_at and it return timezone
        departing_timezone = obj.timezone_at(lng=location_departing.longitude, lat=location_departing.latitude)

        departing_tz = pytz.timezone(departing_timezone)
        date_departing = datetime.now(departing_tz)
        current_time_departing = date_departing.strftime("%H:%M:%S")

        # pass the latitude and longitude into a timezone_at and it return timezone
        arriving_timezone = obj.timezone_at(lng=location_arriving.longitude, lat=location_arriving.latitude)

        arriving_tz = pytz.timezone(arriving_timezone)
        date_arriving = datetime.now(arriving_tz)
        current_time_arriving = date_arriving.strftime("%H:%M:%S")

        # split the hour, minute and seconds indicators to be able to calculate difference
        departing_list = current_time_departing.split(":")
        arriving_list = current_time_arriving.split(":")

    def time_valid(self):
        # check if there is no time difference
        if int(departing_list[0]) == int(arriving_list[0]) and int(departing_list[1]) == int(arriving_list[1]):
            st.error("You are not changing timezones, so no need to adapt! Please re-enter.")
            return False
        else:
            return True

    def get_time_difference(self):
        global minute_difference
        # when both cities and times are valid, calculate the time difference
        minute_difference = 0

        # get the date of each of the times
        day1 = date_departing.day
        day2 = date_arriving.day

        month1 = date_departing.month
        month2 = date_arriving.month

        # compare to see if they are equal or not

        if day1 == day2:
            # check which destination's time is later

            # check if there is no minute difference
            if int(departing_list[1]) == int(arriving_list[1]):

                # this means the user is travelling east
                if int(departing_list[0]) < int(arriving_list[0]):
                    minute_difference = (int(arriving_list[0]) * 60) - (int(departing_list[0]) * 60)

                # this means the user is travelling west
                elif int(departing_list[0]) > int(arriving_list[0]):
                    minute_difference = (int(departing_list[0]) * 60) - (int(arriving_list[0]) * 60)

            # this means there is a minute difference
            else:

                # check if there is no hour difference
                if int(departing_list[0]) == int(arriving_list[0]):

                    # check which one is the furthest in minutes for subtraction
                    if int(departing_list[1]) < int(arriving_list[1]):
                        minute_difference = int(arriving_list[1]) - int(departing_list[1])

                    elif int(departing_list[1]) > int(arriving_list[1]):
                        minute_difference = int(departing_list[1]) - int(arriving_list[1])

                # this means the user is travelling east
                elif int(departing_list[0]) < int(arriving_list[0]):
                    minute_difference = ((int(arriving_list[0]) * 60) + int(arriving_list[1])) - (
                                (int(departing_list[0]) * 60) + int(departing_list[1]))

                # this means the user is travelling west
                elif int(departing_list[0]) > int(arriving_list[0]):
                    minute_difference = ((int(departing_list[0]) * 60) + int(departing_list[1])) - (
                                (int(arriving_list[0]) * 60) + int(arriving_list[1]))

        # this means the user is travelling east
        elif (day1 < day2 and month1 == month2) or (day1 > day2 and month1 != month2):
            # add the difference between time1 and 00:00 and then time2
            minute_difference = (1440 - (int(departing_list[0]) * 60 + int(departing_list[1]))) + (
                        int(arriving_list[0]) * 60 + int(arriving_list[1]))

        # this means the user is travelling west
        elif (day1 > day2 and month1 == month2) or (day1 < day2 and month1 != month2):
            # add the difference between time2 and 00:00 and then time1
            minute_difference = (1440 - (int(arriving_list[0]) * 60 + int(arriving_list[1]))) + (
                        int(departing_list[0]) * 60 + int(departing_list[1]))

        # the 12 hours thing
        if minute_difference > 720:
            minute_difference = 1440 - minute_difference

        # converting the time difference into the graph hour system (ex: 10.5 instead of 630)
        min_diff = minute_difference % 60
        if min_diff == 0:
            min_diff = 0.0
        elif min_diff == 15:
            min_diff = 0.25
        elif min_diff == 30:
            min_diff = 0.5
        elif min_diff == 45:
            min_diff = 0.75

        # time_diff will be the real time difference value in the right "unit"
        time_diff = int(minute_difference / 60) + min_diff

        return time_diff

    def get_direction(self):
        direction = ""
        minute_difference = 0

        # get the date of each of the times
        day1 = date_departing.day
        day2 = date_arriving.day

        # compare to see if they are equal or not

        if day1 == day2:
            # check which destination's time is later

            # check if there is no minute difference
            if int(departing_list[1]) == int(arriving_list[1]):

                # this means the user is travelling east
                if int(departing_list[0]) < int(arriving_list[0]):
                    direction = "east"
                    minute_difference = (int(arriving_list[0]) * 60) - (int(departing_list[0]) * 60)

                # this means the user is travelling west
                elif int(departing_list[0]) > int(arriving_list[0]):
                    direction = "west"
                    minute_difference = (int(departing_list[0]) * 60) - (int(arriving_list[0]) * 60)

            # this means there is a minute difference
            else:

                # check if there is no hour difference
                if int(departing_list[0]) == int(arriving_list[0]):

                    # check which one is the furthest in minutes for subtraction
                    if int(departing_list[1]) < int(arriving_list[1]):
                        direction = "east"
                        minute_difference = int(arriving_list[1]) - int(departing_list[1])

                    elif int(departing_list[1]) > int(arriving_list[1]):
                        direction = "west"
                        minute_difference = int(departing_list[1]) - int(arriving_list[1])

                # this means the user is travelling east
                elif int(departing_list[0]) < int(arriving_list[0]):
                    direction = "east"
                    minute_difference = ((int(arriving_list[0]) * 60) + int(arriving_list[1])) - (
                                (int(departing_list[0]) * 60) + int(departing_list[1]))

                # this means the user is travelling west
                elif int(departing_list[0]) > int(arriving_list[0]):
                    direction = "west"
                    minute_difference = ((int(departing_list[0]) * 60) + int(departing_list[1])) - (
                                (int(arriving_list[0]) * 60) + int(arriving_list[1]))

        # this means the user is travelling east
        elif day1 < day2:
            direction = "east"
            # add the difference between time1 and 00:00 and then time2
            minute_difference = (1440 - (int(departing_list[0]) * 60 + int(departing_list[1]))) + (
                        int(arriving_list[0]) * 60 + int(arriving_list[1]))

        # this means the user is travelling west
        elif day1 > day2:
            direction = "west"
            # add the difference between time2 and 00:00 and then time1
            minute_difference = (1440 - (int(arriving_list[0]) * 60 + int(arriving_list[1]))) + (
                        int(departing_list[0]) * 60 + int(departing_list[1]))

        # to get the time difference used for the actual calculations (equivalent) but without caring about the date
        if minute_difference > 720:
            if direction == "east":
                direction = "west"
            elif direction == "west":
                direction = "east"

        return direction

    def get_loc(self):
        # initialize Nominatim API
        geolocator = Nominatim(user_agent="GeoLoc")

        # ARRIVAL CITY
        arriving = self.Acity

        # getting latitude and longitude of arriving city
        location = geolocator.geocode(arriving)

        # create this list to format it in only the latitude and longitude data of the location
        loc = []

        loc.append(location.latitude)
        loc.append(location.longitude)

        return loc

    def create_schedule(self, biowake, asleep, nights, land, time_diff, direction):
        # Create a figure and axis
        fig = plt.figure()
        plot = fig.add_subplot(111)

        fig.set_figwidth(15)
        fig.set_figheight(7.5)

        # get the biosleep time
        biosleep = biowake + (24 - asleep)
        if biosleep > 24:
            biosleep = biosleep - 24

        day = 1

        # for if the travel day instructions were accounted for
        time_diff = time_diff - 1

        # if there is only 1 hour or less time difference to start with
        if time_diff <= 0:
            if direction == "east":
                plot.set_title(
                    label="just a little tip for your travel day:\ntry and get as much sun during your usual morning routine (go outside),\n"
                          "have a wonderful trip! :)\nbut by the time you get there you'll already be adapted, so no need for advice!")

            if direction == "west":
                plot.set_title(
                    label="just a little tip for your travel day:\ntry and get as little sun during your usual morning routine (wear some sunglasses),\n"
                          "have a wonderful trip! :)\nbut by the time you get there you'll already be adapted, so no need for advice!")

        while time_diff > 0 and day <= nights:
            if direction == "east":
                # recommended plan for the travelling day
                plot.set_title(
                    label="just a little tip for your travel day:\ntry and get as much sun during your usual morning routine (go outside),\n"
                          "have a wonderful trip! :)")

                # FOR BIOWAKE RECTANGLES
                temp_biowake = (biowake + time_diff) % 24

                w_ymax = temp_biowake + 2
                w_ymin = temp_biowake - 2
                if w_ymax > 24:
                    w_ymax = w_ymax - 24
                    wake1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, w_ymax, color='#ffe878')
                    plot.add_patch(wake1)
                    wake2 = matplotlib.patches.Rectangle(((day - 1), w_ymin), 1, (24 - w_ymin), color='#ffe878')
                    plot.add_patch(wake2)
                elif w_ymin < 0:
                    w_ymin = w_ymin + 24
                    wake1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, w_ymax, color='#ffe878')
                    plot.add_patch(wake1)
                    wake2 = matplotlib.patches.Rectangle(((day - 1), w_ymin), 1, (24 - w_ymin), color='#ffe878')
                    plot.add_patch(wake2)
                else:
                    wake = matplotlib.patches.Rectangle(((day - 1), w_ymin), 1, (w_ymax - w_ymin), color='#ffe878')
                    plot.add_patch(wake)

                # FOR BIOSLEEP RECTANGLES
                temp_biosleep = (biosleep + time_diff) % 24

                s_ymax = temp_biosleep + 4
                s_ymin = temp_biosleep - 4
                if s_ymax > 24:
                    s_ymax = s_ymax - 24
                    sleep1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, s_ymax, color='#005c77')
                    plot.add_patch(sleep1)
                    sleep2 = matplotlib.patches.Rectangle(((day - 1), s_ymin), 1, (24 - s_ymin), color='#005c77')
                    plot.add_patch(sleep2)
                elif s_ymin < 0:
                    s_ymin = s_ymin + 24
                    sleep1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, s_ymax, color='#005c77')
                    plot.add_patch(sleep1)
                    sleep2 = matplotlib.patches.Rectangle(((day - 1), s_ymin), 1, (24 - s_ymin), color='#005c77')
                    plot.add_patch(sleep2)
                else:
                    sleep = matplotlib.patches.Rectangle(((day - 1), s_ymin), 1, (s_ymax - s_ymin), color='#005c77')
                    plot.add_patch(sleep)

            elif direction == "west":
                # recommended plan for the travelling day
                plot.set_title(
                    label="just a little tip for your travel day:\ntry and get as little sun during your usual morning routine (wear some sunglasses),\n"
                          "have a wonderful trip! :)")

                # FOR BIOWAKE RECTANGLES
                temp_biowake = biowake - time_diff
                if temp_biowake < 0:
                    temp_biowake = temp_biowake + 24

                w_ymax = temp_biowake + 2
                w_ymin = temp_biowake - 2
                if w_ymax > 24:
                    w_ymax = w_ymax - 24
                    wake1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, w_ymax, color='#005c77')
                    plot.add_patch(wake1)
                    wake2 = matplotlib.patches.Rectangle(((day - 1), w_ymin), 1, (24 - w_ymin), color='#005c77')
                    plot.add_patch(wake2)
                elif w_ymin < 0:
                    w_ymin = w_ymin + 24
                    wake1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, w_ymax, color='#005c77')
                    plot.add_patch(wake1)
                    wake2 = matplotlib.patches.Rectangle(((day - 1), w_ymin), 1, (24 - w_ymin), color='#005c77')
                    plot.add_patch(wake2)
                else:
                    wake = matplotlib.patches.Rectangle(((day - 1), w_ymin), 1, (w_ymax - w_ymin), color='#005c77')
                    plot.add_patch(wake)

                # FOR BIOSLEEP RECTANGLES
                temp_biosleep = biosleep - time_diff
                if temp_biosleep < 0:
                    temp_biosleep = temp_biosleep + 24

                # exception for the day 1
                if day == 1:
                    s_ymax = temp_biosleep + 4
                    s_ymin = temp_biosleep - 4

                else:
                    s_ymax = temp_biosleep
                    s_ymin = temp_biosleep - 4

                if s_ymin < 0:
                    s_ymin = s_ymin + 24
                    sleep1 = matplotlib.patches.Rectangle(((day - 1), 0), 1, s_ymax, color='#ffe878')
                    plot.add_patch(sleep1)
                    sleep2 = matplotlib.patches.Rectangle(((day - 1), s_ymin), 1, (24 - s_ymin), color='#ffe878')
                    plot.add_patch(sleep2)
                # don't even need for max because it is just the temporary bio sleep
                else:
                    sleep = matplotlib.patches.Rectangle(((day - 1), s_ymin), 1, (s_ymax - s_ymin), color='#ffe878')
                    plot.add_patch(sleep)

            day = day + 1
            time_diff = time_diff - 1.5

        # check if there are still some days
        if time_diff <= 0 and day <= nights:
            # to cancel out the added one at the end of the previous while loop
            temp_day = day - 1
            day = day - 1

            while day <= nights:

                # THE BIOWAKE NATURAL RECTANGLE
                natural_biowake = matplotlib.patches.Rectangle((day, biowake), 1, 2, color='#ffe878')
                plot.add_patch(natural_biowake)

                # THE BIOSLEEP NATURAL RECTANGLE(S)
                if (biosleep + 4) > 24:
                    max = (biosleep + 4) - 24
                    natural_biosleep1 = matplotlib.patches.Rectangle((day, (biosleep - 4)), 1, (24 - (biosleep - 4)),
                                                                     color='#005c77')
                    plot.add_patch(natural_biosleep1)
                    natural_biosleep2 = matplotlib.patches.Rectangle((day, 0), 1, max, color='#005c77')
                    plot.add_patch(natural_biosleep2)

                elif (biosleep - 4) < 0:
                    min = (biosleep - 4) + 24
                    natural_biosleep1 = matplotlib.patches.Rectangle((day, min), 1, (24 - min), color='#005c77')
                    plot.add_patch(natural_biosleep1)
                    natural_biosleep2 = matplotlib.patches.Rectangle((day, 0), 1, (biosleep + 4), color='#005c77')
                    plot.add_patch(natural_biosleep2)
                else:
                    natural_biosleep = matplotlib.patches.Rectangle((day, (biosleep - 4)), 1, 8, color='#005c77')
                    plot.add_patch(natural_biosleep)

                day = day + 1

            # create a background rectangle to show the user is adapted during those days
            adapted = matplotlib.patches.Rectangle((temp_day, 0), (nights - temp_day), 24, linewidth=0, fill=None,
                                                   hatch='///')
            plot.add_patch(adapted)

        # place the travel bloc on top of the schedule for beginning of day 1
        if land != 0:
            travel = matplotlib.patches.Rectangle((0, 0), 1, land, color='#c1d7de')
            plot.add_patch(travel)
            plot.annotate('travelling\ntime', (0.1, land / 2), color="black", fontsize=10, va="center")

        # set axis limits and labels
        plot.set_xlim(0, nights)
        plot.set_ylim(0.0, 24.0)
        plot.set_xticks(range(nights))
        plot.set_xlabel("Days")
        plot.set_yticks(range(24))
        plot.set_ylabel("Hour of Day")

        plot.invert_yaxis()

        # set up the legend of the graph
        blue_patch = mpatches.Patch(color='#005c77', label='avoid exposing yourself to light, sleep is best!')
        yellow_patch = mpatches.Patch(color='#ffe878', label='try and get some sun, or at least some light!')
        hatch_patch = mpatches.Patch(hatch='///',
                                     label='by now you should have adapted to the timezone,\nso this schedule is just to keep up the good work!',
                                     fill=False)
        plot.legend(handles=[blue_patch, yellow_patch, hatch_patch])

        st.pyplot(fig)
