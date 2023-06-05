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
        name="\u200b", value="**&joke** - display a joke", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&meme** - display a meme", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&join** - join the voice channel", inline=False)
    embedVar.add_field(name="\u200b", value="**&play/p song_name/url:** - play music from url/search keyword",
                       inline=False)
    embedVar.add_field(
        name="\u200b", value="**&resume** - continue playback", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&pause** - pause the current track", inline=False)
    embedVar.add_field(
        name="\u200b", value="**&stop** - stop the current track", inline=False)
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
