This project downloads twitch clips from twitch.tv, renders the clips together using Vegas Pro's editing software, and then uploads the rendered video to youtube.

RenderScript.cs is a c# script used by Vegas Pro to edit downloaded clips together
/
Vegas Pro Scripting API file included under vegas_scripting_api for reference
/

Chromedriver.exe is needed for the Selenium library to be used through Chrome
/
/

TwitchClipScraper.py contains the main driver for the program
/
Multi-threaded to accomidate each twitch category being downloaded from
Calls a sub process of Vegas Pro to edit the downloaded clips together
Execution of the script continues after Vegas Pro is closed, opening up youtube.com
Signs into youtube.com using information that I provided(Information removed from github repository)
Uploads edited videos to logged in channel
/

A lot of the file paths are static because this is not meant to be shared

Games.txt
/
A list of all the categories to scrape clips from
/
