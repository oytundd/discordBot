import discord
import logging
import re
import pickle
from collections import Counter
from botToken import myToken
from discord.ext import commands
import os
import urllib.request, json
from datetime import datetime
import humanize
import os, ssl
import subprocess
try:
    os.mkdir("pickleJar")
except:
    pass


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

emoteMatch = re.compile(r"<:.+?:\d+>")
#emoteMatchid = re.compile("<:.+?:(\d+)>")
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
    global launchTime
    launchTime = datetime.now()
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'man':
        #await message.channel.send(file=discord.File('pictures/man.png'))
        await message.channel.send('https://pbs.twimg.com/media/EUwtJWaXgAE_sZh.png:large')

    if message.content == 'horse':
        await message.channel.send('https://pbs.twimg.com/media/EUwvxkQXYAA-FY9.jpg:large')
    if message.content == 'my man':
        await message.channel.send('https://pbs.twimg.com/media/EazYe-9WoAA0i9L.jpg')

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
                    mySorted = sorted(x.items(),key=lambda x:x[1])
                    pickle.dump(mySorted,toWrite)
            except:
                with open(serverName,"wb") as toWrite:
                    pickle.dump(c,toWrite)    
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
@bot.command()
async def latency(ctx):
    await ctx.send(bot.latency)
@bot.command()
async def cocktail(ctx):
    with urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v1/1/random.php") as url:
        cockDict = json.loads(url.read().decode())
    drinkUrl = "https://www.thecocktaildb.com/drink/"+cockDict['drinks'][0]['idDrink']
    drinkName = cockDict['drinks'][0]['strDrink']
    drinkDesc = cockDict['drinks'][0]['strInstructions']
    cockEmbed = discord.Embed(title=drinkName, description="["+drinkDesc+"]("+drinkUrl+")",color =0xE85F5C)
    cockEmbed.set_thumbnail(url=cockDict['drinks'][0]['strDrinkThumb'])
    cockEmbed.add_field(name='Glass Type', value= cockDict['drinks'][0]['strGlass'])
    
    cockEmbed.set_footer(text="Powered by thecocktaildb.com")
    for i in range(1,16,1):
        ing = 'strIngredient'+str(i)
        mes = 'strMeasure'+str(i)
        if cockDict['drinks'][0][ing] != None:
            cockEmbed.add_field(name=cockDict['drinks'][0][ing],value = cockDict['drinks'][0][mes])
        
    await ctx.send(embed=cockEmbed)
@bot.command()
async def up(ctx):
    upCommandTime = datetime.now()
    upTime =  upCommandTime - launchTime
    #await ctx.send(upTime.weeks+"week(s)"+str(upTime.days)+"day(s)"+str(upTime.hours)+"hour(s)"+str(upTime.minutes))
    await ctx.send("I have been up for "+ humanize.naturaldelta(upTime))
@bot.command()
async def update(ctx):
    if ctx.author.id == 82987768711483392:
        await ctx.send("Updating...")
        subprocess.call("./updateScript.sh")
        await bot.close()
    else:
        await ctx.send("Unauthorized entry, will self destruct in 5 seconds.")
bot.run(myToken)