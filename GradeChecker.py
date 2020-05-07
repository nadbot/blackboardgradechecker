import credentials as cred
from selenium import webdriver
import time

driver = webdriver.Chrome('C:/images/chromedriver.exe')

def login():
    '''
    Method for logging into blackboard. Uses link and credentials from credentials.py.
    The client will stay logged in in this window until a certain amount of time expires.
    :return: Nothing
    '''
    driver.get(cred.linkLogin)
    username = driver.find_element_by_id("user_id")
    username.send_keys(cred.ssid)
    password = driver.find_element_by_id("password")
    password.send_keys(cred.pw)
    button = driver.find_element_by_id('entry-login')
    button.click()

def checkGrade(link):
    '''
    Checks the grades for a given link
    :param link: Link of grades page for that specific course
    :return: list of grades for that course
    '''
    driver.get(link)
    gradesWrapper = driver.find_elements_by_class_name("sortable_item_row")
    gradesForCourse = []
    # loop through all grades
    for row in gradesWrapper:
        # get wrapper for grade
        score = row.find_element_by_class_name("grade")
        # get name of assignment.
        # If it is multiple lines divide it into name, due date and type of assignment
        name = row.find_element_by_class_name("gradable").text
        if "\n" in name:
            name, due, type = name.split("\n")
        # get maximum amount of points possible (usually 10)
        pointsPossible = score.find_elements_by_class_name("pointsPossible")
        if len(pointsPossible) > 0:
            pointsPossible = pointsPossible[0].text
        else:
            # if it is not given, use the default value of 10
            pointsPossible = "/10"
        testGrade = score.find_element_by_class_name("grade").text
        if score.find_elements_by_class_name("itemStats"):
            # if additional stats are given, also add store these
            # otherwise set them to 0
            itemStats = score.find_element_by_class_name("itemStats")
            average = itemStats.find_element_by_class_name("ave").text
            median = itemStats.find_element_by_class_name("med").text
        else:
            average = 0
            median = 0
        # merge grade and max points to grade column
        result = testGrade+""+pointsPossible
        # add everything as dict to the grades from that course
        gradesForCourse.append({'name': name, 'score': result, 'average': average, 'median': median})

    return gradesForCourse

def printGrades(grades):
    '''
    Prints grades for a given list of grades
    :param grades: list of grades to print
    :return: Nothing
    '''
    for key in grades:
        print(key)
        for assignment in grades[key]:
            print(assignment)
            print("\n")

def getClasses():
    '''
    Method to get a list of courses the user is subscribed to and the url to their grades page
    :return: Nothing, updates list from credentials
    '''
    driver.get("https://uu.blackboard.com/")

    # find block with all courses
    classWrapper = driver.find_elements_by_id("div_4_1")
    classes = []
    # if module is not loaded, wait 5 seconds and repeat
    while "Please wait while the module loads" in classWrapper[0].text:
        driver.get("https://uu.blackboard.com/")
        time.sleep(5)
        classWrapper = driver.find_elements_by_id("div_4_1")

    # loop through the courses
    for row in classWrapper:
        # find the hyperlink, as it contains the id of the course
        courses = row.find_elements_by_tag_name("a")
        for course in courses:
            # store all the elements of each course
            classes.append(course)
    # loop through the list of hyperlink elements
    for course in classes:
        # name of course is given as the text
        element = driver.find_element_by_link_text(course.text)
        # link of the course is given by href property
        link = element.get_property("href")
        # as link would lead to start page of that course, we extract id only
        _,end = link.split("&id=")
        id,_ = end.split("&url=")

        # enter id of course in url for grades
        url = 'https://uu.blackboard.com/webapps/bb-mygrades-bb_bb60/myGrades?course_id='+id+'&stream_name=mygrades&is_stream=false'
        # add entry to links
        cred.links[element.text] = url
    print(cred.links)


def checkGrades():
    '''
    Wrapper for checkGrade method. Calls it once for every course
    :return: dict of all grades for all courses
    '''
    grades = {}
    for key in cred.links:
        grades[key] = checkGrade(cred.links[key])
    return grades

def main():
    '''
    Main Method
    :return: Nothing
    '''
    login()
    grades = checkGrades()
    printGrades(grades)

if __name__ == '__main__':
    main()