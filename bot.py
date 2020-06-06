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

        commands = ['!', '!help', '!yeet', '!md']
        guides = '''YeetCode Bot Command Guide
        \'!yeet <difficulty>\'      Send problem in the given level of difficult
                    (\'easy\': 1, \'medium\': 2, \'hard\': 3)
        \'!md <problemID>\'         Mark problem as finished'''

        if message.content.startswith('!') and message.content.split()[0] not in commands:
            await message.channel.send('`Invalid commands`')
            await message.channel.send(f'```{guides}```')
            return

        if message.content in ('!', '!help'):
            await message.channel.send(f'```{guides}```')
            return

        if message.content.startswith('!yeet'):
            
            def read_log():
                finishedProblems = []
                
                try:
                    with open("log.txt", "r") as f:
                        data = f.readlines()
                        for frontend_question_id in data:
                            finishedProblems.append(int(frontend_question_id))

                except Exception as e:
                    print(f'[-] Error Occurred: {e}')

                return finishedProblems

            finishedProblems = read_log()

            # difficulties = {'easy':1, 'medium':2, 'hard':3}
            validDiffculties = (1, 2, 3)
            difficulty = int(message.content[len('!yeet')+1:])

            if difficulty not in validDiffculties:
                message.channel.send('`Invalid difficulty level`')
                return

            lc = leetcodeScraper('algorithms', difficulty)
            problemList = lc.getProblemList()
            randProblem = problemList[random.randint(0, len(problemList)-1)]
            frontend_question_id = randProblem[0]

            while frontend_question_id in finishedProblems:
                randProblem = problemList[random.randint(0, len(problemList)-1)]

            problemString = lc.downloadProblem(randProblem)

            if problemString:
                await message.channel.send(f'```{problemString}```')

            else:
                await message.channel.send('`Error Occurred. Try again.`')
            
            return

        if message.content.startswith('!md'):

            def write_log(frontend_question_id):
                try:
                    with open("log.txt", "a") as f:
                        f.write(f'{frontend_question_id}')
                        f.close()

                except Exception as e:
                    print(f'[-] Error Occurred:: {e}')

            frontend_question_id = message.content[len('!md')+1:] 
            write_log(frontend_question_id)
            message.channel.send(f'`Marked problem {frontend_question_id} as DONE`')

            return

client.run(token)
