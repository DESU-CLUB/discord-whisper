import discord
from discord.ext import commands
from discord.sinks import WaveSink
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from whisper_jax import FlaxWhisperPipline


intents = discord.Intents.all()
intents.members = True
model =FlaxWhisperPipline("openai/whisper-large-v2")

bot = commands.Bot(command_prefix='!', intents=intents)
executor = ThreadPoolExecutor(max_workers=5)




@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


def transcribe(audio):
    text = model(audio)
    return text['text']

@bot.command()
async def join(ctx):
    print(ctx)
    channel = ctx.author.voice.channel
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")
        return
    elif ctx.voice_client != None:
        await ctx.send("I'm already in a voice channel!")
    else:
        await channel.connect()

def read_file(sink):
    with open('output.wav', 'wb') as file:
        file.write(sink.get_all_audio()[0].getvalue())


@bot.command()
async def record(ctx):
    async def my_callback(sink, *args):
        # Save the recorded audio to a file
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, read_file, sink)
        #run whisper on here
        text = await loop.run_in_executor(executor,transcribe,'output.wav')
        #If more than 4000 words, split into chunks
        if len(text) > 4000:
            for x in range(0, len(text), 4000):
                await ctx.send(f'{text[x:x+4000]}')
        else:
            await ctx.send(text)
        #delete file
        os.remove('output.wav')
        
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")
        return
    elif ctx.voice_client != None:
        await ctx.send("I'm already in a voice channel!")
        return
    else:
        channel = ctx.author.voice.channel
        await channel.connect()

    if ctx.voice_client == None:
        await ctx.send('I am not in a voice channel!')
        return
    
    elif ctx.voice_client and ctx.voice_client.is_connected():
        sink = WaveSink()
        ctx.voice_client.start_recording(sink,my_callback)

@bot.command()
async def stop_record(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client == None:
        await ctx.send("You are not in a voice channel!")
        return
    ctx.voice_client.stop_recording()
    await ctx.voice_client.disconnect()



if __name__ == "__main__":
    with open('mykey.txt','r') as f:
        key = f.read().strip()
        bot.run(key)
