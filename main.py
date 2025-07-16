import disnake
from disnake.ext import commands
import os

# Ortam değişkenlerinden verileri al
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))
TRIGGER_WORD = "olympos"

intents = disnake.Intents.all()
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")

@bot.event
async def on_presence_update(before, after):
    if after.bot:
        return

    activities = after.activities
    found = False
    for activity in activities:
        name = getattr(activity, 'name', '') or ''
        state = getattr(activity, 'state', '') or ''
        details = getattr(activity, 'details', '') or ''
        full_text = f"{name} {state} {details}".lower()
        if TRIGGER_WORD in full_text:
            found = True
            break

    if found:
        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(after.id)
        role = guild.get_role(ROLE_ID)
        if role and role not in member.roles:
            await member.add_roles(role)
            print(f"{member.name} kullanıcısına rol verildi.")

@bot.command()
async def Olmypos(ctx):
    await ctx.send("🔍 Kullanıcı durumları izleniyor. Olympos yazanlara otomatik rol verilecek.")

bot.run(TOKEN)
