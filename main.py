import discord
import youtube_dl
import os
from discord.ext.commands import Bot


bot = Bot(command_prefix='!')
token = "" #hidden for privacy reasons

@bot.event
async def on_ready():
    print("We have logged in as {0}".format(bot.user))
    await bot.change_presence(activity = discord.Game("Music"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send("Hello!")

    await bot.process_commands(message)

@bot.command(name = 'server', help = "Fetches server information")
async def fetchServerInfo(context):
    guild = context.guild

    await context.send("Server Name: {0}".format(guild.name))
    await context.send("Server Size: {0}".format(len(guild.members)))

@bot.command()
async def play(ctx, url: str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Already playing a song.")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'General') #search for voice channel name
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild) #searching through voice client in the guild
    
    #if not voice.is_connected():
        #await voiceChannel.connect()
    
    #if url == "":
        #await ctx.send("Enter a url to play music.")

    ydl_opts = {
        'format': "bestaudio/best",
        'postprocessors': [{
            'key': "FFmpegExtractAudio",
            'preferredcodec': "mp3",
            'preferredquality': "192",
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command() #disconnects the bot
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("The bot is not playing anything.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@bot.command() #stop music but doesn't disconnect the bot
async def stop(ctx): 
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_connected():
        voice.stop()
    else:
        await ctx.send("Bot is not connected.")

bot.run(token)
