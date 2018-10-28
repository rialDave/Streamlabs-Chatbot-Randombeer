# Streamlabs-Chatbot-Randombeer
A Python Script for Streamlabs Chatbot to gift some random user a "Beer" (similar to currencies by SL Chatbot)

# How to install (still "Alpha af!') 

1. Go to this directory (starting from the root where Streamlabs Chatbot is installed):
```
Services\Scripts\
```
2. Create a new Folder called _"RandomBeer"_
3. Drop all of the stuff from this Repository in there
4. Reload the scripts in SL Chatbot and you're good to go!

If you're having trouble with loading scripts in the SL Chatbot, see: https://www.youtube.com/watch?v=l3FBpY-0880

# How to use

This will come a little later, when this baby is "stable at 0.0.2

# Changelog

**v0.0.1**

* initial Build

**v0.0.2 [WIP]**

* [x] parse first command
* [x] Add .gitignore for .csv files
* [x] check if randuser is already in file then plus 1
* [ ] fix error when moving written temp file
* [ ] if not found add new line with viewer name and st to 1
* [x] parse second command: check file for given username and print out value
* [x] outputting 1., 2. and 3. as "first" "second" and "third" (hopefully low hanging fruits | edit: yeah it was)

**Known bugs to fix:**

* Updating the beerdata.csv only saves the current line to the new file (discards all other lines that were there before) [see v0.0.2 above]
* Settings don't apply sometimes (discovered on "cooldown" setting)

**Future ideas (tell me what you need most):**

* <s>outputting 1., 2. and 3. as "first" "second" and "third" (hopefully low hanging fruits)</s>
* Trigger gifs on !randombeer command
* blacklist users (maybe with streamlabs blacklist) to exclude bots from getting beer (what a shame!)
* combination with currency system from sl chatbot
* !top10beers
* More exception handling and debug information for streamers
* Automatic backup function of beerdata.csv so that the data won't get lost
