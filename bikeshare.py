#import necessary packages
import time
import pandas as pd
import numpy as np

#define data sources
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    month = None
    day = None
    while True:
        city = input('Which city would you like to take a closer look at? Please enter chicago, new york city, or washington: ')
        city = city.lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('Sorry, I did not understand that.')
            continue
        else:
            print('Great! We\'ll look at bikeshare data from {}.'.format(city))
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Do you want to look at one month in particular, or all months? Please enter all, january, february, march, april, may, or june: ')
        month = month.lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print('Sorry, I did not understand that.')
            continue
        elif month == 'all':
            print('Okay, we will look at all the data from january through june.')
            break
        else:
            print('Okay, we will focus on data from {}.'.format(month))
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Do you want to look at a single day, or every day? Please enter all, sunday, monday, tuesday, wednesday, thursday, friday, or saturday: ')
        day = day.lower()
        if day not in ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            print('Sorry, I did not understand that.')
            continue
        elif day == 'all' and month == 'all':
            print('Here we go! We\'ll look at stats from {}, for every day in january through june!'.format(city))
            break
        elif day == 'all':
            print('Here we go! We\'ll look at stats from {}, for every day in {}!'.format(city, month))
            break
        else:
            print('Here we go! We\'ll look at stats from {}, but only from {}\'s in {}.'.format(city, day, month))
            break

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

    # extract month and day of week from Start Time to create new columns
    df.insert(1, 'month', df['Start Time'].dt.month)
    df.insert(2, 'day_of_week', df['Start Time'].dt.weekday_name)
    df.insert(3, 'hour', df['Start Time'].dt.hour)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month for use is: {}".format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print("The most common day for use is: {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print("The most common start hour for use is: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most commonly used end station is: {}".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip

    df.insert(8, 'trip', (df['Start Station'] + ' to ' + df['End Station']))
    print("The most frequent combination of start and end station is: {}.".format(df['trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = (df['Trip Duration'].sum())/60
    print("Bikes were used for a total of {} minutes during the window of interest.".format(total_time))

    # TO DO: display mean travel time
    mean_time = (df['Trip Duration'].mean())/60
    print("Each trip lasted {} minutes on average.".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("There were {} subscriber and {} customer users.".format((df['User Type'].value_counts()['Subscriber']), (df['User Type'].value_counts()['Customer'])))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("There were {} male and {} female users.".format((df['Gender'].value_counts()['Male']), (df['Gender'].value_counts()['Female'])))


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("The oldest user was born in {}.".format(int(df['Birth Year'].min())))
        print("The youngest user was born in {}.".format(int(df['Birth Year'].max())))
        print("The most common year of birth for users was {}.".format(int(df['Birth Year'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_display(df):
    """Displays 5 lines of raw data at a time, per user's request."""
    answer = None
    answer = input("Would you like to look at some of the raw data behind these statistics? Enter yes or no: ")
    count = 0
    while True:
        if answer == 'yes':
            print(df[:][count:(count+5)])
            count += 5
        elif answer == 'no':
            break
        else:
            print('Sorry, I didn\'t understand that.')
            continue
        answer = input('Would you like to see 5 more rows of data? Enter yes or no: ')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
