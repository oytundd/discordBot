import discord
import logging
from botToken import myToken
from discord.ext import commands


bot = commands.Bot(command_prefix='.')

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
        print('Message from {0.author}: {0.content}'.format(message))
            
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(myToken)