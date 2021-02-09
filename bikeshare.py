import time
import pandas as pd

# global variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city
    while True:
        try:
            city = input('Please enter the city you wish to analyze: Chicago, New York City, Washington: ')
            if city.lower() in CITY_DATA:
                city = city.lower()
                break
            else:
                print('There is no data for the city you entered.')
        except Exception as e:
            print("Exception occurred: {}".format(e))

    # get user input for filter
    while True:
        try:
            filter = input('Do you want to filter by [m]onth, [d]ay, [b]oth or [n]one? ')
            if filter in ['m','d','b','n']:
                break
        except Exception as e:
            print("Exception occurred: {}".format(e))

    # get user input for month
    if filter in ['m','b']:
        while True:
            try:
                month = input('Please enter the month you wish to filter by (January - June): ')
                if month.lower() in MONTHS:
                    month = MONTHS.index(month.lower()) + 1 # use the index of the months list to get the corresponding int
                    break
            except Exception as e:
                print("Exception occurred: {}".format(e))
    elif filter in ['d','n']:
        month = 'all'

    # get user input for day of week
    if filter in ['d','b']:
        while True:
            try:
                day = input('Please enter the weekday you wish to filter by (Monday - Sunday): ')
                if day.title() in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']:
                    day = day.title()
                    break
            except Exception as e:
                print("Exception occurred: {}".format(e))
    elif filter in ['m','n']:
        day = 'all'

    print('\n')
    return city, month, day


#load data
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


# compute the mode and corresponding count of a data frame column
def get_mode_count(df):
    """
    Computes the mode and the count of the mode from an array.

    Args:
    df - data fram with ONE column

    Returns:
    df_mode - mode of the column
    df_mode_count - count for that mode

    """
    # calculate the mode and its count from the input data fram (with one column)
    df_value_counts = df.value_counts()
    df_mode = df_value_counts.index[0]
    df_mode_count = df_value_counts.iloc[0]

    return df_mode, df_mode_count


# calculate time statistics
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    start_time = time.time()

    print('\n','-'*40,'\n\nTravel time statistics:\n')
    # display the most common month
    month_popular, month_popular_count = get_mode_count(df['month'])
    print('Most popular month: {}\nCount: {}\n'.format(MONTHS[month_popular-1].title(),month_popular_count))

    # display the most common day of week
    day_popular, day_popular_count = get_mode_count(df['day_of_week'])
    print('Most popular day: {}\nCount: {}\n'.format(day_popular,day_popular_count))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_popular, hour_popular_count = get_mode_count(df['hour'])
    print('Most popular hour: {}\nCount: {}\n'.format(hour_popular,hour_popular_count))

    print("These calculations took %s seconds.\n" % (time.time() - start_time))


# calculate station statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()

    print('\n','-'*40,'\n\nStation statistics:\n')
    # display most commonly used start station
    start_station_popular, start_station_popular_count = get_mode_count(df['Start Station'])
    print('Most popular start station: {}\nCount: {}\n'.format(start_station_popular,start_station_popular_count))

    # display most commonly used end station
    end_station_popular, end_station_popular_count = get_mode_count(df['End Station'])
    print('Most popular end station: {}\nCount: {}\n'.format(end_station_popular,end_station_popular_count))

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' --> ' + df['End Station']
    comb_station_popular, comb_station_popular_count = get_mode_count(df['Station Combination'])
    print('Most popular combination of stations: {}\nCount: {}\n'.format(comb_station_popular,comb_station_popular_count))

    print("These calculations took %s seconds.\n" % (time.time() - start_time))


#calculate trip duration statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()

    print('\n','-'*40,'\n\nTravel duration statistics:\n')
    # total travel time
    total_duration = df['Trip Duration'].sum()
    if total_duration/60/60/24/365 > 1:
        total_duration = total_duration/60/60/24/365
        unit = 'years'
    elif total_duration/60/60/24/7 > 1:
        total_duration = total_duration/60/60/24/7
        unit = 'weeks'
    elif total_duration/60/60/24 > 1:
        total_duration = total_duration/60/60/24
        unit = 'days'
    elif total_duration/60/60 > 1:
        total_duration = total_duration/60/60
        unit = 'hours'
    else:
        total_duration = total_duration/60
        unit = 'minutes'

    print('Total travel time: {0:.2f} {1:s}'.format(total_duration, unit))

    # mean travel time in seconds and minutes
    mean_duration_sec = df['Trip Duration'].mean()
    mean_duration_minutes = mean_duration_sec/60

    print('Average travel time: {0:.2f} minutes\n'.format(mean_duration_minutes))

    print("These calculations took %s seconds.\n" % (time.time() - start_time))


# calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    start_time = time.time()

    print('\n','-'*40,'\n\nUser statistics:\n')
    # Display counts of user types
    usertype_counts = df['User Type'].value_counts()
    print('Subscribers: {}\nCustomers: {}\n'.format(usertype_counts['Subscriber'], usertype_counts['Customer']))

    # Display counts of gender
    gender_counts = df['Gender'].value_counts()
    print('Male users: {}\nFemale users: {}\n'.format(gender_counts['Male'], gender_counts['Female']))

    # Display earliest, most recent, and most common year of birth
    birthyear_max = int(df['Birth Year'].max())
    birthyear_min = int(df['Birth Year'].min())
    birthyear_mode = int(df['Birth Year'].mode()[0])

    print('Oldest user born in: {}\nYoungest user born in: {}\nMost users born in: {}\n'.format(birthyear_min,birthyear_max,birthyear_mode))

    print("These calculations took %s seconds.\n" % (time.time() - start_time))


# display raw data
def raw_data(df,block):
    """
    Displays 5 lines of raw data.
    Args:
    df - data frame to be used for display of raw data
    block - the display begins at row no. = (block-1)*5
    """
    for i in range((block-1)*5,block*5): # go through blocks of 5 lines
        print('--'*5,'\n\n')
        for j in range(1,len(df.columns)-4):  # go through all columns except the 4 ones added during the script
            print(df.columns[j],': ',df.iloc[i][j])
        print('\n')


# main script
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('Your calculations will be based on {} lines of data.'.format(df.size))
        input("Press Enter to continue...")
        time_stats(df)
        input("Press Enter to continue...")
        station_stats(df)
        input("Press Enter to continue...")
        trip_duration_stats(df)
        if city != 'washington':
            input("Press Enter to continue...")
            user_stats(df)
        block = 0  # set the first line of raw data display to 0
        while True:
            try:
                restart = input('\nWould you like to see raw data, yes or no? ')
                if restart.lower() not in ['no','yes','n','y']:
                    print('\nPlease enter yes or no.')
                elif (restart.lower() in ['yes','y']) and (block <= df.size/5):
                    block += 1
                    raw_data(df,block)
                elif (restart.lower() in ['no','n']) or (block > df.size/5):
                    break
            except Exception as e:
                print("Exception occurred: {}".format(e))
        while True:
            try:
                restart = input('\nWould you like to analyse more data, yes or no? ')
                if restart.lower() not in ['no','yes','n','y']:
                    print('\nPlease enter yes or no.')
                elif restart.lower() in ['no','yes','n','y']:
                    break
            except Exception as e:
                print("Exception occurred: {}".format(e))
        if restart.lower() in ['no','n']:
            break

if __name__ == "__main__":
	main()
