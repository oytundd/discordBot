import discord
import logging
from botToken import myToken
from discord.ext import commands

client = discord.Client()

### LOGGER ###
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

### EVENTS ###
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'man':
        await message.channel.send(file=discord.File('pictures/man.png'))

    if message.content == 'my man':
        await message.channel.send(file=discord.File('pictures/myMan.jpg'))

client.run(myToken)
