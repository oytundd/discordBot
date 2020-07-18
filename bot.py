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

emoteMatch = re.compile("<:.+?:\d+>")
emoteMatchid = re.compile("<:.+?:(\d+)>")
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
            c = Counter(m)
            try:
                with open(serverName,"rb") as toRead:
                    z = pickle.load(toRead)
                    x = c + z
                with open(serverName,"wb") as toWrite:
                    pickle.dump(x,toWrite)
            except:
                with open(serverName,"wb") as toWrite:
                    pickle.dump(c,toWrite)    
            """
            file =  open(serverName, "wb+")
            try:
                z = pickle.load(file)
                x = c + z
                pickle.dump(x, file)
                file.close()
                print(x)
            except EOFError:
                pickle.dump(c,file)
                file.close()
                print(c)
            """



    await bot.process_commands(message)

@bot.command()
async def counter(ctx):
    serverName = "pickleJar/"+str(ctx.message.guild)
    try:
        with open(serverName,"rb") as toRead:
            counterObject = pickle.load(toRead)
        counterEmbed = discord.Embed(title="Emote usage for "+str(ctx.guild),color =0xE85F5C)
        counterEmbed.set_thumbnail(url=str(ctx.guild.icon_url))
        for key in counterObject:
            counterEmbed.add_field(name=key, value = counterObject[key],inline=True)
        await ctx.send(embed=counterEmbed)
            #await ctx.send("Most popular emotes for the server "+str(ctx.guild)+":\n"+str(counterObject))
    except Exception as e:
        print(e)
        #await ctx.send("There are no recorded emotes for this server")
@bot.command()
async def icon(ctx):
    await ctx.send(str(ctx.guild.icon_url))
@bot.command()
async def emotes(ctx):
    print(ctx.guild.emojis)


bot.run(myToken)