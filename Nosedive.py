import discord
import pandas as pd 
import numpy as np
from datetime import datetime
from discord import app_commands
import os
import random
import time

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True
intents.members = True

ratings = {}
cooldowns = {}

if os.path.exists('Nosedive/out.csv'):
    df = pd.read_csv('Nosedive/out.csv')
    for index, row in df.iterrows():
        ratings[row['Member']] = row['Rating']
else:
    df = pd.DataFrame(columns=['Member', 'Rating'])

@tree.command(name = "rate", description = "Rate a member!")
async def first_command(interaction: discord.Interaction, member: discord.User, rating: int):
    if((interaction.user.name.lower(), member.name.lower()) in cooldowns):
        if(time.time() - cooldowns[(interaction.user.name.lower(), member.name.lower())] < 3600):
            await interaction.response.send_message("You can rate this person in **" + str(3600 - int(time.time() - cooldowns[(interaction.user.name.lower(), member.name.lower())])) + "**s")
            return


    if(member.name.lower() == interaction.user.name.lower()):
        await interaction.response.send_message("**You cannot rate yourself!**")
        return

    if(member.name.lower() not in ratings):
        ratings[member.name.lower()] = 3
    if(interaction.user.name.lower() not in ratings):
        ratings[interaction.user.name.lower()] = 3
    if(rating <= 5 and rating >= 1):
        ratings[member.name.lower()] = getNewRating(ratings[member.name.lower()], ratings[interaction.user.name.lower()], rating)
        updateDataframe()
        cooldowns[(interaction.user.name.lower(), member.name.lower())] = time.time()
        await interaction.response.send_message("**" + str(interaction.user.name.capitalize()) + "** has rated **" + str(member.name.capitalize()) + "** a **" + str(rating) + "**\nTheir rating is now a **" + str(ratings[member.name.lower()])[:5] + "**")
    else:
        await interaction.response.send_message("**Invalid number of stars! (1-5)**")


@tree.command(name = "get", description = "Get a member's rating!")
async def first_command(interaction: discord.Interaction, member: discord.User):

    await interaction.response.send_message("**" + member.name.capitalize() + "** has **" + str(ratings[member.name.lower()])[:5] + " stars**")
    
@tree.command(name = "leaderboard", description = "Check the leaderboard!")
async def leaderboard(interaction: discord.Interaction):

    message = "***Leaderboard:***\n\n"
    names = [[mem, ratings[mem]] for mem in ratings]
    names.sort(key=lambda x : float(x[1]))
    names.reverse()
    for name in names:
        message += "**" + str(name[0]).capitalize() + "**: " + str(name[1])[:4] + " ⭐\n"

    await interaction.response.send_message(message)
    

def getNewRating(targetCurrent, raterRating, rating):
    c = targetCurrent
    r = rating
    i = raterRating
    m = random.random() * -0.1

    diff = (c-r)
    return (targetCurrent + (((-diff/10) + (diff * m) * i) / 2))

def updateDataframe():
    df = pd.DataFrame(columns=['Member', 'Rating'])
    for key in ratings:
        df.loc[len(df.index)] = [key, ratings[key]]
    df.to_csv('Nosedive/out.csv', index=False)




@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')
    print("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOAH")
    print("Ready!")

client.run('NICE TRY')