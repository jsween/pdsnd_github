import math
import os
import time
import pandas as pd
import numpy as np
from scipy import stats

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = {'january': 1,
          'february': 2,
          'march': 3,
          'april': 4,
          'may': 5,
          'june': 6,
          'all': -1}
DAYS = {'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'all': -1}


def get_city():
    """
    Asks user to specify city to analyze.

    Returns:
        (str) selected_city - name of the city to analyze
    """
    selected_city = None
    while selected_city not in CITY_DATA.keys():
        selected_city = input('Please select a city: '
                              'Chicago, New York City or '
                              'Washington\n').lower()

        if selected_city in CITY_DATA.keys():
            return selected_city
        else:
            print(f'{selected_city} is not available. '
                  'Please try selecting again.\n')


def get_month():
    """
    Asks user to specify month to analyze.

    Returns:
        (str) selected_month - name of the month to filter by,
        or "all" to apply no month filter
    """
    selected_month = None
    while selected_month not in MONTHS.keys():
        selected_month = input('Please select a month: '
                               'January, February, March, April, May, June, '
                               'or all\n').lower()

        if selected_month in MONTHS.keys():
            return selected_month
        else:
            print(f'{selected_month.capitalize()} is not available. '
                  'Please try selecting again.\n')


def get_day_of_week():
    """
    Asks user to specify day to analyze.

    Returns:
        (str) selected_day - name of the day of week to filter by,
                             or "all" to apply no day filter
    """
    selected_day = None
    while selected_day not in DAYS.keys():
        selected_day = input('Please select a day of the week: Sunday,'
                             ' Monday, Tuesday, Wednesday, '
                             'Thursday, Friday, Saturday, or all\n').lower()

        if selected_day in DAYS.keys():
            return selected_day
        else:
            print(f'{selected_day.capitalize()} is not available. '
                  'Please try selecting again.\n')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
                      or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
                    or "all" to apply no day filter
    """
    os.system('clear')
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day_of_week()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
                      or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
                    or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(f'data/{CITY_DATA[city]}')
    df_copy = df.copy()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['DayOfWeek'] = df['Start Time'].dt.weekday

    if month != 'all':
        df[df['Month'] == MONTHS[month]]

    if day != 'all':
        df[df['DayOfWeek'] == DAYS[day]]

    return df, df_copy


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month != 'all':
        print(f'Selected Month: {month.capitalize()}')
    else:
        month_index = df['Month'].value_counts().idxmax()
        print('Month: '
              f'{list(MONTHS.keys())[list(MONTHS.values()).index(month_index)].capitalize()}')

    # display the most common day of week
    if day != 'all':
        print(f'Selected Day: {day.capitalize()}')
    else:
        day_index = df['DayOfWeek'].value_counts().idxmax()
        print('Day of Week: '
              f'{list(DAYS.keys())[list(DAYS.values()).index(day_index)].capitalize()}')

    # display the most common start hour
    df['StartHour'] = df['Start Time'].dt.hour
    print(f'Start Hour: {df["StartHour"].value_counts().idxmax()}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Common Start Station: '
          f'{df["Start Station"].value_counts().idxmax()}')

    # display most commonly used end station
    print('Most Common Start Station: '
          f'{df["End Station"].value_counts().idxmax()}')

    # display most frequent combination of start station and end station trip
    df['StartEndCombo'] = df['Start Station'] + ' and ' + df['End Station']
    print('Most Common Start & End Combination: '
          f'{df["StartEndCombo"].value_counts().idxmax()}')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_minutes = df['Trip Duration'].sum() / 60
    sum_hours = math.floor(sum_minutes / 60)
    minutes = round(sum_minutes % sum_hours)
    print(f'Total Travel Time: {sum_hours} hour(s) and {minutes} minute(s)')

    # display mean travel time
    mean_minutes = df['Trip Duration'].mean() / 60
    if mean_minutes >= 60:
        mean_hours = math.floor(mean_minutes / 60)
        print(f'Mean Travel Time: {mean_hours} hour(s) and '
              f'{mean_minutes % mean_hours} minute(s)')
    else:
        print(f'Mean Travel Time: {round(mean_minutes, 2)} minute(s)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].values

    sum_subscriber = (user_type == 'Subscriber').sum()
    sum_customer = (user_type == 'Customer').sum()
    sum_dependent = (user_type == 'Dependent').sum()

    print(f'Total Subscriber Users: {sum_subscriber}')
    print(f'Total Customer Users: {sum_customer}')
    if city == 'chicago':
        print(f'Total Dependent Users: {sum_dependent}')

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        # gender
        user_gender = df['Gender'].values

        sum_male = (user_gender == 'Male').sum()
        sum_female = (user_gender == 'Female').sum()

        print(f'Total Male Users: {sum_male}')
        print(f'Total Female Users: {sum_female}')

        # birth data
        birth_year = df['Birth Year'].values
        cleaned_birth_year = birth_year[~np.isnan(birth_year)]
        unique_birth_year = np.unique(cleaned_birth_year)

        print(f'Earliest Birth Year: {int(unique_birth_year.min())}')
        print(f'Most Recent Birth Year: {int(unique_birth_year.max())}')
        print('Most Common Birth Year: '
              f'{int(stats.mode(cleaned_birth_year, keepdims=True)[0])}')
    else:
        print('\nWARNING: No Gender or Age Data available for Washington')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def display_raw_data(raw_df):
    """
    Displays the raw data upon the user's request
    """
    i = 1
    display_data = input('\nWould you like to view the first 5 lines of raw '
                         'data? Enter "y" or "n".\n').lower()
    while display_data == 'y' or display_data == 'yes':
        print(raw_df[i:i+5])
        i += 5
        display_data = input('\nWould you like to see the next 5 lines?'
                             ' Enter "y" or "n".\n')


def main():
    while True:
        city, month, day = get_filters()
        df, raw_df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(raw_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
