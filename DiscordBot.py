import discord
import asyncio

import GradeChecker
import credentials as cred
from tabulate import tabulate


client = discord.Client()
running = False
@client.event
async def on_message(message):
    global running
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #TODO improve commands: commands lower and upper case working, make list clickable (show recommandations?)
    #TODO put commands inside methods
    #TODO reload grades only every few minutes and not with every call
    if message.content.startswith('!hello'):
        await message.channel.send("Hello")
    #simple help method
    if message.content.startswith('!help'):
        await message.channel.send("Use !getClasses to refresh the classes which will be checked\n"
              "Use !showGrades to show all available grades in all courses\n"
              "Use !showGrade to show a certain grade in a course. Choosing can be done by sending the corresponding number")
    #call getClasses function, which updates list of links for grades
    if message.content.startswith('!getClasses'):
        classes = GradeChecker.getClasses()
    #show all grades
    if message.content.startswith('!showGrades'):
        grades = GradeChecker.checkGrades()
        await message.channel.send("```"+createTableforGrades(grades)+"```")
    #show grade for specific entry
    elif message.content.startswith('!showGrade'):
        #update all grades
        grades = GradeChecker.checkGrades()
        courses = []
        for index, key in enumerate(grades):
            courses.append([index,key])
        print(courses)
        #print table with course and an index
        await message.channel.send("```Choose the course by replying with the index: \n"+str(tabulate(courses,["Index","Course"]))+"```")
        #wait for specific index (currently does not catch invalid options
        msg = await client.wait_for('message')
        #find chosen course
        courseChosen = list(grades.keys())[int(msg.content)]
        print("You chose "+str(courseChosen))
        items = []
        #create list of items in that course with indices
        for index, item in enumerate(grades[courseChosen]):
            items.append([index, item['name'], item['score']])
        print(items)
        #print table with assignments and index
        await message.channel.send(
            "```Choose the item by replying with the index: \n" + str(tabulate(items, ["Index", "Item","Grade"])) + "```")
        #wait for specific index
        msg = await client.wait_for('message')
        itemID = int(msg.content)
        itemChosen = grades[courseChosen][itemID]
        print("You chose " + str(itemChosen['name']))
        #show details for that item
        await message.channel.send(
            "```" + str(
                tabulate([[itemChosen['name'],itemChosen['score'],itemChosen['average'],itemChosen['median']]], ["Name", "Grade", "Average","Median"])) + "```")
        if "-" in itemChosen['score']:
            #if grade not available, allow user to watch that item
            await message.channel.send("Do you want to watch this item? (yes/no)")
            msg = await client.wait_for('message')
            print("You chose " + str(msg.content))
            if msg.content == "yes":
                #item will be observed, bot will send message once grade becomes available, checking every few minutes
                await message.channel.send(str(itemChosen['name']) +" will be observed for changes")
                channel = message.channel
                #prevents it from running multiple instances at once
                #TODO if observing multiple grades, make list and send updates for each
                if not running:
                    client.loop.create_task(my_background_task(channel,courseChosen,itemID))
                    running = True
            else:
                await message.channel.send(str(itemChosen['name']) + " will not be observed for changes")

def createTableforGrades(grades):
    '''
    Create a proper table for showing the grades. Displays for each course the items and their grade.
    :param grades: Dict of grades, gathered from GradeChecker
    :return: String representing the table. Can be sent to the user
    '''
    string = ""
    for key in grades:
        print(key)
        gradeForCourse = []
        for item in grades[key]:
            grade = [item['name'],item['score']]
            gradeForCourse.append(grade)
        print(tabulate(gradeForCourse,["Item","Grade"]))
        string+=key+"\n"
        string+=tabulate(gradeForCourse,["Item","Grade"])+"\n\n"
    return string

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#TODO improve to be able to watch several grades at once
async def my_background_task(channel, course, itemID):
    '''
    Asynchronous method used to check regularly for updates on specific grades.
    :param channel: Channel on which update should be sent
    :param course: Course for which the grade is being observed
    :param itemID: ID of the item that is being observed
    :return: returns nothing, prints to user once it finds something
    '''
    global running
    #await client.wait_until_ready()
    counter = 0
    print("Test")
    while True:
        #check for updates
        grades = GradeChecker.checkGrades()
        observedGrade = grades[course][itemID]
        #look if observed grade is still not available
        if "-" not in observedGrade['score']:
            #if it is available, stop the background task and send info to user
            await channel.send("Your grade for "+observedGrade['name']+ " is " + str(observedGrade['score']))
            running = False
            break
        else:
            #otherwise try again in 3 minutes
            counter += 1
            print(counter)
            print(observedGrade)
            await asyncio.sleep(180) # task runs every 180 seconds

def main():
    '''
    Initial method once bot starts. Will login to blackboard and retrieve list of courses. After that, it will start the discord bot
    :return: Nothing
    '''
    GradeChecker.login()
    GradeChecker.getClasses()
    client.run(cred.TOKEN)


if __name__ == '__main__':
    main()

