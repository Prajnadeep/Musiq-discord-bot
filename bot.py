import discord
from discord.ext import commands
from pytube import YouTube, Search
import random
import requests
import json
import asyncio


# INIT
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&',intents=intents)


# FFMPEG Options
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}


# Server Emojis
play_emoji = ['<a:partyblob:889560132588027907>',
              '<a:emoji_19:864380696323162122>',
              '<a:2170_CatRainbowJam:889432104314757170>']


# On Ready
@bot.event
async def on_ready():
    print("Bot is online !")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="&h"))

# PING
@bot.command()
async def ping(ctx):
    latency = bot.latency
    latency_in_ms = round(latency * 1000, 1)
    await ctx.send(f"Pong! 🏓\nLatency: {latency_in_ms}ms")


# JOIN VOICE CHANNEL
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()


# LEAVE VOICE CHANNEL
@bot.command(name='leave', aliases=['dc'], description="To make the bot leave the voice channel")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Disconnected ! Bye bye 👋")
    else:
        await ctx.send("The bot is not connected to a voice channel 🙄")

# PAUSE
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
# RESUME
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

# PLAY MUSIC
@bot.command(name='play', aliases=['p'], description="play any song/url")
async def play(ctx,*msg):
    #check if connected to vc
    voice = ctx.message.guild.voice_client
    if voice is None:
        voiceChannel = ctx.message.author.voice.channel
        await voiceChannel.connect()
        print("Connected to voice")
        voice = ctx.message.guild.voice_client


    server = ctx.message.guild
    voice_channel = server.voice_client

    # Search query
    search = str(' '.join(msg))

    # Extract URL from song
    print("searching . .")
    await ctx.send("Just a moment . . I'm searching")

    
    # SEARCH
    query = Search(search)
    filename = query.results[0].title
    url = query.results[0].watch_url
    print("YT url = ", url)

    # Now get stream url from video url
    yt = YouTube(url)
    thubnail = YouTube(url).thumbnail_url
    audio_url = yt.streams.get_audio_only().url

    async with ctx.typing():   
        # Play URL
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            voice_channel.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
        else:
            voice_channel.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
   
    embedVar = discord.Embed(title="🎵\tNow playing : \n{}".format(filename),description=random.choice(play_emoji),color=0x00ff00)
    embedVar.set_image(url=thubnail)
    await ctx.channel.send(embed=embedVar)

# STOP MUSIC
@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()

# AUTO DISCONNECT
@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return

    # Check if the bot is connected to a voice channel
    voice_client = member.guild.voice_client
    if not voice_client:
        return

    # Check if everyone has left the voice channel
    voice_channel = voice_client.channel
    if len(voice_channel.members) == 1:  # Only the bot is in the voice channel
        await asyncio.sleep(30)  # Wait for 30 seconds
        if len(voice_channel.members) == 1:  # Still no one has joined
            await voice_client.disconnect()

# DISPLAY JOKE
@bot.command(description="display a joke")
async def joke(ctx):
    data = requests.get("https://v2.jokeapi.dev/joke/Any")
    y = json.loads(data.text)
    if y["type"] == "single":
        await ctx.channel.send(y["joke"])
    else:
        await ctx.channel.send(y["setup"])
        await asyncio.sleep(2)
        await ctx.channel.send(y["delivery"]) 

# MEME
@bot.command(name='meme', aliases=['MEME', 'Meme'], description="display a meme")
async def meme(ctx):
    try:
        url = 'https://meme-api.com/gimme'
        data = requests.get(url)
        y = json.loads(data.text)
        await ctx.send(y['url'])

    except:
        await ctx.send("Oh no!😖 Looks like something went wrong")

