#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json

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
Version = "0.1.1"

#---------------------------
#   Define Global Variables
#---------------------------
SettingsPath = ""
ScriptSettings = MySettings()

beerFilename = os.path.join('data', 'beerdata.json')
beerFilepath = os.path.join(os.path.dirname(__file__), beerFilename)

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join("Settings", "settings.json")
    SettingsPath = os.path.join(os.path.dirname(__file__), SettingsFile)
    ScriptSettings = MySettings(SettingsPath)
    ScriptSettings.Response = "Overwritten pong! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

    # check if beerFile is completely empty and stop if true
    if os.stat(beerFilepath).st_size == 0:
    	Parent.Log('Error', "beerFile is empty! Path:")
        Parent.Log('PathToBeerfile', beerFilepath)

    #Parent.Log(Time(time.strftime("%H:%M"), 'this is a test')
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
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
#
# ORIGINAL DEF: def Parse(parseString, userid, username, targetid, targetname, message):
#---------------------------
def Parse(parseString):
    randUser = Parent.GetRandomActiveUser()
    randUsername = Parent.GetDisplayName(randUser)

    # Randombeer command called
    if "$randomuser" in parseString:

    	AddBeerForUsername(randUsername)

    	parseString = parseString.replace("$randomuser", str(randUsername))

    # Personal beercheck command called
    if "$personalbeercount" in parseString:
        beerCount = getBeerCountForUsername(randUsername)
        parseString = parseString.replace("$personalbeercount", GetCountLocalization(beerCount))

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
#   Own Functions: ModifyBeerFile: Function for Modfiying the file which contains the beer guys and according counters
#---------------------------
def AddBeerForUsername(username):

    with open(beerFilepath, 'r') as f:
        data = json.load(f)

        if str(username.lower()) not in data:
            data[str(username.lower())] = 1
        else:
            data[str(username.lower())] += 1

    os.remove(beerFilepath)
    with open(beerFilepath, 'w') as f:
        json.dump(data, f, indent=4)

    return

#---------------------------
#   Own Functions: getBeerCountForUsername: Function for Modifying the file which contains the beer guys and according counters
#---------------------------
def getBeerCountForUsername(username):
    with open(beerFilepath, 'r') as f:
        data = json.load(f)

    if str(username.lower()) not in data:
        Parent.Log('Error', 'Oh shit, something went wrong when getting the beercount.')
    else:
        return data[str(username.lower())]


#---------------------------
#   Own Functions: GetCountLocalization: Returns "first", "second" and "third" instead of 1., 2., 3. if none are mapping, then it just outputs the given number again
#
#   returns: checked or translated number as a string
#---------------------------
def GetCountLocalization(beerCounter):
    if beerCounter > 3:
        return str(beerCounter) + "th";

    beerCounterMapping = ["first", "second", "third"]

    return str(beerCounterMapping[beerCounter - 1]);
