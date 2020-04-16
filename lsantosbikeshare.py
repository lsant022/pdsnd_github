#source https://stackoverflow.com/questions/55719762/how-to-calculate-mode-over-two-columns-in-a-python-dataframe
#source https://stackoverflow.com/questions/31037298/pandas-get-column-average-mean
# view all columns https://towardsdatascience.com/how-to-show-all-columns-rows-of-a-pandas-dataframe-c49d4507fcf
# datetime columns https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime
# IN PROGESS WORKING ON REPO @ https://github.com/lsant022/pdsnd_github


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
WEEKDAY_DATA = {0: 'all', 1: 'sunday', 2: 'monday', 3: 'tuesday', 4: 'wednesday', 5: 'thursday', 6: 'friday', 7: 'saturday'}
SCOPE_LIST = {'both','day','month'}

GET_DAY_CHECK = ['0','1','2','3','4','5','6','7']

def get_data():
    get_city = ''
    while get_city.lower() not in CITY_DATA:
        get_city = input("Please enter the city you would like to review from the following options: Chicago, New York City, Washington:   ")
        if get_city.lower() in CITY_DATA:
            city = CITY_DATA[get_city.lower()]
        else:
             print("\nInvalid selection, please try again\n")

#check for scope
    scope = ""
#check for correct response
    while scope.lower() not in SCOPE_LIST:
        scope = input("Would you like to review by Month, Day or Both? Please type your option     ")
        if scope.lower() in SCOPE_LIST:
            break
        else:
            print("\nInvalid selection, please try again\n")

    if scope.lower() == "month":
        get_month = ""
        while get_month.lower() not in MONTH_DATA:
            get_month = input("Which month would you like to review (Type 'All' to view all): January, February, March, April, May, June   ")
            if get_month.lower() in MONTH_DATA:
                month = get_month.lower()
                get_day = 0
                day = WEEKDAY_DATA[get_day]
            else:
                 print("\nInvalid selection, please try again\n")

    if scope.lower() == "day":
        month = 'all'
        get_day = -1
        while get_day not in WEEKDAY_DATA:
            get_day = input("Which day would you like to review? Please Select a number: \n For no filter select 0 for Sunday = 1 etc.....")
            if get_day in GET_DAY_CHECK:
                get_day = int(get_day)
                if get_day >= 0 and get_day <= 7:
                    day = WEEKDAY_DATA[get_day]

    if scope.lower() == 'both':
        get_month = ""
        while get_month.lower() not in MONTH_DATA:
            get_month = input("Which month would you like to review (Type 'All' to view all): January, February, March, April, May, June   ")
            if get_month.lower() in MONTH_DATA:
                month = get_month.lower()
            else:
                 print("\nInvalid selection, please try again\n")
            get_day = -1
        while get_day not in WEEKDAY_DATA:
            get_day = input("Which day would you like to review? Please Select a number: \n For no filter select 0 for Sunday = 1 etc.....")
            if get_day in GET_DAY_CHECK:
                get_day = int(get_day)
                if get_day >= 0 and get_day <= 7:
                    day = WEEKDAY_DATA[get_day]
            else:
                print("\nInvalid selection, please try again\n")

    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df.loc[df['Month'] == month.title()]

    if day != 'all':
        df = df.loc[df['Day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # Improved code to eliminate redundancy when selecting month in scope
    # e.g. if June is select, most common month is June
    # cleaned code to run only of 'all' is selected.
    if month == "all":
        common_month = df['Month'].mode()[0]
        print("The most common month for your inquiry is {}".format(common_month))

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print("The most common day of the week for your inquiry is {}".format(common_day))


    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    if common_hour >= 13:
        common_hour -= 12
        print("The most common hour for your inquiry is {}:00PM".format(common_hour))
    else:
        print("The most common hour for your inquiry is {}:00AM".format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    cmn_start_station = df['Start Station'].mode()[0]
    print("Most commonly used Start Station is: {}".format(cmn_start_station))


    # display most commonly used end station
    cmn_end_station = df['End Station'].mode()[0]
    print("Most commonly used End Station is: {}".format(cmn_end_station))


    # display most frequent combination of start station and end station trip
    # Edited: Fixed captialization of string.
    combination = (df['Start Station'] + " <> " + df['End Station']).mode()[0]
    print("Most commonly used combination of Start Station and End Station trip  is: {}".format(combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time for your inquiry is: {} hours".format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("The average travel time for your inquiry is: {} hours".format(avg_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n")
    print(str(user_types)+"\n")
    # Display counts of gender
    #code crashes if Washington is selected
    if city != 'washington.csv':
        gender_types = df['Gender'].value_counts()
        print("Counts of Gender:\n")
        print(str(gender_types)+"\n")

        # Display earliest, most recent, and most common year of birth
        recent_dob = df['Birth Year'].min()
        earliest_dob = df['Birth Year'].max()
        mean_dob = df['Birth Year'].mean()
        print("Oldest bikeshare user was born in {}".format(int(recent_dob)))
        print("Youngest bikeshare user was born in {}".format(int(earliest_dob)))
        print("Average bikeshare user was born in {}".format(int(mean_dob)))


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def view_data(df):

    user_input = ""
    i = 0
    while user_input.lower() != 'quit' or user_input.lower() != 'q':
        user_input = input("Would you like to see a few rows? Type Yes to continue or Type Quit or Q to end:")
        if user_input.lower() == 'yes':
            print(df.iloc[i:i+5])
            i += 5
        elif user_input.lower() == 'q' or user_input.lower() == 'quit':
            break
        else:
            print("\nInvalid selection, please try again\n")

def main():
    while True:
        city, month, day = get_data()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        pd.set_option('display.max_columns', None)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
