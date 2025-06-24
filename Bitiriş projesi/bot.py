import discord
from discord.ext import commands
import os
import random
from discord import ui,ButtonStyle
from a import gen_buttons
from config import Token




intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık') 


@bot.event
async def on_interaction(interaction):
    buttons=gen_buttons()
    view=discord.ui.View()
    for button in buttons:
        view.add_item(button)
   

    if isinstance(interaction, commands.Context):
        await interaction.send("Hangi sınıftasınız", view=view)

    else:
        await interaction.followup.send("Hangi sınıftasınız", view=view)


@bot.command()
async def giriş():
    user=input("Lütfen Adınız-Soyadınız,Numaranız ve sınıfınızı giriniz:")
    print(user)

    
    


bot.run(Token)











