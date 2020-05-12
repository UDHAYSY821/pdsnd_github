import time
import pandas as pd
import numpy as np


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
    city = input("Please Enter a city Name: ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Please Enter a Valid city Name: ").lower()
    # get user input for month (all, january, february, ... , june)
    month = input("Please Enter a Month Name or if you wish to see all the data enter 'all': ").lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input("Please Enter a Valid Month Name: ").lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please Enter a day of week or if you wish to see all the data enter 'all': ").lower()
    while day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday" , "sunday", "all"): 
        day = input("Please Enter Valid day of week: ").lower()
    print('-'*50)
    print("Loading Please wait.........")
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
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: {}".format(str(df['month'].mode().values[0])))

    # display the most common day of week
    print("The most common day of the week: {}".format(str(df['day_of_week'].mode().values[0])))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour: {}".format(str(df['start_hour'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {} ".format(df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print("The most common end station is: {}".format(df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    print("The most common start and end station combo is: {}".format(df['routes'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("The total travel time is: {}".format(str(df['duration'].sum())))

    # display mean travel time
    print("The mean travel time is: {}".format(str(df['duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here are the counts of various user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print("Here are the counts of gender:")
        print(df['Gender'].value_counts())


        # Display earliest, most recent, and most common year of birth
        print("The earliest birth year is: {}".format(str(int(df['Birth Year'].min()))))
        print("The latest birth year is: {}".format(str(int(df['Birth Year'].max()))))
        print("The most common birth year is: {}".format(str(int(df['Birth Year'].mode().values[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Iterate through 5 entries at a time.
    Returns:
        Print five row entries of data to terminal
    """

    show_more = 'yes'
    while show_more == 'yes':
        for i in df.iterrows():
            count = 0
            while count < 5:
                print(i)
                count += 1
            response = input('\nView 5 more data entries? Yes or No?\n')
            if response.lower() == 'no':
                show_more = 'no'
                break

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        while True:
            select_data = input("\nPlease select the information you would like to obtain.\n\n [ts]  Time Stats\n [ss] "
                                 " Station Stats\n [tds] Trip Duration Stats\n "
                                 "[us]  User Stats\n"
                                 " [rd]  View Raw_Data\n"
                                 " [rs]  Restart or exit"
                                 "\n\nPlease enter your value here:")          
            while select_data not in ['ts', 'ss', 'tds','us','rd','rs']:
                select_data = input("\nPlease enter a valid input from the below.\n\n [ts]  Time Stats\n [ss] "
                                 " Station Stats\n [tds] Trip Duration Stats\n "
                                 "[us]  User Stats\n"
                                 " [rd]  View Raw_Data\n"
                                 " [rs]  Restart or exit"
                                 "\n\nPlease enter your value here:") 
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':                       
                station_stats(df)
            elif select_data == 'tds':                          
                trip_duration_stats(df)
            elif select_data == 'us':                        
                user_stats(df, city)
            elif select_data == 'rd':
                raw_data(df)
            elif select_data == 'rs':
                break      
       

        restart = input('\nWould you like to restart? Enter yes to exit enter no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()