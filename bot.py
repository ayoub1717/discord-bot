import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1441901995794501714



@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")




@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return

    embed = discord.Embed(
        title="مرحبا بك <:4020_blurple_wave:1448294667467755631>",
        description=f"مرحبا **{member.mention}** ! نورتنا في السرفر <a:8422lightbluefireflames:1448293696117407824>",
        color=0x4169E1
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="مرحبا")

    await channel.send(embed=embed)

load_dotenv()

print("TOKEN VALUE =", os.getenv("DISCORD_TOKEN"))

token = os.getenv("DISCORD_TOKEN")
if not token:
    print("❌ ERROR: DISCORD_TOKEN not found in environment variables")
    exit(1)

bot.run(token)
