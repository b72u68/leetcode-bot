import discord
import configparser
import random
from leetcodeScraper import leetcodeScraper

def read_token():
    config = configparser.ConfigParser()
    config.read(r'./.config/discord.ini')
    return config['DISCORD']['bot_token']

client = discord.Client()
token = read_token()

lc = leetcodeScraper("algorithms")
lc.getProblemList()

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

        commands = ['!', '!help', '!yeet', '!md', '!sl']
        guides = '''YeetCode Bot Command Guide
    \'!yeet <difficulty>\'              Send problem in <difficulty>
            (\'easy\': 1, \'medium\': 2, \'hard\': 3)
    \'!md <problemID>\'                 Mark problem as finished
    \'!sl <problemSlug> <language>\'    Send solution
            (language: python, python-3, c, cpp, java)'''

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
                        for questionInfo in data:
                            frontend_question_id = questionInfo.split()[0].strip()
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

            for problem in lc.problems:
                if problem['difficulty'] == difficulty and problem['frontend_question_id'] not in finishedProblems:
                    problemText = lc.getProblem(problem)

                    if problemText:
                        await message.channel.send(f'```{problemText}```')

                    else:
                        await message.channel.send('`Error Occurred. Try again.`')

                    break

            # randProblem = problemList[random.randint(0, len(problemList)-1)]
            # frontend_question_id = randProblem['frontend_question_id']

            # while frontend_question_id in finishedProblems:
                # randProblem = problemList[random.randint(0, len(problemList)-1)]

            # problemString = lc.getProblem(randProblem)

            # if problemString:
                # await message.channel.send(f'```{problemString}```')

            # else:
                # await message.channel.send('`Error Occurred. Try again.`')
            
            return

        if message.content.startswith('!md'):

            def write_log(frontend_question_id, question_title_slug):
                try:
                    with open("log.txt", "a") as f:
                        f.write(f'{frontend_question_id}    {question_title_slug}')
                        f.close()

                except Exception as e:
                    print(f'[-] Error Occurred:: {e}')

            frontend_question_id = message.content[len('!md')+1:] 

            question_title_slug = None

            for problem in lc.problems:
                if problem['frontend_question_id'] == frontend_question_id:
                    question_title_slug = problem['question_title_slug']

            if question_title_slug:
                write_log(frontend_question_id, question_title_slug)
                message.channel.send(f'`Marked problem {frontend_question_id}. {question_title_slug} as DONE`')
                return

            else:
                message.channel.send(f'`Invalid problem ID. Try again.`')
                return

        if message.content.startswith('!sl'):
            question_title_slug = message.content.split()[1].strip()
            language = message.content.split()[2].strip()

            solution = lc.getSolution(question_title_slug, language)

            if solution:
                await message.channel.send(f'```{solution}```')
                return

            else:
                await message.channel.send('`Error Occurred. Try again.`')
                return

client.run(token)
