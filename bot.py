import discord
import configparser
import random
from leetcodeScraper import leetcodeScraper

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

        commands = ['!y', '!md']
        guides = 'YeetCode Bot Command Guide\n\'!y <difficulty>\'\t\tSend problem in the given level of difficulty\n(\'easy\': 1, \'medium\': 2, \'hard\': 3)\n\'!md <problem id>\'\t\tMark finished problem'

        if message.content.startswith('!') and message.content.split()[0] not in commands:
            await message.channel.send('`Invalid commands`')
            await message.channel.send(f'```{guides}```')
            return

        if message.content.startswith('!y'):
            
            def read_log():
                finishedProblems = []
                
                try:
                    with open("log.txt", "r") as f:
                        data = f.readlines()
                        for info in data:
                            # finishedProblems.append({"frontend_question_id":int(info.split()[0].strip()), "question_title_slug":info.split()[1].strip()})
                            finishedProblems.append(info.split()[0].strip())

                except Exception as e:
                    print(f'[-] Error Occurred: {e}')
                    pass

                return finishedProblems

            finishedProblems = read_log()

            # difficulties = {'easy':1, 'medium':2, 'hard':3}
            difficulty = int(message.content.split()[1])

            lc = leetcodeScraper('algorithms', difficulty)
            problemList = lc.getProblemList()
            randProblem = problemList[random.randint(0, len(problemList)-1)]
            problemID = randProblem[0]

            while problemID in finishedProblems:
                randProblem = problemList[random.randint(0, len(problemList)-1)]

            problemString = lc.downloadProblem(randProblem)

            if problemString:
                await message.channel.send(f'```{problemString}```')

            else:
                await message.channel.send('`Error Occurred. Try again.`')
            
            return

client.run(token)
