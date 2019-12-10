# Finalproject

This project utilizes the Reddit API for pulling the 'top 24 hours' page of each default subreddit. The data from these requests are then cached and written into a database containing two separate tables. After a day, the cache is deleted and the database is re-written to contain new data showing the live data. Finally the data is visualised into different bar and pie charts.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The requirements.txt file included in the repository holds all packages needed to run this program. Run the following command in your terminal to pip install requirements.
```
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```
Provided in the repository are two sample files named secret_sample.py and config_sample.py. These files contain the variables you will need to fill in for data extraction through the Reddit API and connecting to the database you specify.

### Getting Credentials from Reddit

To get a client_id and client_secret for Reddit, please go to reddit.com and create an account. If you already have an account you can skip this step and log into you account.Once you have an account, go into your preferences and click onto the 'apps' tab(https://www.reddit.com/prefs/apps). Scroll to the bottom and click 'create another app...'. This will create a new box. You will need to select script as shown and fill in a name and description.

After that is complete you will have a client_id and client_secret from your app. Please remember to input these values as strings in the sample file secret_sample.py. Again, you will need to rename this file afterwards to secret.py as stated above.

On this same file, you will need to input you Reddit account username and password in the sample file provided. This is required to make a successful request to the Reddit API.

For complete reddit API documentation, please follow the links below:

[Reddit API Quick Start Steps](https://github.com/reddit-archive/reddit/wiki/OAuth2)

[Complete Reddit API Request Types](https://www.reddit.com/dev/api/)

### Creating and Accessing Database
Provided for you is a config_sample.py file. This contains all the required variable inputs to the program. At the end of these steps, you will need to rename the file config.py for correct import.

This program requires database connection using PostgreSQL. For documentation on installing PostgreSQL follow the links below:

### For Mac:

Get homebrew: Go to this link: https://brew.sh/ Copy the one line of code that they have on that page, which is this:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Open your Terminal and paste that entire line in. It will run for a while. It may prompt you for your computer password (or it may not).

After homebrew is installed run:
```
brew install postgres
```
To start the connection to your database run:
```
pg_ctl -D /usr/local/var/postgres start
```
After that is complete, you are now connected to your Postgres database. For simpler visualization, you can use TeamSQL which can be downloaded [here](https://teamsql.io/). I used pgAdmin4. 

### For Windows:

Follow the documentation provided at the link below: 
(https://labkey.org/Documentation/wiki-page.view?name=installPostgreSQLWindows)

After the above is done, you are now ready to create a database to store all the data the program gathers. Run the following to create a database. You can name the database whatever you'd like, however just be sure to remember what that is.
```
createdb your_database_name
```
Once you have a database created, you can now being to fill in the provided 'config_sample.py' file. Replace the ```db_name``` with the name of your database, ```db_user``` with the user name associated to your database upon installation, and ```db_password``` if the database you created has a password, if not then leave as an empty string. Once again, you will need to rename the file ```config.py``` for correct import.

### Running the program
Once all the above has been completed, you are now ready to run the program. The first step is to check the database connection by running:
```
python3 finalproject.py
```
You should see a readout in your terminal of 'Success connecting to the database'

To set up the structure of the database, run the following:
```
setup 
```
This ```setup``` command creates the database tables for storing the data that we pull later on by running the ```setup_database()``` function.

If you open up TeamSQLor pgAdmin4 and look at the database, it should contain two tables. One for Subreddits and the other for Postings.

To get the data from each subreddit written into the database, run the following:
```
write
```
This write command runs the ```start_reddit_session(), load_cache(), and run_search_on_default()``` functions. The ```start_reddit_session()``` does, as you would guess, start the reddit request session saving a token in the 'creds.json' file. The ```load_cache()``` functions loads the cache into the CACHE_DICTION variable, but if the cache file is older than a day, it deletes the file and makes a new cache_file for the day. The ```run_search_on_default()``` function finally pulls all this together and iterates over a static list containing default subreddits that each account is automatically subscribed to when they create a reddit account. It then checks to see if it is making a new request or pulling from the database for each subreddit and inputing the data into the database.

The database should look similar to this:

![img](https://user-images.githubusercontent.com/55447190/70535903-db006000-1b2b-11ea-88b6-8f6da1ff7148.PNG)

![img1](https://user-images.githubusercontent.com/55447190/70536004-01260000-1b2c-11ea-9cb2-3692fa8ba9ef.PNG)

To create a plot, run the following command in your terminal
```
plot
```
The ```plot``` command runs the ```plot()``` function. Connection and storage of data into the database is required for this function to work. The function runs an SQL query collecting the sum of each post's score, inner joining the tables on their foreign key (ID and subreddit_id), and grouping the sum by the Subreddit's name. After running a .fetchall(), we are left with a list containing the sum of scores and the subreddit name associated. After unpacking the list, we then use Plotly to create a visual of the data collected.

The bar chart should open automatically in Google Chrome (or your default browser), however, if that doesn't appear to be the case, go into the directory and open the file ```subreddit_analysis.html``` in your webbrowser.

Example output after running plot:

![plot](https://user-images.githubusercontent.com/55447190/70536047-1438d000-1b2c-11ea-9474-37c936bb2bad.PNG)

Running the program each time will require a write command followed by a plot command. Write to get all data into the database, and plot to plot the data.

### Running the tests
The finalproject_tests.py file included contains all test cases for this program. If you are having issues with getting through the installation steps, please run these tests. It will give you an idea of what where the issue is.

Provided for you is a sample post json file ```sample_reddit_post.json```. This needs to be in your folder for some of the test functions.

### Built With
[Plotly](https://chart-studio.plot.ly/feed/#/) - Data visualization

[Requests](https://2.python-requests.org//en/master/) - Sending requests to Reddit API

[Psycopg2](http://initd.org/psycopg/) - PostgreSQL adapter for python

[Reddit API](https://www.reddit.com/dev/api/) - Where the data came from

### Author
Yashaswini Joshi
