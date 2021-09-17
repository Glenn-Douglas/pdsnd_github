#!/usr/bin/env python
# coding: utf-8

# In[8]:


import sys
import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Input desired city please. Choose between Chicago, New York City, and Washington D.C. If choosing Washington D.C., enter "Washington".\n').lower()
    while (city.lower() not in ['new york city','chicago','washington']):
        city = input('Incorrect Entry. Please enter either new york city, chicago, or washington.\n').lower()
    print('\nYou selected {}'.format(city)+'.')

    # get user input for month (all, january, february, ... , june)
    month = input('Input desired month please (limited to first six months of the year). Enter "All" if you do not wish to filter by month.\n').lower()
    while (month.lower() not in ['january','february','march','april','may','june','all']):
        month = input('Incorrect Entry. Please enter January, February, March, April, May or June or All.\n ').lower()
    print('\nYou selected {}'.format(month)+'.')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Input desired day of the week please. Enter "All" if you do not wish to filter by day.\n').lower()
    while (day.lower() not in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']):
        day = input('Incorrect Entry. Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All.\n').lower()
    print('\nYou selected {}'.format(day)+'.')

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
    df = pd.read_csv(CITY_DATA.get(city.lower()))
    df['Month Name'] = (pd.to_datetime(df['Start Time'])).dt.month_name(locale='English')
    df['Weekday_Name'] = (pd.to_datetime(df['Start Time'])).dt.strftime("%A")
    if month.lower() != "all" and day.lower() != "all":
        df = df[(df['Month Name'] == str(month.title())) & (df['Weekday_Name'] == str(day.title()))]
    elif month.lower() != "all" and day.lower() == "all":
        df = df[df['Month Name'] == str(month.title())]
    elif month.lower() == "all" and day.lower() != "all":
        df = df[df['Weekday_Name'] == str(day.title())]
    else:
        df

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['Month Name'].unique()) > 1:
        print('The most common month for trips: '+ str((df['Month Name'].value_counts(ascending=False).nlargest(1)).index[0])
        + ' with ' + str((pd.DataFrame(df['Month Name'].value_counts(ascending=False).nlargest(1)).iat[0,0])) +'.')
    elif len(df['Month Name'].unique()) == 1:
        print('Most common month not relevant. The data frame was initially loaded with a filter on month.')

    # display the most common day of week
    if len(df['Weekday_Name'].unique()) > 1:
        print('The most common day for trips: '+ str((df['Weekday_Name'].value_counts(ascending=False).nlargest(1)).index[0])
        + ' with ' + str((pd.DataFrame(df['Weekday_Name'].value_counts(ascending=False).nlargest(1)).iat[0,0])) +'.')

    elif len(df['Weekday_Name'].unique()) == 1:
        print('Most common day not relevant. The data frame was initially loaded with a filter on weekday.')

    # display the most common start hour
    df['Hour'] = pd.DatetimeIndex(df['Start Time']).hour
    def hour_text (row):
        if row['Hour'] ==0:
            return 'midnight'
        elif row['Hour'] ==1:
            return '1:00 am'
        elif row['Hour'] ==2:
            return '2:00 am'
        elif row['Hour'] ==3:
            return '3:00 am'
        elif row['Hour'] ==4:
            return '4:00 am'
        elif row['Hour'] ==5:
            return '5:00 am'
        elif row['Hour'] ==6:
            return '6:00 am'
        elif row['Hour'] ==7:
            return '7:00 am'
        elif row['Hour'] ==8:
            return '8:00 am'
        elif row['Hour'] ==9:
            return '9:00 am'
        elif row['Hour'] ==10:
            return '10:00 am'
        elif row['Hour'] ==11:
            return '11:00 am'
        elif row['Hour'] ==12:
            return 'noon'
        elif row['Hour'] ==13:
            return '1:00 pm'
        elif row['Hour'] ==14:
            return '2:00 pm'
        elif row['Hour'] ==15:
            return '3:00 pm'
        elif row['Hour'] ==16:
            return '4:00 pm'
        elif row['Hour'] ==17:
            return '5:00 pm'
        elif row['Hour'] ==18:
            return '6:00 pm'
        elif row['Hour'] ==19:
            return '7:00 pm'
        elif row['Hour'] ==20:
            return '8:00 pm'
        elif row['Hour'] ==21:
            return '9:00 pm'
        elif row['Hour'] ==22:
            return '10:00 pm'
        elif row['Hour'] ==23:
            return '11:00 pm'
    hour_string = df.apply (lambda row: hour_text(row), axis=1)
    hour_string = pd.DataFrame(hour_string,columns=['hour_text'])
    df = df.join(hour_string,how='inner')
    print('The most common hour for trips: '+ str((df['hour_text'].value_counts(ascending=False).nlargest(1)).index[0])
        + ' with ' + str((pd.DataFrame(df['hour_text'].value_counts(ascending=False).nlargest(1)).iat[0,0])) +'.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common starting station: ' + str((df['Start Station'].value_counts(ascending=False).nlargest(1)).index[0])
          + ' with ' + str((pd.DataFrame(df['Start Station'].value_counts(ascending=False).nlargest(1)).iat[0,0])) +' trips.')

    # display most commonly used end station
    print('The most common ending station: ' + str((df['End Station'].value_counts(ascending=False).nlargest(1)).index[0])
          + ' with ' + str((pd.DataFrame(df['End Station'].value_counts(ascending=False).nlargest(1)).iat[0,0])) +' trips.')

    # display most frequent combination of start station and end station trip
    df['Trips'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most common trip from start to end: ' + str((df['Trips'].value_counts(ascending=False).nlargest(1)).index[0])
          + ' with ' + str((pd.DataFrame(df['Trips'].value_counts(ascending=False).nlargest(1)).iat[0,0])) +' trips.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ' + str(np.sum(pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time']))))
    # display mean travel time
    print('Mean travel time: ' + str(np.mean(pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time']))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #print(df['User Type'].value_counts())
    print('There were ' + str(pd.DataFrame(df['User Type'].value_counts()).iat[0,0]) + ' ' +
    str(pd.DataFrame(df['User Type'].value_counts()).index[0]) +'s' + ' and ' +
    str(pd.DataFrame(df['User Type'].value_counts()).iat[1,0])  + ' ' +
    str(pd.DataFrame(df['User Type'].value_counts()).index[1]) +'s.')

    # Display counts of gender

    if 'Gender' in df.columns:
        print('There were ' + str(pd.DataFrame(df['Gender'].value_counts()).iat[0,0]) + ' ' +
        str(pd.DataFrame(df['Gender'].value_counts()).index[0]) +'s' + ' and ' +
        str(pd.DataFrame(df['Gender'].value_counts()).iat[1,0])  + ' ' +
        str(pd.DataFrame(df['Gender'].value_counts()).index[1]) +'s.')
    # Display earliest, most recent, and most common year of birth
        print('The earliest birth year was ' + str(int(df['Birth Year'].min())) +'.')
        print('The most recent birth year was ' + str(int(df['Birth Year'].max())) +'.')
        print('The most common birth year was ' + str(int((df['Birth Year'].value_counts(ascending=False).nlargest(1)).index[0])) + '.')
    else:
        print('Gender and birth year data available only for Chicago and New York City.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        i = 0
        raw = input("\nWould you like to see first 5 rows of raw data? Type 'yes' or 'no'?\n").lower()
        pd.set_option('display.max_columns',200)
        while True:
            if raw.lower() == 'no':
                break
            elif raw.lower() != 'no' and raw != 'yes':
                raw = input('Incorrect entry. Please enter yes or no.\n')
            elif raw.lower() == 'yes':
                print(df[i:i+5])
                raw = input('\nWould you like to see the next rows 5 of raw data?\n').lower()
                i += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while True:
            if restart.lower() != 'no' and restart.lower() != 'yes':
                restart = input('Incorrect entry. Please enter yes or no.\n')
            elif restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                print('You have chosen to exit.')
                sys.exit(0)



if __name__ == "__main__":
    	main()


# In[ ]:
