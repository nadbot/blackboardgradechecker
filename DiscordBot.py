import discord
import asyncio
import GradeChecker
import credentials as cred
from tabulate import tabulate
from pprint import pprint


client = discord.Client()
running = False
@client.event
async def on_message(message):
    global running
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send("Still running")
    if message.content.startswith('!checkGrades'):
        grades = GradeChecker.checkGrades()
        await message.channel.send("```"+createTableforGrades(grades)+"```")
    if message.content.startswith('!grade'):
        msg = 'Hello {0.author.mention}'.format(message)
        user = discord.utils.get(client.get_all_members(), id=message.author.id)

        channel = message.channel
        if not running:
            client.loop.create_task(my_background_task(channel))
            running = True
        grade = GradeChecker.checkGrades()
        await channel.send(msg)
        # await channel.send("Your grade is "+ str(grade))

        # await client.send(user, msg)


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

async def my_background_task(channel):
    #await client.wait_until_ready()
    counter = 0
    print("Test")
    counter += 1
    while True:
        grade = GradeChecker.checkGrades()
        counter += 1
        #TODO fix
        await channel.send("Your grades are " + str(grade))
        if grade:
            await channel.send("Your grades are "+ str(grade))
            break
        else:
            await asyncio.sleep(180) # task runs every 60 seconds


GradeChecker.login()
client.run(cred.TOKEN)

