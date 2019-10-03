#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import random
import time
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "RandomBeer"
Website = "https://twitch.tv/rialDave/"
Description = "Gifts a beer 'currency' to any random user in the chat and counts how many beers one user has got yet."
Creator = "rialDave"
Version = "0.4.0"

#---------------------------
#   Define Global Variables
#---------------------------
SettingsPath = ""
ScriptSettings = MySettings()

beerFilename = os.path.join('data', 'beerdata.json')
beerFilepath = os.path.join(os.path.dirname(__file__), beerFilename)

# Configuration of keys in json file
JSONVariablesBeercountToday = 'beercounttoday'
JSONVariablesBeercountOverall = 'beercountoverall'
JSONVariablesLastbeer = 'lastbeer'
JSONVariablesDrunkleveltoday = 'drunkleveltoday'

# syntax: drunklevel-id: max. beercount for this drunklevel
# known issue: this is checked too late in the code atm: e.g. the user will be able to get 4 instead of 3 beer when having drunklevel 1
VariablesDrunklevel = {
    "1": 3,
    "2": 5,
    "3": 10
}

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Checks if beerfile exists, if it doesnt: creates it
    if os.path.isfile(beerFilepath) == 0:
        data = {}
        with open(beerFilepath, 'w') as f:
            json.dump(data, f, indent=4)

    #   Load settings
    SettingsFile = os.path.join("Settings", "settings.json")
    SettingsPath = os.path.join(os.path.dirname(__file__), SettingsFile)
    ScriptSettings = MySettings(SettingsPath)
    ScriptSettings.Response = "Overwritten file!"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Command on cooldown! Seconds remaining: " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

    #   Check if the propper command is used, the command is not on cooldown to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        ParsedResponse = Parse(ScriptSettings.Response)    # Parse response first
        Parent.SendStreamMessage(ParsedResponse)    # Send your message to chat
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown

    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#   I don't really know what this does, but seems to be required to at least have an empty function defined.
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
#   Here's where the magic happens, all the strings are sent and processed through this function
#   
#   Parent.FUNCTION allows to use functions of the Chatbot and other outside APIs (see: https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Parent)
#
# ORIGINAL DEF: def Parse(parseString, userid, username, targetid, targetname, message):
#---------------------------
def Parse(parseString):
    # get a random active user from chat and afterwards their displayname
    randUser = Parent.GetRandomActiveUser()
    randUsername = Parent.GetDisplayName(randUser)

    # just a fallback, luckily this didn't happen while being live too often yet
    if randUsername == "":
        return "DaveDebug: generated random username was an empty string again, what the heck?"

    if IsDrunkToday(randUsername) == False:
        # Randombeer variable called
        if "$randomuser" in parseString:

            # Adds a new Beer for given Username
            AddBeerForUsername(randUsername)
            # Replacing the variable "$randomuser" of the configured command text with the correct username which got the new beer 
            parseString = parseString.replace("$randomuser", str(randUsername))

        # Beercountoverall variable for "overall" called, this sets the overall beercount of the randomuser which was called here
        if "$beercountoverall" in parseString:
            beerCount = GetBeerCountForUsernameAndType(randUsername, JSONVariablesBeercountOverall)

            # if it's the very first beer for user overall, use a different return text (hardcoded). If not: Replaces the string with the correct localization text for "beerCount"
            if beerCount == 1:
                parseString = "Congratulations! That's " + randUsername + "'s very first beer ever!"

            else:
                parseString = parseString.replace("$beercountoverall", GetCountLocalization(beerCount))

        # Beercounttoday variable for "today" called, this sets the todays beercount for the random user which was called here
        if "$beercounttoday" in parseString:
            beerCount = GetBeerCountForUsernameAndType(randUsername, JSONVariablesBeercountToday)
            parseString = parseString.replace("$beercounttoday", GetCountLocalization(beerCount))
    else:
        if GetDrunkLevel(randUsername) == 1:
            parseString = "Oh shit " + randUsername + ", you probably didn't eat a Schweinsbron before drinking - he's already drunk today!"
        if GetDrunkLevel(randUsername) == 2:
            parseString = randUsername + ", you should stop the fun now, you've got to work tomorrow!"
        if GetDrunkLevel(randUsername) == 3:
            parseString = "Already 5 Maß?! Are you crazy " + randUsername + "? Now I understand why you can't walk straight anymore."

    # after every necessary variable was processed: return the whole parseString
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsPath)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

