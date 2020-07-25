# blackboardgradechecker
Checks your grade automatically and sends it over discord.

Regularly during my studies, grades for exams have been added to Blackboard without any notification of it.
In order to get a notification that a grade for an assignment or test has been added, I have created this script.

It connects to a discord bot and runs every 30 minutes by default to check if any changes to the grades have been made.
If changes are found, the bot will send a message to the channel where you started the observation.

To avoid problems with timeouts, you need to provide your username and password in the credentials file.
If the bot faces a timeout, it will automatically log in again and then poll the results.
This way, the bot can run in the background the whole time and the observation can be activated only when needed
to avoid unnecessary traffic on the blackboard page.

## GradeChecker
This script will automatically login to blackboard and check the grades for all given courses.
It will then output a table with all the results sorted by each course you are following.
 

![Picture of Grades shown in Discord](./Images/Sample_Grades.JPG?raw=true "Title")


# Setup
## Discord bot
In order to create a discord bot, which can message you about your results and is the UI for the program,
follow the guide:
https://discordpy.readthedocs.io/en/latest/discord.html

This bot can either be added to a server (where everyone can see your results,
so it would be advisable to use it on a private server only) or can be messaged directly.
The bot will notify you (if enabled) about a new grade on the channel where you messaged the bot for observing changes.


## Selenium
To work, the program uses Selenium to automate the browser and login to blackboard and receive the grades.
In order for Selenium to work, a Web driver is needed.

This application uses the Chromium Web driver for Selenium and it has not been tested with other web drivers.
The Web driver needs to be downloaded separately, the latest tested version for this script is Version 83 (ChromeDriver 83.0.4103.39)
found on this page: https://chromedriver.chromium.org/downloads

Detailed instructions can be found at:
https://chromedriver.chromium.org/getting-started

## Credentials file
The credentials file is used for configuration and credentials and has the following structure:

linkLogin = "URL of Loginscreen"

ssid = "StudentSSID"

pw = "StudentPassword"

links = {} # can be left empty, as it will be filled automatically

TOKEN = "TOKEN used for Discord Bot"

background_task_time = 1800 (amount of time to pass before observing task checks for grades again)

path_to_chromedriver = 'C:/images/chromedriver_win32_83_0_4103_39/chromedriver.exe'

# Commands
Here is a list of commands that can be sent to the bot directly or to a server on which the bot is added.
More commands will be added from time to time.
For every command, the spelling as well as the capitalization is important to work.
## !showGrades
If you send the message `!showGrades` to the bot, it will return a table like the one shown below containing all grades
sorted by the course to which they belong.
![Picture of Grades shown in Discord](./Images/Sample_Grades.JPG?raw=true "Title")

## !showGrade
If you send the message `!showGrade` to the bot, it will show an interactive dialogue,
where you can choose the course and the item in the course by sending numbers starting from 0 for the corresponding 
course/item. Once an item is chosen, more details such as grade, average and median are shown.
In a later version, it is also planned that comments received for this assignment are also shown.

## !help
Shows an overview of which commands can be used.

## !status
Shows whether the grades are observed or not, how long it will take until it polls the results again 
band how long the bot has been running.

An example reply from the bot is shown below:
![Picture of Status shown in Discord](./Images/Status.JPG?raw=true "Title")

## !observeChanges
Sending `!observeChanges` to the bot will start the observation of grades.

This will result in the bot checking for new updates every 30 minutes (time can be changed in the credentials.py file).

If changes occur, a message will be sent with the new results or the ones that changed to before.

If nothing changes, no message will be sent.

The observation will continue until it is stopped manually, it will not automatically stop after a grade is received.

## !stopObserving

In order to manually stop observing, send `!stopObserving` to the bot.

This will result in no further observations of the grade.

However, it will still poll once more in less than 30 minutes, as the countdown for that has already been started.
