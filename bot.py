import discord
import logging
import re
import pickle
from collections import Counter
import botParameters
from discord.ext import commands
import os
import urllib.request, json
from datetime import datetime
import humanize
import os, ssl
import subprocess
import aiohttp
import socket
import asyncio
tempMsgSwitch = True
tempMsgList = []
try:
    import lastServer
except:
    pass
try:
    os.mkdir("pickleJar")
except:
    pass


### REQUESTS FIX
# if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
#     ssl._create_default_https_context = ssl._create_unverified_context

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
### ### ###

### EVENTS ###
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    try:
        lastChannel = bot.get_channel(lastServer.channelId)
        await lastChannel.send("Live!")
    except:
        pass
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

    if message.content:#
        tempMsgList.append(message)
        if tempMsgList[0].content == tempMsgList [1].content and tempMsgList[1].content == tempMsgList [2].content and tempMsgList[0].author != tempMsgList[1].author and tempMsgList[1].author != tempMsgList[2].author  and tempMsgList[0].author != tempMsgList[2].author:
            tempMsgList.clear()
            await message.channel.send(message.content)
    
        elif len(tempMsgList) >= 3:
            tempMsgList.pop(0)


    if message.content:#EMOTE COUNTER EMOTE RECOGNITION
        #print('{0.content} in {0.guild}'.format(message))
        m = emoteMatch.findall('{0.content}'.format(message))
        #print(m)
        if m:
            for emoteInMessage in m:
                emojiIDs0 = str(emoteInMessage)
                emojiIDs1 = emojiIDs0[-21:] 
                emojiIDstr = emojiIDs1[:-3]
                emojiID = int(emojiIDstr)
                emojiObject = bot.get_emoji(emojiID)
                #print(emojiID)
                #print(emojiObject)
                if emojiObject.is_usable():
                    serverName = "pickleJar/"+'{0.guild}'.format(message)
                    global c
                    c = Counter(emoteInMessage)
                    try:
                        with open(serverName,"rb") as toRead:
                            z = pickle.load(toRead)
                            x = c + z
                            #s = sorted(x.items(),key=lambda x:x[1])
                        
                        with open(serverName,"wb") as toWrite:
                            pickle.dump(x,toWrite)
                    except:
                        with open(serverName,"wb") as toWrite:
                            pickle.dump(c,toWrite)    
    await bot.process_commands(message)

@bot.command()
async def counter(ctx,arg =None):
    serverName = "pickleJar/"+str(ctx.message.guild)
    try:
        with open(serverName,"rb") as toRead:
            counterObject = pickle.load(toRead)
        sortedObject = counterObject.most_common(None)
        if arg =="r":
            sortedObject.reverse()
        #print(type(sortedObject))
            counterEmbed = discord.Embed(title="📉 - Least popular emotes for "+str(ctx.guild),color =0xE85F5C)
            counterEmbed.set_thumbnail(url=str(ctx.guild.icon_url))
            for i in range(len(sortedObject)):
                counterEmbed.add_field(name=sortedObject[i][0], value = sortedObject[i][1],inline=True)
            await ctx.send(embed=counterEmbed)
                #await ctx.send("Most popular emotes for the server "+str(ctx.guild)+":\n"+str(counterObject))
        else:
             #print(type(sortedObject))
            counterEmbed = discord.Embed(title="📈 - Most popular emotes for "+str(ctx.guild),color =0xE85F5C)
            counterEmbed.set_thumbnail(url=str(ctx.guild.icon_url))
            for i in range(len(sortedObject)):
                counterEmbed.add_field(name=sortedObject[i][0], value = sortedObject[i][1],inline=True)
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
    ### PI PIX https://github.com/aio-libs/aiohttp/issues/2522
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        verify_ssl=False,
    )
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get('https://www.thecocktaildb.com/api/json/v1/1/random.php') as url:
            cockDict = await url.json() #json.loads(url.read().decode())
    # with urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v1/1/random.php") as url:
    #     cockDict = json.loads(url.read().decode())
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
async def meal(ctx):
    ### PI PIX https://github.com/aio-libs/aiohttp/issues/2522
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        verify_ssl=False,
    )
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get('https://www.themealdb.com/api/json/v1/1/random.php') as url:
            mealDict = await url.json() #json.loads(url.read().decode())
    # with urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v1/1/random.php") as url:
    #     cockDict = json.loads(url.read().decode())
    mealUrl = "https://www.themealdb.com/meal/"+mealDict['meals'][0]['idMeal']
    mealName = mealDict['meals'][0]['strMeal']
    mealDesc = mealDict['meals'][0]['strInstructions']
    mealEmbed = discord.Embed(title=mealName, description="["+mealDesc+"]("+mealUrl+")",color =0xE85F5C)
    mealEmbed.set_thumbnail(url=mealDict['meals'][0]['strMealThumb'])
    mealEmbed.add_field(name='Category', value= mealDict['meals'][0]['strCategory'])
    
    mealEmbed.set_footer(text="Powered by thethemealdb.com")
    for i in range(1,21,1):
        ing = 'strIngredient'+str(i)
        mes = 'strMeasure'+str(i)
        if mealDict['meals'][0][ing]:
            mealEmbed.add_field(name=mealDict['meals'][0][ing],value = mealDict['meals'][0][mes])
        
    await ctx.send(embed=mealEmbed)