#---------------------------
#   Own Functions: ModifyBeerFile: Function for Modfiying the file which contains the beer guys and according counters, see data/beerdata.json
#---------------------------
def AddBeerForUsername(username):

    currenttimestamp = int(time.time())
    currentday = datetime.fromtimestamp(currenttimestamp).strftime('%Y-%m-%d')

    # this loads the data of the beer file beerdata.json into variable "data"
    with open(beerFilepath, 'r') as f:
        data = json.load(f)

        # check if the given username exists in data. -> user doesnt exist yet, create array of the user data, which will be stored in beerdata.json
        if str(username.lower()) not in data:
            data[str(username.lower())] = {}
            data[str(username.lower())][JSONVariablesBeercountToday] = 1
            data[str(username.lower())][JSONVariablesBeercountOverall] = 1
            data[str(username.lower())][JSONVariablesLastbeer] = currentday
            data[str(username.lower())][JSONVariablesDrunkleveltoday] = GetRandomDrunkLevel()

        # if the user already exists, update the user with added beercounts, but we need to check here if it's the first beer today or not to set the right values 
        else:
            # new day since last beer? -> only count beercountoverall up, set beercounttoday to 1 again because it's a new day to start.
            if currentday != data[str(username.lower())][JSONVariablesLastbeer]:
                data[str(username.lower())][JSONVariablesBeercountToday] = 1
                data[str(username.lower())][JSONVariablesBeercountOverall] += 1
                data[str(username.lower())][JSONVariablesLastbeer] = currentday
                data[str(username.lower())][JSONVariablesDrunkleveltoday] = GetRandomDrunkLevel()

            # same day since last beer? -> count both up since we have still the same day since the last beer for the given user
            else:
                if IsDrunkToday(username) == False:
                    data[str(username.lower())][JSONVariablesBeercountToday] += 1
                    data[str(username.lower())][JSONVariablesBeercountOverall] += 1
                    data[str(username.lower())][JSONVariablesLastbeer] = currentday

    # after everything was modified and updated, we need to write the stuff from our "data" variable to the beerdata.json file 
    os.remove(beerFilepath)
    with open(beerFilepath, 'w') as f:
        json.dump(data, f, indent=4)

    return

#---------------------------
#   Own Functions: GetBeerCountForUsernameAndType: Returns the current beer count of a specific type (today or overall) as int
#   Params: username, beercounttype (JSONVariablesBeercountOverall or JSONVariablesBeercountToday)
#---------------------------
def GetBeerCountForUsernameAndType(username, beercounttype):
    # reads the beerdata.json into "data" variable again 
    with open(beerFilepath, 'r') as f:
        data = json.load(f)

    # if the given username doesn't exist in data, return error. Else return the value of the beercount for this user.
    # specialty: the submitted param "beercounttype" needs to be one of the examples in function description (also defined as global variables in the beginning of the script)
    # so it matches with the array key and returns the correct value
    # (this is just for saving some lines of code since it's more intelligent)
    if str(username.lower()) not in data:
        Parent.Log('Error', 'Oh shit, something went wrong when getting the beercount.')
    else:
        return data[str(username.lower())][beercounttype]

#---------------------------
#   Own Functions: GetCountLocalization: Returns "first", "second" and "third" instead of 1., 2., 3. if none are mapping, then it just outputs the given number again
#
#   returns: checked or translated number as a string
#---------------------------
def GetCountLocalization(beerCounter):

    # prepend "th" string to the beercount number if its higher than 3 
    if beerCounter > 3:
        return str(beerCounter) + "th"

    # build mapping for the first three numbers to be readable.
    beerCounterMapping = ["first", "second", "third"]

    # since the previously created array matches with the keys 0, 1 and 2 it can be directly used when subtracting integer value 1 from the key.
    return str(beerCounterMapping[int(beerCounter) - 1])


#---------------------------
#   Own Functions: GetRandomDrunkLevel
#
#   returns: int drunklevel
#---------------------------
def GetRandomDrunkLevel():
    return random.randrange(1, 4)

#---------------------------
#   Own Functions: GetDrunkLevel
#
#   returns: int drunklevel of given username
#---------------------------
def GetDrunkLevel(username):
    # reads the beerdata.json into "data" variable again 
    with open(beerFilepath, 'r') as f:
        data = json.load(f)

        return data[str(username.lower())][JSONVariablesDrunkleveltoday]

#---------------------------
#   Own Functions: IsDrunkToday
#
#   returns: Boolean if the user is drunk or not
#---------------------------
def IsDrunkToday(username):

    # reads the beerdata.json into "data" variable again 
    with open(beerFilepath, 'r') as f:
        data = json.load(f)

        if (JSONVariablesDrunkleveltoday in data[str(username.lower())]):
            
            beercountToday = GetBeerCountForUsernameAndType(username, JSONVariablesBeercountToday)
            drunklevelToday = data[str(username.lower())][JSONVariablesDrunkleveltoday]

            if (beercountToday > VariablesDrunklevel[str(drunklevelToday)]):
                return True
            else:
                return False
        else:
            return False