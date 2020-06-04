import discord
import configparser
import random
from leetcodeScaper import leetcodeScaper

def read_token():
    config = configparser.ConfigParser()
    config.read('discord.ini')
    return config['DISCORD']['bot_token']

client = discord.Client()
token = read_token()

@client.event
async def on_ready():
    print(f'[+] {client.user} has connected to Discord!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Yeet away from unemployment'))

@client.event
async def on_message(message):

    channels = ['leetcode']

    if str(message.channel) in channels:
        if message.author == client.user:
            return

        commands = ['!y']
        guides = 'YeetCode Bot Command Guide\n\'!y <difficulty>\'\t\tSend problem in the given level of difficulty\n(\'easy\': 1, \'medium\': 2, \'hard\': 3)'

        if message.content.startswith('!') and message.content.split()[0] not in commands:
            await message.channel.send('`Invalid commands`')
            await message.channel.send(f'```{guides}```')
            return

        if message.content.startswith('!y'):
            # difficulties = {'easy':1, 'medium':2, 'hard':3}
            difficulty = int(message.content.split()[1])

            lc = leetcodeScaper('algorithms', difficulty)
            problemList = lc.getProblemList()
            randProblem = problemList[random.randint(0, len(problemList)-1)]

            problem = lc.downloadProblem(randProblem)

            if problem:
                await message.channel.send(f'```{problem}```')

            else:
                await message.channel.send('`Error Occurred. Try again.`')
            
            return

client.run(token)
