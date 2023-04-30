import time
import pandas as pd
import numpy as np

from input_util import get_user_input

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
       city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
       if city in CITIES:
           break

    # get user input for month (all, january, february, ... , june)
    month = get_user_input('All right! now it\'s time to provide us a month name '\
                    'or just say \'all\' to apply no month filter. \n(e.g. all, january, february, march, april, may, june) \n> ', MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input('One last thing. Could you type one of the week day you want to analyze?'\
                   ' You can type \'all\' again to apply no day filter. \n(e.g. all, monday, sunday) \n> ', DAYS)

    print('-'*40)
    return city, month, day

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

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    # display the most common start hour

    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

def trip_duration_stats(df):
    # df = pd.read_csv(CITY_DATA[city])
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    # displaying counts of user types using value_counts() method
    print('\nCounts of user types: \n',df['User Type'].value_counts())

    # TO DO: Display counts of gender
    # displaying counts of gender using value_counts() method
    #handling any error would show up because 'washington' csv file has no Gender column
    try:
        print('\nCounts of gender: \n',df['Gender'].value_counts())
    except:
        print('\nSorry, Whasington has no "Gender" informations')

    # TO DO: Display earliest, most recent, and most common year of birth

    #displaying earliest, most recent, and most common year of birth
    #handling any error would show up because 'washington' csv file has no Birth Year column
    try:
        oldest=int(df['Birth Year'].min())
        youngest=int(df['Birth Year'].max())
        most=int(df['Birth Year'].mode())
        print('\nOldest User/Customer year of birth is: ',oldest)
        print('\nYoungest User/Customer year of birth is: ',youngest)
        print('\nMost common User/Customer year of birth is: ',most)
    except:
        print('\nSorry, Whasington has no "year of birth" informations')

def display_raw_data(city):
    """Show 5 records from the selected city.
    Asks user to type if he wants to show raw data or not

    Args:
        (df): the data frame of the selected city.
    Returns:
        Nothing.
    """
    df = pd.read_csv(CITY_DATA[city])
    answers = ['no','yes']
    user_input = ''

    #counter to use later in displaying raw data with df.head() method
    i = 0

    #if the user wants to see more records
    while user_input not in answers:
        print("\nDo you wanna see raw data records?")
        print("\nPlease type: Yes or No\n")
        user_input = input().lower()

        #displaying 5 records of raw data if user says yes using df.head() method
        if user_input == "yes":
            print(df.head())
        elif user_input not in answers:
            print("\nPlease enter a right answer.")

    #Another loop to ask the user if he wants more data to be displayed
    while user_input == 'yes':
        print("\nDo you wanna see MORE raw data records?\n")
        i += 5
        user_input = input().lower()
        #If yes -> display more 5 records, else -> break
        if user_input == "yes":
             print(df[i:i+5])
        elif user_input != "yes":
             break

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
        
    display_raw_data(city)


if __name__ == "__main__":
	main()
