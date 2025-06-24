import discord
from discord.ext import commands
import os
import random
from discord import ui,ButtonStyle
from a import gen_buttons
from config import Token



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık') 

ogerenciler={}

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

#KAYIT
@bot.command()
async def kayit(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Adınızı giriniz:")
    ad = await bot.wait_for("message", check=check)

    await ctx.send("Soyadınızı giriniz:")
    soyad = await bot.wait_for("message", check=check)

    await ctx.send("Numaranızı giriniz:")
    numara = await bot.wait_for("message", check=check)

    await ctx.send("Kaçını sınıfınız:")
    sinif = await bot.wait_for("message", check=check)


    ogerenciler[ctx.author.id] = {
        "ad": ad.content,
        "soyad": soyad.content,
        "numara": numara.content,
        "sınıf": sinif.content  
    }

    await ctx.send(f"Kayıt başarıyla tamamlandı! 🎉\n**Ad:** {ad.content}\n**Soyad:** {soyad.content}\n**Numara:** {numara.content}\n**Sınıf:** {sinif.content}")

    await ctx.send(f"Lütfen ders programı zorluğunuzu seçiniz 1-10:")
    
    
    

#KAYIT KONTROL
@bot.command(name="bilgim")
async def bilgim(ctx):
    bilgi = ogerenciler.get(ctx.author.id)
    if bilgi:
        await ctx.send(f"📄 Kayıtlı Bilgileriniz:\nAd: {bilgi['ad']}\nSoyad: {bilgi['soyad']}\nNumara: {bilgi['numara']}\nSınıf: {bilgi['sınıf']}")
    else:
        await ctx.send("Henüz bir kayıt bulunamadı. `!kayıt` komutu ile kaydolabilirsin.")
    
    



bot.run(Token)






