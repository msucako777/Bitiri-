import discord
from discord.ext import commands
import os
import random
from discord import ui,ButtonStyle
import a
from config import Token

zorluk=0


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
data=a.DB_Manager("Okul.db")
class But(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Kayıt",style=ButtonStyle.primary)
    async def kayit_button(self,interaction:discord.Interaction,button:ui.Button):
        await kayit_logic(interaction)

    @discord.ui.button(label="Bilgim",style=ButtonStyle.secondary)
    async def bilgim_button(self,interaction:discord.Interaction,button:ui.Button):
        await bilgim_logic(interaction)

    @discord.ui.button(label="zorluk",style=ButtonStyle.secondary)
    async def zorluk_button(self,interaction:discord.Interaction,button:ui.Button):
        await zorluk(interaction)

class KayitModal(ui.Modal, title="Kayıt Formu"):
    ad = ui.TextInput(label="Adınız", placeholder="Adınızı girin", required=True)
    soyad = ui.TextInput(label="Soyadınız", placeholder="Soyadınızı girin", required=True)
    numara = ui.TextInput(label="Numaranız", placeholder="Örn: 1234", required=True)
    sinif = ui.TextInput(label="Sınıfınız", placeholder="Örn: 10", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            ogerenciler[interaction.user.id] = {
                "ad": self.ad.value,
                "soyad": self.soyad.value,
                "numara": self.numara.value,
                "sınıf": self.sinif.value
            }
            sonuc = data.ogrencikayit(
                int(interaction.user.id),
                self.ad.value,
                self.soyad.value,
                int(self.numara.value),
                int(self.sinif.value)
            )
            await interaction.response.send_message(
                f"Kayıt tamamlandı ✅\n{sonuc}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"Hata oluştu: {e}", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık') 

ogerenciler={}

async def kayit_logic(target):
    if isinstance(target,discord.Interaction):
        modal = KayitModal()
        await target.response.send_modal(modal)
    else:
        def check(m):
            return m.author == target.author and m.channel == target.channel

        await target.send("Adınızı giriniz:")
        ad = await bot.wait_for("message", check=check)

        await target.send("Soyadınızı giriniz:")
        soyad = await bot.wait_for("message", check=check)

        await target.send("Numaranızı giriniz:")
        numara = await bot.wait_for("message", check=check)

        await target.send("Kaçını sınıfınız:")
        sinif = await bot.wait_for("message", check=check)


        ogerenciler[target.author.id] = {
            "ad": ad.content,
            "soyad": soyad.content,
            "numara": numara.content,
            "sınıf": sinif.content  
        }
        sonuc=data.ogrencikayit(int(target.author.id),ad.content,soyad.content,int(numara.content),int(sinif.content))
        await target.send((int(target.author.id),ad.content,soyad.content,int(numara.content),int(sinif.content)))
        await target.send(sonuc)



async def bilgim_logic(target):
    if isinstance(target,discord.Interaction):
        bilgi = data.get_ogrenciler(target.user.id)
        try:
            await target.response.send_message(
                f"📄 Kayıtlı Bilgileriniz:\nAd: {bilgi[0][1]}\nSoyad: {bilgi[0][2]}\nNumara: {bilgi[0][3]}\nSınıf: {bilgi[0][4]}",
                ephemeral=True  # sadece kullanıcı görsün diye
            )
        except:
            await target.response.send_message(
                "Henüz bir kayıt bulunamadı. `!kayıt` komutu ile kaydolabilirsin.",
                ephemeral=True
            )
    else:
        bilgi = data.get_ogrenciler(target.author.id)
        try:
            await target.send(f"📄 Kayıtlı Bilgileriniz:\nAd: {bilgi[0][1]}\nSoyad: {bilgi[0][2]}\nNumara: {bilgi[0][3]}\nSınıf: {bilgi[0][4]}")
        except:
            await target.send(bilgi)
            await target.send("Henüz bir kayıt bulunamadı. `!kayıt` komutu ile kaydolabilirsin.")

async def Zorluk(interaction):
    def check(m):
        return m.author.id == interaction.user.id and m.channel == interaction.channel

    await interaction.response.send_message("Lütfen ders programı zorluğunuzu seçiniz 1-10:")


    cevap = await bot.wait_for("message", check=check)

    try:
        zorluk_seviyesi = int(cevap.content)
    except ValueError:
        await interaction.followup.send("Geçerli bir sayı girmelisin (1-10)!")
        return

    ders_programlari = {
        1:{"tarih":1,"fizik":1,},
        2:{"mat":1,"tarih":1,"coğrafya":1,},
        3:{"mat":1,"fizik":1,"biyoloji":1,},
        4:{"mat":1,"fizik":1,"edebiyat":1,"ing":1},
        5:{"mat":2,"fizik":1,"kimya":1,"edebiyat":0.5,},
        6:{"mat":2,"fizik":1,"biyoloji":2,"ing":0.5},
        7:{"mat":3,"fizik":1,"kimya":1,},
        8:{"mat":3,"fizik":1,"kimya":1,"biyoloji":0.5,},
        9:{"mat":3,"fizik":1,"kimya":1,"biyoloji":0.5,"coğrafya":0.5,},
        10:{"mat":3,"tarih":1,"fizik":1,"kimya":1,"biyoloji":1,"ing":1}
        }
    


    program = ders_programlari.get(zorluk_seviyesi, "Belirttiğiniz seviyeye özel bir program bulunamadı.")

    await interaction.followup.send(f"Seçtiğiniz zorluk seviyesi {zorluk_seviyesi}. Ders programınız:\n{program}")





#KAYIT
@bot.command()
async def kayit(ctx):
    await kayit_logic(ctx)


#KAYIT KONTROL
@bot.command(name="bilgim")
async def bilgim(ctx):
    await bilgim_logic(ctx)

@bot.command(name="komutlar")
async def komutlar(ctx):
    a=But()
    await ctx.send("selam",view=a)


bot.run(Token)


