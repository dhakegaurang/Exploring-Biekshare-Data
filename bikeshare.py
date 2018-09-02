import time
import pandas as pd
import re
import glob
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', -1)

#from dask.array.ufunc import equal
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_OBJ = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'novermber':11,'december':12}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Getting user input for city (chicago, new york city, washington)
    city=""
    while True:
        city = input("\nPlease name of the city (chicago, new york city, washington) to filter by or 'all' for no filter:")
        city_str_len = len(re.search('[a-zA-Z ]+',city,0).group()) if re.search('[a-zA-Z ]+',city,0) != None else 0         
        
        if (len(city) == city_str_len):
            if (CITY_DATA.get(city) != None or city == "all"):
                break
            else:
                print("Error: Make sure you enter correct spelling of city!!\n")
        else:
            print("Error: Please enter only alphabets for city as input!!\n")
        
    
    #Getting user input for month (all, january, february, ... , june)
    month = ""
    while True:
        month = input("\nPlease enter month (january, february, ... ) to filter by or 'all' for no filter: \n")
        month_str_len = len(re.search('[a-zA-Z ]+',month,0).group()) if re.search('[a-zA-Z ]+',month,0) != None else 0  
        if len(month) == month_str_len:
            if (MONTH_OBJ.get(month) != None or month == "all"):
                break
            else:
                print("Error: Make sure you enter correct spelling of month!!\n")
        else:
            print("Error: Please enter only alphabets for month as input!!\n")


    #Getting user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while True:
        day = input("\nPlease enter day of week to filter by or 'all' for no filter: \n")
        
        if(day == "all"):
            break
        elif(day.isdigit()):
            if((int(day) >= 0) and (int(day) <= 6)):
                break
            else:
                print("Error: Make sure you enter week of day between 0(Monday) to 6(Sunday) OR 'all' for no filter!!\n")
        else:
            print("Error: Make sure you enter week of day between 0(Monday) to 6(Sunday) OR 'all' for no filter!!\n")

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
    
    if city == "all":
        city_name = "*.csv"
    else:
        city_name=(CITY_DATA.get(city)) 
    
    df = pd.concat([pd.read_csv(f) for f in glob.glob(city_name)], ignore_index = True)
    
    if month != "all":
        df = df[pd.to_datetime(df['Start Time']).dt.month == int(MONTH_OBJ[month])]
    if day != "all":
        df = df[pd.to_datetime(df['Start Time']).dt.day == int(day)]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if not df['Start Time'].empty:     
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # Displaying the most common month
        
        month_num = (df['Start Time'].dt.month).value_counts().idxmax()
        print("Most frequent month for travelling: "+str(list(MONTH_OBJ.keys())[list(MONTH_OBJ.values()).index(month_num)].title()))
        
        #Displaying the most common day of week
        day_num = (df['Start Time'].dt.weekday_name).value_counts().idxmax()
        print("Most frequent day of week for travelling: "+str(day_num.title()))
    
        # Displaying the most common start hour
        hour_num = (df['Start Time'].dt.hour).value_counts().idxmax()
        print("Most frequent hour for travelling: "+str(hour_num))
    else:
        print("No data to display!!")       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    if not df['Start Station'].empty: 
        # Displaying most commonly used start station
        print("Most frequently used start station: "+str(df['Start Station'].mode()[0]))
        print("\n")
    
        #Displaying most commonly used end station
        
        print("Most frequently used end station: "+str(df['End Station'].mode()[0]))
        print("\n")
        
        #Displaying most frequent combination of start station and end station trip
        print("Most frequently used combination of start station and end station: ")
        print(df.groupby(['Start Station', 'End Station']).size().nlargest(1))
    else:
        print("No data to display!!")   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    if not df['Trip Duration'].empty:
        # Displaying total travel time
        #Trip Duration
        print("Total Traveling time: ",df['Trip Duration'].sum()) 
    
        # Displaying mean travel time
        print("Mean of Traveling time: ",df['Trip Duration'].mean())
    else:
        print("No data to display!!")   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Displaying counts of user types
    print("Counts per user:")
    if not df['User Type'].empty:
        print(df['User Type'].value_counts())
    else:
        print("No data to display!!")   
    print("\n")
    # Displaying counts of gender
    print("Counts per gender:")
    if ('Gender' in df) and (not df['Gender'].empty):   
        print(df['Gender'].value_counts())
    else:
        print("No gender information found!!")                
    # Displaying earliest, most recent, and most common year of birth
    print("\n")
    if ('Birth Year' in df) and (not df['Birth Year'].empty):
        print("Earliest Data of birth:", int(df['Birth Year'].min()))
        print("Most recent Data of birth:", int(df['Birth Year'].max()))
        print("Most Common Data of birth:", int(df['Birth Year'].mode()[0]))
    else:
        print("No Birth Year information found!!")      
    
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
        counter = 0
        while True:
            more_data = input('\nWould you like see more data? Enter yes or no.\n')
            if more_data.lower() != 'yes':
                break
            else:
                if df.size > 0:
                    print(df[counter:(counter+5)])
                    counter += 5
                else:
                    print("No raw data found!!")    
                    break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Exiting...\n")
            break
        


if __name__ == "__main__":
	main()
