import time, datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():

    city = None
    month = None
    day = None

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cities = ["Chicago", "New York City", "Washington"]
    periods = ["month", "day", "none"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]
    months = ["January", "February", "March", "April", "May", "June", "All"]
    user_input = None
    period = None
 
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        try:
            user_input = str(input("Would you like to see data for Chicago, New York City, or Washington?").title())
        except ValueError:
            print ('The provided value is not a valid string')
        if user_input in cities:
            print('You selected to see the data for:\n{}'.format(user_input))
            city = user_input
            break
        else:
                print("Please check your spelling. We don't have that city in our database.")
       
        
    while True:

        try:
            period = input("Would you like to filter the data by month, day, or not at all? Type ""none"" for no time filter.").lower()
        except ValueError:
            print ('The provided value is not a valid string')
        if period not in periods:
            print("Please check your spelling.")
        
         # get user input for month (all, january, february, ... , june)
        elif period == "month":
            
            while True:

                try:
                    month = input("Which month - January, February, March, April, May, June or all?").title()
                except ValueError:
                    print ('The provided value is not a valid string')
                if month not in months:
                    print("Please check your spelling. You can choose from Jan to Jun or All")
                else:
                    month = month
                    break
            break
        
        # get user input for day of week (all, monday, tuesday, ... sunday)    
        elif period == "day":
            
            while True:
                try:
                    day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?").title()
                except ValueError:
                    print ('The provided value is not a valid string')
                if day not in days:
                    print("Please check your spelling. You can choose from Mon to Sun or All")
                else:
                    day = day
                    break
            break
        
        elif period == "none":
            
            day = None
            month = None
            break

    print('-'*40)
    return city, month, day

#city, month, day = get_filters()

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
    df = pd.read_csv(CITY_DATA[city.lower()])
    df["Start Time"]=pd.to_datetime(df["Start Time"])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != None and month !="All":
        df = df[df['month'] == month]
    elif day != None and day !="All":
        df = df[df['day_of_week'] == day]
    else: 
        df = df
    return df

#df = load_data(city, month, day)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Hour:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Start Hour:', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = str(df.value_counts(['Start Station','End Station']).idxmax())
    print('Most frequent combination of start station and end station trip:',popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time  = df['Trip Duration'].sum(axis=0)
    total = datetime.timedelta(seconds = float(total_travel_time))
    print("Total travel time:", total)

    # display mean travel time
    mean_travel_time  = df['Trip Duration'].mean(axis=0)
    mean = datetime.timedelta(seconds = float(mean_travel_time))
    print("Mean travel time:", mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:\n", user_types, "\n")

    # Display counts of gender
    if city != 'Washington':
        user_genders = df['Gender'].value_counts()
        print("Counts of gender:\n",user_genders, "\n")

    # Display earliest, most recent, and most common year of birth
        min_year = int(df['Birth Year'].min())
        max_year = int(df['Birth Year'].max())
        mode_year = int(df['Birth Year'].mode())
        print("Earliest year of birt entered: {}, most recent: {} and most common year was: {}".format(min_year, max_year, mode_year))
    else:
        return

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
    
        while True:
            restart = str(input('\nWould you like to restart? Enter yes or no.\n')).lower()
            if restart not in ("yes", "no"):
                print('Please try again.')
            elif restart == "yes":
                break   
            else:
                return True
      
               

if __name__ == "__main__":
	main()
