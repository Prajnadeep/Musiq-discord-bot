# Musiq-discord-bot
<div align="center">
  <p>
    <a href="#"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/40622675/244601014-9fbae3b3-5b47-4c59-972e-e5f542c17461.png" width="100" height="100" alt="Musiq Logo" /></a>
  </p>
  </div>
 
This is a multipurpose Discord bot that can play music from YouTube using search keywords or URLs. Additionally, it can display memes and jokes when prompted with the prefix "&" followed by specific commands

# Installation
To use this bot, you will need to have the following prerequisites:

* Python 3.6 or higher
* Discord.py library
* FFmpeg (for playing music)

1. Clone or download this repository to your local machine.

 Then generate the <b>token</b> and paste it in the script.
 ``` python
 client.run('YOUR TOKEN HERE')
 ```
2. Install the required dependencies by running the following command:
```python 
pip install -r requirements.txt
```
3. Run the bot using the following command :
```python 
python bot.py
```
4. Invite the bot to your Discord server using the OAuth2 URL generated for your bot. You can find detailed instructions on how to create and invite a bot to a Discord server [here.](https://discordpy.readthedocs.io/en/latest/discord.html)

# Usage
Once the bot is running and invited to your server, you can use the following commands:

* <b>&play</b> song_name: Plays a song from YouTube based on the provided search keyword.
* <b>&play</b> [YouTube_URL](https://youtu.be/dQw4w9WgXcQ): Plays the audio from the provided YouTube video URL.
* <b>&joke</b>: Displays a random joke.
* <b>&meme</b>: Displays a random meme.
<br>
  The bot also supports basic control commands:
<br>
  
* <b>&join</b>: Joins the voice channel of the user who issued the command.
* <b>&leave</b>: Leaves the current voice channel.
* <b>&pause</b>: Pauses the currently playing song.
* <b>&resume</b>: Resumes a paused song.
* <b>&stop</b>: Stops playing and clears the song queue.
* <b>&ping</b>: Displays the bot latency in ms.
  
  
# Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.

When contributing code, make sure to follow the existing coding style and submit a pull request with your changes. Please provide clear descriptions and context for your changes to facilitate the review process.
  
# Acknowledgments
  
* [Discord.py](https://discordpy.readthedocs.io/en/stable/) - Discord API wrapper for Python.
* [pytube](https://github.com/pytube) - Python library (and command-line utility) for downloading YouTube videos
* [FFmpeg](https://ffmpeg.org/) - Open-source software for handling multimedia data.
* <a href="https://www.flaticon.com/free-icons/music" title="music icons">Music icons created by Freepik - Flaticon</a>
