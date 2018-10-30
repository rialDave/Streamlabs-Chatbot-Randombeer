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

This will come a little later, when this baby is "stable"

Changelog
---------

**v0.0.1**

  * initial Build

**v0.0.2 (was WIP)**

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

**v0.1.1**

  * Mostly code style related fixes
  * Added codacy badge

**Known bugs to fix:**

  * <s>Updating the beerdata.csv only saves the current line to the new file (discards all other lines that were there before) [see v0.0.2 above]</s>
  * Settings don't apply sometimes (discovered on "cooldown" setting)
  * "How to use" stuff still missing in this readme
  * Big one: create "beerdata.json" file if it doesn't exists (when one just installed the script)

**Future ideas (tell me what you need most):**

  * <s>Outputting 1., 2. and 3. as "first" "second" and "third" (hopefully low hanging fruits)</s>
  * Split Beercounter for: daily (or per stream?) and overall
  * Trigger gifs on !randombeer command
  * Blacklist users (maybe with streamlabs blacklist) to exclude bots from getting beer (what a shame!)
  * Combination with currency system from sl chatbot
  * !top10beers
  * More exception handling and debug information for streamers
  * Automatic backup function of beerdata.csv so that the data won't get lost