@bot.command()
async def up(ctx):
    upCommandTime = datetime.now()
    upTime =  upCommandTime - launchTime
    #await ctx.send(upTime.weeks+"week(s)"+str(upTime.days)+"day(s)"+str(upTime.hours)+"hour(s)"+str(upTime.minutes))
    await ctx.send("I have been up for "+ humanize.naturaldelta(upTime))
@bot.command()
async def update(ctx):
    if ctx.author.id == 82987768711483392:
        with open("lastServer.py", "w+") as writeLastServer:
            writeLastServer.write("guildId = "+str(ctx.guild.id)+"\nchannelId="+str(ctx.channel.id) )
        await ctx.send("Updating...")
        subprocess.call("./updateScript.sh")
        await bot.close()
    else:
        await ctx.send("Unauthorized entry, will self destruct in 5 seconds.")
@bot.command()
async def die(ctx):
    if ctx.author.id == 82987768711483392:
        await ctx.send("Goodbye...")
        bot.close()
@bot.command()
async def recipe(ctx, *, arg):
    conn = aiohttp.TCPConnector(
    family=socket.AF_INET,
    verify_ssl=False,
    )
    async with aiohttp.ClientSession(connector=conn) as session:
        getVar = 'https://api.edamam.com/search?q='+arg+'&app_id='+botParameters.edamameID+'&app_key='+botParameters.edamemeToken+'&from=0&to=100'
        print(getVar)
        async with session.get(getVar) as url:
            recipeResult = await url.json() #json.loads(url.read().decode())
            if recipeResult:
                print('hit!')
            recipeEmbed = discord.Embed(title=str(len(recipeResult['hits']))+' results were found for '+arg,color =0xE85F5C)
            #for i in range(1,hitCount,1):
            for i in range(len(recipeResult['hits'])):
                recipeUrl       =recipeResult['hits'][i]['recipe']['url']
                recipeSource    =recipeResult['hits'][i]['recipe']['source']
                recipeEmbed.add_field(name=recipeResult['hits'][i]['recipe']['label'],value="["+recipeSource+"]("+recipeUrl+")")
                if i > 25:
                    break
            recipeEmbed.set_footer(text="Powered by edamam.com")
            myMessage = await ctx.send(embed=recipeEmbed)
            #await myMessage.add_reaction('⬅️')
            #await myMessage.add_reaction('➡️')
    
            


            # await myMessage.add_reaction('\U00002b05\U0000fe0f')
            # await myMessage.add_reaction('\U000027a1\U0000fe0f')
                
                




bot.run(botParameters.myToken)