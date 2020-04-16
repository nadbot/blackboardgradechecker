import credentials as cred
from selenium import webdriver

driver = webdriver.Chrome('C:/images/chromedriver.exe')

def login():
    driver.get(cred.linkLogin)
    username = driver.find_element_by_id("user_id")
    username.send_keys(cred.ssid)
    password = driver.find_element_by_id("password")
    password.send_keys(cred.pw)
    button = driver.find_element_by_id('entry-login')
    button.click()

def checkGrade(link):
    driver.get(link)
    gradesWrapper = driver.find_elements_by_class_name("sortable_item_row")
    gradesForCourse = []
    for row in gradesWrapper:
        score = row.find_element_by_class_name("grade")
        name = row.find_element_by_class_name("gradable").text
        if "\n" in name:
            name, due, type = name.split("\n")
        pointsPossible = score.find_elements_by_class_name("pointsPossible")
        if len(pointsPossible) > 0:
            pointsPossible = pointsPossible[0].text
        else:
            pointsPossible = "/10"
        testGrade = score.find_element_by_class_name("grade").text
        if score.find_elements_by_class_name("itemStats"):
            itemStats = score.find_element_by_class_name("itemStats")
            average = itemStats.find_element_by_class_name("ave").text
            median = itemStats.find_element_by_class_name("med").text
        else:
            average = 0
            median = 0
        result = testGrade+""+pointsPossible
        gradesForCourse.append({'name': name, 'score': result, 'average': average, 'median': median})

    return gradesForCourse

def printGrades(grades):
    for key in grades:
        print(key)
        for assignment in grades[key]:
            print(assignment)
            print("\n")

def checkGrades():
    grades = {}
    for key in cred.links:
        grades[key] = checkGrade(cred.links[key])
    return grades



def main():
    login()
    grades = checkGrades()
    printGrades(grades)

if __name__ == '__main__':
    main()