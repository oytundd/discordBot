import discord
import logging
import re
import pickle
from collections import Counter
from botToken import myToken
from discord.ext import commands
import os
try:
    os.mkdir("pickleJar")
except:
    pass
emoteMatch = re.compile('<:.+?:\d+>')
bot = commands.Bot(command_prefix='.')
c = Counter()

### LOGGER ###
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

### EVENTS ###
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'man':
        await message.channel.send(file=discord.File('pictures/man.png'))

    if message.content == 'my man':
        await message.channel.send(file=discord.File('pictures/myMan.jpg'))

    if message.content:
        #print('{0.content} in {0.guild}'.format(message))
        m = emoteMatch.findall('{0.content}'.format(message))
        #print(m)
        if m:
            serverName = "pickleJar/"+'{0.guild}'.format(message)
            global c
            c += Counter(m)
            pickle.dump(c, open(serverName, "wb"))
            print(c)

    await bot.process_commands(message)

@bot.command()
async def counter(ctx):
    serverName = "pickleJar/"+str(ctx.message.guild)
    counterObject = pickle.load(open(serverName,"rb"))
    await ctx.send("Most popular emotes for the server "+str(ctx.guild)+":\n"+str(counterObject))


bot.run(myToken)