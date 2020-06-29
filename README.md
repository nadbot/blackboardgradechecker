# blackboardgradechecker
Checks your grade automatically and sends it over discord

## GradeChecker
This script will automatically login to blackboard and check the grades for all given courses.
It will then output a dictionary with all the results.
For receiving the results, it uses the selenium webdriver, this has to be installed in advance.
 
## Credentials file
The credentials file is used for configuration and credentials and has the following structure:

linkLogin = "<URL of Loginscreen>"

ssid = "StudentSSID"

pw = "StudentPassword"

links = {}

TOKEN = "TOKEN used for Discord Bot"

background_task_time = 1800 <amount of time to pass before observing task checks for grades again>

path_to_chromedriver = 'C:/images/chromedriver_win32_83_0_4103_39/chromedriver.exe'
