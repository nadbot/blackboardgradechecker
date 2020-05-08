import discord
import asyncio

import GradeChecker
import credentials as cred
from tabulate import tabulate

client = discord.Client()
running = False
observing = []


@client.event
async def on_message(message):
    global running
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # TODO improve commands: commands lower and upper case working, make list clickable (show recommandations?)
    # TODO put commands inside methods
    # TODO reload grades only every few minutes and not with every call
    if message.content.startswith('!hello'):
        await message.channel.send("Hello")
    # simple help method
    if message.content.startswith('!help'):
        await message.channel.send("Use !getClasses to refresh the classes which will be checked\n"
                                   "Use !showGrades to show all available grades in all courses\n"
                                   "Use !showGrade to show a certain grade in a course. "
                                   "Choosing can be done by sending the corresponding number")
    # call getClasses function, which updates list of links for grades
    if message.content.startswith('!getClasses'):
        classes = GradeChecker.get_classes()
        if len(classes) == 0:
            await message.channel.send(
                "Failed to find any classes. Please check if you have the correct module and are logged in")
    # show all grades
    if message.content.startswith('!showGrades'):
        grades = GradeChecker.check_grades()
        await message.channel.send("```" + create_table_for_grades(grades) + "```")
    # show grade for specific entry
    elif message.content.startswith('!showGrade'):
        # update all grades
        grades = GradeChecker.check_grades()
        courses = []
        for index, key in enumerate(grades):
            courses.append([index, key])
        print(courses)
        # print table with course and an index
        await message.channel.send(
            "```Choose the course by replying with the index: \n" + str(tabulate(courses, ["Index", "Course"])) + "```")
        # wait for specific index (currently does not catch invalid options
        msg = await client.wait_for('message')
        # find chosen course
        course_chosen = list(grades.keys())[int(msg.content)]
        print("You chose " + str(course_chosen))
        items = []
        # create list of items in that course with indices
        for index, item in enumerate(grades[course_chosen]):
            items.append([index, item['name'], item['score']])
        print(items)
        # print table with assignments and index
        await message.channel.send(
            "```Choose the item by replying with the index: \n" + str(
                tabulate(items, ["Index", "Item", "Grade"])) + "```")
        # wait for specific index
        msg = await client.wait_for('message')
        item_id = int(msg.content)
        item_chosen = grades[course_chosen][item_id]
        print("You chose " + str(item_chosen['name']))
        # show details for that item
        await message.channel.send(
            "```" + str(
                tabulate([[item_chosen['name'], item_chosen['score'], item_chosen['average'], item_chosen['median']]],
                         ["Name", "Grade", "Average", "Median"])) + "```")
        if "-" in item_chosen['score']:
            # if grade not available, allow user to watch that item
            await message.channel.send("Do you want to watch this item? (yes/no)")
            msg = await client.wait_for('message')
            print("You chose " + str(msg.content))
            if msg.content == "yes":
                # item will be observed, bot will send message once grade becomes available, checking every few minutes
                await message.channel.send(str(item_chosen['name']) + " will be observed for changes")
                channel = message.channel
                # prevents it from running multiple instances at once
                set_items_to_observe(course_chosen,item_chosen['name'])
                if not running:
                    client.loop.create_task(my_background_task(channel, cred.background_task_time))
                    running = True
            else:
                await message.channel.send(str(item_chosen['name']) + " will not be observed for changes")


def create_table_for_grades(grades):
    """
    Create a proper table for showing the grades. Displays for each course the items and their grade.
    :param grades: Dict of grades, gathered from GradeChecker
    :return: String representing the table. Can be sent to the user
    """
    string = ""
    for key in grades:
        print(key)
        grade_for_course = []
        for item in grades[key]:
            grade = [item['name'], item['score']]
            grade_for_course.append(grade)
        print(tabulate(grade_for_course, ["Item", "Grade"]))
        string += key + "\n"
        string += tabulate(grade_for_course, ["Item", "Grade"]) + "\n\n"
    return string


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def set_items_to_observe(course, name):
    """
    Method to append new item to observe. Will automatically update the list of items that will be checked regularly
    :param course: Course for which the grade is being observed
    :param name: Name of the item that is being observed
    :return: Nothing, appends to global variable
    """
    global observing
    print("Adding to observing:")
    print(observing)
    observing.append({'course': course, 'name': name})
    print("New content:")
    print(observing)


async def my_background_task(channel, time=180):
    """
    Asynchronous method used to check regularly for updates on specific grades.
    :param channel: Channel on which update should be sent
    :param time: Time in seconds how often the background task should run
    :return: returns nothing, prints to user once it finds something
    """
    global observing
    global running
    # await client.wait_until_ready()
    counter = 0
    print("Test")
    while True:
        # check for updates
        grades = GradeChecker.check_grades()
        for item in observing:
            print("Looping through observed items")
            print(item)
            course = item['course']
            name = item['name']
            print(grades[course])
            observed_grade = {}
            for element in grades[course]:
                if element['name'] == name:
                    observed_grade = element
            # look if observed grade is still not available
            if "-" not in observed_grade['score']:
                # if it is available, stop the background task and send info to user
                await channel.send("Your grade for " + observed_grade['name'] + " is " + str(observed_grade['score']))
                # running = False
                # break
                observing.remove({'course': course, 'name': name})
        if len(observing) == 0:
            running = False
            break
        else:
            # otherwise try again in 3 minutes
            counter += 1
            print(counter)
            print(observing)
            print("Running Async task after " + str(time) + " seconds")
            await asyncio.sleep(time)  # task runs every 180 seconds


def main():
    """
    Initial method once bot starts. Will login to blackboard and retrieve list of courses.
    After that, it will start the discord bot.
    :return: Nothing
    """
    GradeChecker.login()
    GradeChecker.get_classes()
    client.run(cred.TOKEN)


if __name__ == '__main__':
    main()