# VALO
@bot.command()
async def valo(ctx, username, tag):
    tag = tag.replace("#", "")

    async with ctx.typing(): 
    
        try:
            #Profile Info URL
            profileUrl = 'https://api.henrikdev.xyz/valorant/v1/account/'+username+'/'+tag
            profile = requests.get(profileUrl)
            profileData = json.loads(profile.text)

            # check if Valid Response
            responseStatus = profileData['status']
            if responseStatus!=200:
                await ctx.send("Please recheck the Username and Tag !")
            else:
                playerName = profileData['data']['name']
                playerTagline = profileData['data']['tag']
                playerCardUrl = profileData['data']['card']['wide']
                playerAccountLevel = profileData['data']['account_level']
                playerUUID = profileData['data']['puuid']
                
                # Tier Info
                rankingURL = 'https://api.henrikdev.xyz/valorant/v2/mmr/ap/'+username+'/'+tag
                rank = requests.get(rankingURL)
                rankData = json.loads(rank.text)

                currentTier = rankData['data']['current_data']['currenttierpatched']
                currentTierImage = rankData['data']['current_data']['images']['small']
                highestTier = rankData['data']['highest_rank']['patched_tier']

                # Last Match
                lastMatchURL = 'https://api.henrikdev.xyz/valorant/v3/matches/ap/'+username+'/'+tag
                lastMatch = requests.get(lastMatchURL)
                lastMatchData = json.loads(lastMatch.text)

                lastMatchMap = lastMatchData['data'][0]['metadata']['map']
                lastMatchMode = lastMatchData['data'][0]['metadata']['mode']

                allplayersArray = lastMatchData['data'][0]['players']['all_players']

                # Last Match Data
                for player in allplayersArray:
                    if playerUUID == player['puuid']:
                        character = player['character']
                        kills = player['stats']['kills']
                        deaths = player['stats']['deaths']
                        assists = player['stats']['assists']


                # DISPLAY RESULTS
                embedVar = discord.Embed(title="VALORANT Player Stats", color=0x00ff00)
                embedVar.add_field(name="\u200b", value='** 😎 ID** : '+playerName+' #'+playerTagline, inline=False)
                embedVar.add_field(name="\u200b", value='** ⌛ Account Level** : '+str(playerAccountLevel), inline=False)
                embedVar.add_field(name="\u200b", value='** ▶ Current Rank** : '+currentTier, inline=False)
                embedVar.add_field(name="\u200b", value='** ⬆ Highest Rank** : '+highestTier, inline=False)
                
                embedVar.add_field(name='\u200b',value='**------------------ LAST MATCH DETAILS ------------------**',inline=False)
                embedVar.add_field(name='\u200b',value='** 🗺 Map** - '+lastMatchMap, inline=False)
                embedVar.add_field(name='\u200b',value='** ⚔ Mode**: '+lastMatchMode, inline=False)
                embedVar.add_field(name='\u200b',value='** 🥴 Character**: '+character, inline=False)
                embedVar.add_field(name='\u200b',value='** 🔫 Kills**- '+str(kills), inline=False)
                embedVar.add_field(name='\u200b',value='** ☠ Deaths**- '+str(deaths), inline=False)
                embedVar.add_field(name='\u200b',value='** ❤ Assists**- '+str(assists), inline=False)

                embedVar.set_thumbnail(url=currentTierImage)
                embedVar.set_image(url=playerCardUrl)
                await ctx.send(embed=embedVar)

        except Exception as e:
            print(e)
            await ctx.send("Oh no!😖 Looks like something went wrong")

# HELP
@bot.command(name='h')
async def h(ctx):
    embedVar = discord.Embed(title="Hello, I am Musiq 🤖",
                             description="I am a multipurpose bot. I can play music,display memes and get exotic jokes for you from places unknown. Currently under development 💻 ", color=0x00ff00)
    embedVar.add_field(
        name="\u200b", value="**Author :** - <@494515438303051807> 😎", inline=False)
    embedVar.add_field(name="\u200b", value="**Prefix** - &", inline=False)
    embedVar.add_field(name="Current commands:",
                       value="----------------------------", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&valo** - Display Valorant player stats; usage: &valo Rock #X11", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&joke** - Display a joke", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&meme** - Display a meme", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&join** - Join the voice channel", inline=False)
    embedVar.add_field(name="\u200b", value="**&play/p song_name/url:** - Play music from url/search keyword",
                       inline=False)
    embedVar.add_field(
        name="\u200b", value="**&resume** - Continue playback", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&pause** - Pause the current track", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&stop** - Stop the current track", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&leave/&dc** - Disconnect", inline=False)
    await ctx.channel.send(embed=embedVar)

# HELLO
@bot.command(name='hello', aliases=['hi', 'Hi', 'Hello'])
async def hello(ctx):
    embedVar = discord.Embed(title="Hello, I am Musiq 🤖",
                             description="I am a multipurpose bot. I can play music,display memes and get exotic jokes for you from places unknown. Currently under development 💻 "+random.choice(play_emoji), color=0x00ff00)
    embedVar.add_field(
        name="\u200b", value="**Author :** - <@494515438303051807> 😎", inline=False)
    
    embedVar.add_field(
        name="\u200b", value="**Help :** - type & h for more info", inline=False)
    await ctx.channel.send(embed=embedVar)

# MAIN FUNCTION
if __name__ == "__main__" :
    bot.run("YOUR_TOKEN_HERE")
