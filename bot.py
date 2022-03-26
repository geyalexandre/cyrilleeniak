import discord
import setproctitle
from discord.ext import commands
from pytube import YouTube

musicQueue = []
client = commands.Bot(command_prefix="!")

@client.command()
async def queue(ctx, entry):
    ctx.send("Queuing {}".format(entry))
    musicQueue.append(entry)

def checkQueue(ctx):
    if len(musicQueue) > 0:
        newElem = musicQueue[0]
        musicQueue.pop(0)
        play(ctx, newElem)

@client.command()
async def play(ctx, url : str):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice:
        await join(ctx)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        video = YouTube(url)
        audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
        path = audio.download(filename='music.mp4')
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=path.split("/")[-1]))


@client.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

#######################
######## MAIN #########
#######################
setproctitle.setproctitle('cyril-lee-niak')
client.run('OTU1MTc0NjYzMTM3NDA3MDI2.Yjd1uQ.Mj6jsjEQyOAInjXSfWcw2wXJzOA')