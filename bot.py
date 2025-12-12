import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1441901995794501714
INFO_CHANNEL_ID = 1441902361416302642



@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

async def update_server_info():
    global server_info_message

    channel = bot.get_channel(INFO_CHANNEL_ID)
    if channel is None:
        print("❌ SERVER INFO CHANNEL NOT FOUND")
        return

    guild = channel.guild

    embed = discord.Embed(
        title="📌 Server Information | معلومات السيرفر",
        color=0x1E90FF
    )

    embed.add_field(name="👥 Members | الأعضاء",
                    value=f"**{guild.member_count}** عضو", inline=False)

    embed.add_field(name="🚀 Boost Level | البوست",
                    value=f"Level **{guild.premium_tier}**", inline=False)

    embed.add_field(name="📂 Channels | القنوات",
                    value=f"Text: **{len(guild.text_channels)}**\nVoice: **{len(guild.voice_channels)}**",
                    inline=False)

    embed.add_field(name="🎭 Roles | الرتب",
                    value=f"**{len(guild.roles)}**", inline=False)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.set_footer(text="Auto Updating Panel 🔄")

    # إذا الرسالة موجودة → edit
    if server_info_message:
        try:
            await server_info_message.edit(embed=embed)
            return
        except:
            server_info_message = None

    # إذا مش موجودة → يعمل رسالة جديدة
    server_info_message = await channel.send(embed=embed)


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
