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

    #TODO improve commands: commands lower and upper case working, show list of commands, make list clickable (show recommandations?)
    #TODO put commands inside methods
    #TODO reload grades only every few minutes and not with every call
    if message.content.startswith('!hello'):
        await message.channel.send("Hello")
    if message.content.startswith('!showGrades'):
        grades = GradeChecker.checkGrades()
        await message.channel.send("```"+createTableforGrades(grades)+"```")
    elif message.content.startswith('!showGrade'):
        grades = GradeChecker.checkGrades()
        courses = []
        for index, key in enumerate(grades):
            courses.append([index,key])
        print(courses)
        await message.channel.send("```Choose the course by replying with the index: \n"+str(tabulate(courses,["Index","Course"]))+"```")
        msg = await client.wait_for('message')
        courseChosen = list(grades.keys())[int(msg.content)]
        print("You chose "+str(courseChosen))
        items = []
        for index, item in enumerate(grades[courseChosen]):
            items.append([index, item['name'], item['score']])
        print(items)
        await message.channel.send(
            "```Choose the item by replying with the index: \n" + str(tabulate(items, ["Index", "Item","Grade"])) + "```")

        msg = await client.wait_for('message')
        itemID = int(msg.content)
        itemChosen = grades[courseChosen][itemID]
        print("You chose " + str(itemChosen['name']))
        await message.channel.send(
            "```" + str(
                tabulate([[itemChosen['name'],itemChosen['score'],itemChosen['average'],itemChosen['median']]], ["Name", "Grade", "Average","Median"])) + "```")
        if "-" in itemChosen['score']:
            await message.channel.send("Do you want to watch this item? (yes/no)")
            msg = await client.wait_for('message')
            print("You chose " + str(msg.content))
            await message.channel.send(str(itemChosen['name']) +" will be observed for changes")
            channel = message.channel
            if not running:
                client.loop.create_task(my_background_task(channel,courseChosen,itemID))
                running = True

def createTableforGrades(grades):
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
    global running
    #await client.wait_until_ready()
    counter = 0
    print("Test")
    while True:
        grades = GradeChecker.checkGrades()
        observedGrade = grades[course][itemID]
        if "-" not in observedGrade['score']:
            await channel.send("Your grade for "+observedGrade['name']+ " is " + str(observedGrade['score']))
            running = False
            break
        else:
            counter += 1
            print(counter)
            print(observedGrade)
            await asyncio.sleep(180) # task runs every 180 seconds

def main():
    GradeChecker.login()
    client.run(cred.TOKEN)


if __name__ == '__main__':
    main()

