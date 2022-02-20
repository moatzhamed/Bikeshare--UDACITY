from calendar import c, month
from json import load
from multiprocessing.sharedctypes import Value
import sys
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cityList = {"c": "chicago", "chicago": "chicago",
            "new york city ": "new york city", "w": "washington", "washington": "washington"}


def city_input():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input(
        "Please enter the required city from the below list :\nChicago - C \nNew York City - N \nWashington - W  ").lower()

    while city not in cityList:

        if city == "washington" or city == "w":
            print("\nWashington")
            return("washington")
        elif city == "new york city" or city == "n":
            print("\nnew york city")
            return("new york city")
        elif city == "chicago" or city == "c":
            print("\nChicago")
            return("chicago")
        else:
            print("\nThat's Invalid Input, select from the list:\nChicago - C \nNew York City - N \nWashington - W")
            city = input("select city ").lower()
    city = cityList[city]
    print(cityList[city])
    return(cityList[city])
    # else:
    #     print("\nThat's Invalid Input, select from the list:\nChicago - C \nNew York City - N \nWashington - W")
    #     sys.exit()


# TO DO: get user input for month (all, january, february, ... , june)
# Enter the month either in name or in digits
monthsName = {"All": "all",
              "1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June"}


def month_input():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    monthSelect = input(
        "\nSelect no for the month, to filter the slected city from the lsit :\nJanuary - 1\nFebruary - 2\nMarch - 3\nApril - 4\nMay - 5\nJune - 6\n or\n All for All months from Jan to June\n  ").title()
    tries = 4
    while monthSelect not in monthsName and tries > 0:
        tries -= 1
        if monthSelect not in monthsName:
            print("Not in the list, please try again")
            monthSelect = input("Select month ")
        else:
            print("Exist in the list")
    print(monthsName[monthSelect])
    month = monthsName[monthSelect]
    return(month)


# TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
dayList = ["All", "Saturday", "Sunday",
           "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def day_input():
    """
    Asks user to specify a day to analyze.
    Returns:
       (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    day = input("\nPlease enter the day name from the list: \nSaturday \nSunday \nMonday \nTuesday \nWednesday \nThursday \nFriday \nor \n All for All days\n").title()
    if day in dayList:
        print(day)
    else:
        print("Wrong Selection")
        # sys.exit()
    return(day)


print('-'*40)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
# filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = ['january', 'february', 'March', 'april', 'may', 'june']
        # month = months.index(month) + 1  # used in case of use dt.month in line 26, which gives integers insted of month name

        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
    else:
        month = ['january', 'february', 'March', 'april', 'may', 'june']
    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    else:
        day = ["Saturday", "Sunday", "Monday",
               "Tuesday", "Wednesday", "Thursday", "Friday"]
    # filter by combination of start & end station

    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent month:', popular_month)
   # TO DO:display the least month
    least_month = df['month'].value_counts().idxmin()
    print('least Frequent month:', least_month)
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent day:', popular_day)
    # TO DO:display the least common day of week
    least_day = df['day_of_week'].value_counts().idxmin()
    print('least Frequent day:', least_day)
    # TO DO: display the most common start hour
    popular_time = df['Start Time'].dt.hour.mode()[0]
    print('Most Frequent start time:', popular_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {start_station}")
    # TO DO: display least used start station
    least_start = df['Start Station'].value_counts().idxmin()
    print(f"The least used start station is: {least_start}")
    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {end_station}")
    # TO DO: display least used end station
    least_end = df['End Station'].value_counts().idxmin()
    print(f"The most commonly used end station is: {least_end}")
    # TO DO: display most frequent combination of start station and end station trip
    tripStations = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print(
        "The most most frequent combination of start station and end station trip is: {}".format(tripStations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travelTime = df['Trip Duration'].sum()
    print(
        f"The total travel time is: {travelTime} hours or {travelTime / 24} days")
    # TO DO: display mean travel time
    travelTimeAv = df['Trip Duration'].mean()
    print(
        f"The average travel time is: {travelTimeAv} hours or {travelTimeAv / 24} days")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    userCount = df['User Type'].value_counts()
    print(f"The count of user is:\n {userCount} users")
    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print(f"The count of gender is:\n {gender_count} ")
    except:
        print("No Avilable Data for Gender counts")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        common_birth = df['Birth Year'].mode()[0]
        print(f"The most commonly year of birth is: {common_birth}")
        earliest_birth = df['Birth Year'].min()
        print(f"The earliest year of birth is: {earliest_birth}")
        recent_birth = df['Birth Year'].max()
        print(f"The most recent year of birth is: {recent_birth}")
    except:
        print("No Avilable Data for Birth Date")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city = city_input()
        month = month_input()
        day = day_input()
        df = load_data(city, month, day)
        i = int(input("Please enter the no of rows "))
        more_data = input(
            f"Confirm you need To View the availbale data of {i} rows type: Yes or No if you don't want  ").title()
        while more_data == "Yes":

            i += 5
            if more_data != "Yes":
                print("Thank You")
            elif more_data == "Yes":
                print(df.head(i))
                more_data = input(
                    "To View the availbale data of 5 rows type: Yes or No if you don't want  ").title()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you")
            break


if __name__ == "__main__":
    main()
