import time
import pandas as pd
import numpy as np
import csv
from itertools import islice

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filter(category_name, cat_list):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        cat_input - name to filter the category by
    """
    while True:
        try:
            # Request category and provide options
            cat_input = str(input("Please enter a {0} ({1}): ".format(category_name, ', '.join(cat_list))))
            
            # Test that the category is one of the options that can be accepted
            if cat_input.lower() in [category.lower() for category in cat_list]:
                # Exit loop once we have category
                break
            else:
                # Unknown input
                print("I don't know that {}".format(category_name))
                                   
        except:
            # For any unexpected input, number, etc.
            print("I don't understand what you entered.")
            # Return to the start of the input loop
            continue

    return cat_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get list of acceptable inputs for each variable
    city_list = CITY_DATA.keys()
    month_list = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
    day_list = ["All","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    city = get_filter("city", city_list)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_filter("month", month_list)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter("day", day_list)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):    
    """
    Adopted directly from practice problem 3 per recommendation
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

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # Re-initialize months variable due to local scope
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # Get most popular month
    popular_month = df['month'].mode()[0]
    # Display
    print("Most frequent month: {}".format(months[popular_month - 1].title()))

    # TO DO: display the most common day of week
    # Get most popular day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    # Display
    print("Most frequent day of week: {}".format(popular_day_of_week))

    # TO DO: display the most common start hour
    # Get most popular hour
    popular_hour = df['hour'].mode()[0]
    # Convert to 12 hour clock
    if popular_hour == 0:
        period = "AM"
        popular_hour_12 = 12
    elif popular_hour > 12:
        period = "PM"
        popular_hour_12 = popular_hour - 12
    elif popular_hour == 12:
        period = "PM"
        popular_hour_12 = popular_hour
    else:
        period = "AM"
        popular_hour_12 = popular_hour
    # Display
    print("Most frequent starting hour: {0} {1}".format(popular_hour_12, period))
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # Get most popular start station
    popular_start = df['Start Station'].mode()[0]
    # Display
    print("Most commonly used start station: {}".format(popular_start))

    # TO DO: display most commonly used end station
    # Get most popular start station
    popular_end = df['End Station'].mode()[0]
    # Display
    print("Most commonly used end station: {}".format(popular_end))

    # TO DO: display most frequent combination of start station and end station trip
    # concatenate start and end then take mode
    popular_start_end = ("From " + df['Start Station'] + " to " + df['End Station']).mode()[0]
    # Display
    print("Most frequent combination of start station and end station trip: {}".format(popular_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Source: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
def seconds_to_dhms(seconds):
    """Takes in seconds integer and returns days + hours + minutes + seconds string"""
    # Total minutes and seconds remainder
    m, s = divmod(seconds, 60)
    # Total hours and minutes remainder
    h, m = divmod(m, 60)
    # Total days and hours remainder
    d, h = divmod(h, 24)
    
    # Old-style string formatting
    return "%d days %d hours %02d minutes %02d seconds" % (d, h, m, s)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Get total travel time
    total_travel_seconds = df['Trip Duration'].sum()
    # Display
    print("Total travel time is {}".format(seconds_to_dhms(total_travel_seconds)))

    # TO DO: display mean travel time
    mean_travel_seconds = df['Trip Duration'].mean()
    # Display
    print("Average travel time is {}".format(seconds_to_dhms(mean_travel_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # Get user type counts
    user_types = df['User Type'].value_counts()
    # Display
    print("Count of user trips by user type\n{}".format(user_types.to_string()))
    # Get relative user type counts
    user_types_relative = df['User Type'].value_counts(normalize = True)
    print("Please note that gender and age demographics are only available for subscribers, who make up {0:.0%} of trips.".format(user_types_relative[0]))
    
    # TO DO: Display counts of gender
    # Test for presence of column
    if 'Gender' in df.columns:
        # Get gender counts
        gender_cnt = df['Gender'].value_counts()
        # Display
        print("Count of user trips by gender\n{}".format(gender_cnt.to_string()))
    else:
        print("No gender statistics available for this city")
    # TO DO: Display earliest, most recent, and most common year of birth
    # Test for presence of column
    if 'Birth Year' in df.columns:
        # Get min birth year
        birth_year_min = int(df['Birth Year'].min())
        # Get max birth year
        birth_year_max = int(df['Birth Year'].max())
        # Get most common birth year
        birth_year_mode = int(df['Birth Year'].mode()[0])
        print("Earliest birth year: {0}\nLatest birth year: {1}\nMost common birth year: {2}".format(birth_year_min, birth_year_max, birth_year_mode))
    else:
        print("No birth year statistics available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rawdata_viewer(city):
    """Allow user to review unfiltered raw data for selected city 5 lines at a time"""

# Source: https://coderwall.com/p/5vi8ca/use-python-to-read-file-by-n-lines-each-time
def next_n_lines(file_opened, N):
    """Use generator to return the next 5 lines of an open file with each function call"""
    return [x.strip() for x in islice(file_opened, N)]
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)        
            
        raw_cycle = input('\nWould you like to see the unfiltered city data? Enter yes or no.\n')
        if raw_cycle.lower() == 'yes':
            # load file
            with open(CITY_DATA[city]) as csv_file:
                while True:
                    # Call generator function to capture next 5 lines
                    nextlines = next_n_lines(csv_file, 5)
                    # Print the lines separately
                    for line in nextlines:
                        print(line)
                    # Prompt for exit
                    keep_reading = input('\nDisplay the next 5 lines? Enter yes or no.\n')
                    if keep_reading.lower() != 'yes':
                        break
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
