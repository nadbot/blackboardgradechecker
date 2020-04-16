# blackboardgradechecker
Checks your grade automatically and sends it over discord

## GradeChecker
This script will automatically login to blackboard and check the grades for all given courses.
It will then output a dictionary with all the results.
For receiving the results, it uses the selenium webdriver, this has to be installed in advance.
 
## Credentials file
The credentials file has the following structure
linkLogin = <URL of Loginscreen>

ssid = "StudentSSID"

pw = "StudentPassword"

links = {"Course1":"URLofCourseGrades",
             "Course2":"URLofCourseGrades"}

