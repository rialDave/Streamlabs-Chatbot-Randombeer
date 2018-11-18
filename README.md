Streamlabs-Chatbot-Randombeer
=============================

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/801907104a8a466eaf42e0362cb9f7b1)](https://app.codacy.com/app/rialDave/Streamlabs-Chatbot-Randombeer?utm_source=github.com&utm_medium=referral&utm_content=rialDave/Streamlabs-Chatbot-Randombeer&utm_campaign=Badge_Grade_Dashboard)

A Python Script for Streamlabs Chatbot to gift some random user a "Beer" (similar to currencies by SL Chatbot)

How to install (still "Alpha af!") 
----------------------------------

1. Go to this directory (starting from the root where Streamlabs Chatbot is installed):

```plain
Services\Scripts\
```

2. Create a new Folder called _"RandomBeer"_
3. Drop all of the stuff from this Repository in there
4. Reload the scripts in SL Chatbot and you're good to go!

If you're having trouble with loading scripts in the SL Chatbot, see: https://www.youtube.com/watch?v=l3FBpY-0880

How to use
------------

You don't really need to (and can, because the user config is still buggy) configure much.
Just call the command "!randombeer" in your stream and have fun!

Changelog
---------

**v0.0.1**

  * initial Build

**v0.0.2**

  * parse first command
  * Add .gitignore for .csv files
  * check if randuser is already in file then plus 1
  * parse second command: check file for given username and print out value
  * outputting 1., 2. and 3. as "first" "second" and "third" (hopefully low hanging fruits | edit: yeah it was)

**v0.1.0 (Alpha)**

  * First working version: sending beer with "!randombeer" to random user which is stored and updated in json file
  * fix error when moving written temp file
  * if not found add new line with viewer name and set to 1
  * Biggest thing: switch from csv to json data storage

**v0.1.1 (don't use this, was buggy)**

  * Mostly code style related fixes
  * Added codacy badge

**v0.2.0**

  * Fixes a bug of v0.1.1 that caused the script to crash on load
  * Fixes a known bug: data file "beerdata.json" is now created on "load" of the script, if it didnt exist yet.
  * Implements new Feature: Split Beercounter for: daily and overall counters

**v0.2.1**

  * Fixes a dumb bug in v2.0.0 where i forgot to remove the testing user-override^^
  * Some preset changes and readme updated with a new idea

**Known bugs to fix:**

  * <s>Updating the beerdata.csv only saves the current line to the new file (discards all other lines that were there before) [see v0.0.2 above]</s>
  * <s>Big one: create "beerdata.json" file if it doesn't exists (when one just installed the script)</s>
  * Settings don't apply sometimes (discovered on "cooldown" and "command" setting; seem to load the fallback from "Settings_Module.py" then til you save your script settings again with a click.
  * <s>"How to use" stuff still missing in this readme</s>
  * Think about: can you set a username ont Twitch to one including umlauts (ö,ä,ü)? The script would most likely crash then

**Future ideas in priority order (tell me what you need most):**

  * <s>Outputting 1., 2. and 3. as "first" "second" and "third" (hopefully low hanging fruits)</s>
  * <s>Split Beercounter for: daily (or per stream?) and overall</s>
  * <s>Replace complete "parseString" if beercount is exactly 1 in Parse() so it will display a completely different response for the first beer today and maybe the first ever additionally</s>
  * Limit of beers for today (user gets too drunk)
  * Automatic backup function of beerdata.csv so that the data won't get lost
  * Blacklist users (maybe with streamlabs blacklist) to exclude bots from getting beer (what a shame!) and then get switch from "random active users" to "random users"
  * !top10beers
  * More exception handling and debug information for streamers
  * Trigger gifs on !randombeer command
  * Combination with currency system from sl chatbot