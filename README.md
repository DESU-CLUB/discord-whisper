# Discord-Whisper

Discord-Whisper is a powerful open source Discord bot that leverages OpenAI Whisper to provide real-time transcription in Discord voice channels.

## Features

- Accurate and Reliable: OpenAI Whisper has been trained on a massive amount of multilingual and multitask supervised data, making it highly accurate and reliable for transcription tasks.

- Easy Setup: Getting started with Discord-Whisper is straightforward. Simply invite the bot to your Discord server and give it the necessary permissions to join voice channels and transcribe conversations.


## Usage

1. Run this on your terminal: `pip install -r requirements.txt`

2. Invite Discord-Whisper to your server. A good guide on how to do so can be found [here](https://www.writebots.com/discord-bot-token/).

3. Add the bot key to botkey.txt.

4. Grant the bot the necessary permissions to join voice channels and access voice-related features.

5. Use the `!record` command to summon the bot into a voice channel. The bot will automatically start recording the conversation.

6. Use the `!stop_record` command to stop the recording. The bot will then transcribe the entirety of the conversation into a discord message, and send it to the channel `!record` was sent to. 

7. Enjoy the convenience of having voice channel transcriptions in your Discord server!

## Example Output
![Screenshot 1](demo_images/example.png)

## TODO

1. Add additional commands to customize the bot's behavior. For example, `!whisper language en` sets the transcription language to English.

2. Use faster Whisper models

3. Transcribe conversation into chunks in real time, rather than entire conversation in one go

4. Test model on scenarios where multiple speakers are talking at the same time.

5. Add more customisability in the form of confidence thresholds, filters, etc.

## Feedback and Support

If you encounter any issues, have suggestions, or need support, please open an issue at  the Discord-Whisper GitHub repository [here](https://github.com/DESU-CLUB/discord-whisper)

## Credits
Credits to OpenAI for their Whisper model, and pycord for voice channel recording capabilities.

## Conclusion

Discord-Whisper is a fantastic bot that brings the power of OpenAI Whisper to your Discord voice channels. With its accurate and real-time transcription capabilities, it enhances communication and accessibility within your server. Give it a try and make your voice conversations more inclusive and searchable!

