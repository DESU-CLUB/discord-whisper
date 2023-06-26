import discord
from discord.ext import commands
from discord.sinks import WaveSink
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from whisper_jax import FlaxWhisperPipline
import io
import numpy as np
import wave
import jax.numpy as jnp
import time
intents = discord.Intents.all()
intents.members = True

model =FlaxWhisperPipline("openai/whisper-large-v2", dtype=jnp.float16)

bot = commands.Bot(command_prefix='!', intents=intents)
executor = ThreadPoolExecutor(max_workers=5)

   
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')




async def start_recording(ctx,sink,my_callback,*args):
    ctx.voice_client.start_recording(sink,my_callback,ctx,args)
    return

def transcribe(audio):
    start = time.time()
    text = model(audio)
    print('FInish transcription', time.time()-start)
    os.unlink(audio)
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


import io
import numpy as np
import wave

import io
import os
import tempfile



async def my_callback(sink, *args):
        # Save the recorded audio to a file
        ctx,summarize = args
        loop = asyncio.get_event_loop()
        start = time.time()
        progress = await ctx.send('Reading bytes...')
        data = await loop.run_in_executor(executor,read_file,sink)
        #run whisper on here
        print('Reading bytes',time.time()-start)
        await progress.edit('Transcribing...')
        start = time.time()
        text = await loop.run_in_executor(executor,transcribe,data)
        print('Transcribed', time.time()-start)
        #If more than 4000 words, split into chunks
        if len(text) > 4000:
            for x in range(0, len(text), 4000):
                if x == 0:
                    await progress.edit(f'{text[x:x+4000]}')
                await ctx.send(f'{text[x:x+4000]}')
        else:
            await progress.edit(text)


def read_file(sink):
    try:
        all_audio = sink.get_all_audio()
        if not all_audio:
            print("No audio data in sink")
            return None

        # Get WAV data bytes
        wav_data_bytes = all_audio[0].getvalue()

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_filename = temp_file.name

        # Write the WAV data bytes to the temporary file
        with open(temp_filename, 'wb') as f:
            f.write(wav_data_bytes)

        # Delete the temporary file
        return temp_filename

    except Exception as e:
        print(f'Error in read_file: {e}')
        return None




@bot.command()
async def record(ctx):
        #delete file        
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")
        return
    elif ctx.voice_client != None and ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.send("I'm already in another voice channel!")
        return
    else:
        channel = ctx.author.voice.channel
        if ctx.voice_client == None:
            await channel.connect()

    if ctx.voice_client == None:
        await ctx.send('I am not in a voice channel!')
        return
    
    elif ctx.voice_client and ctx.voice_client.is_connected():
        print('Working!')
        sink = WaveSink()
        await start_recording(ctx,sink,my_callback)
        return
    else:
        await ctx.send('Unknown Error Found!')
        return

@bot.command()
async def stop_record(ctx):
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel!")
        return

    try:
        # Check if the bot is actively recording before stopping the recording
        ctx.voice_client.stop_recording()
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    
    
@bot.command()
async def disconnect(ctx):
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel!")
        return
    await ctx.voice_client.disconnect()



if __name__ == "__main__":
    with open('mybot.txt','r') as f:
        key = f.read().strip()
        bot.run(key)
