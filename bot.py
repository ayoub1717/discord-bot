import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1441901995794501714
RULES_CHANNEL_ID = 1441902151499518062


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

    channel = bot.get_channel(RULES_CHANNEL_ID)
    if channel is None:
        print("Rules channel not found!")
        return

    embed = discord.Embed(
        title="<:94979discordrules:1448418310860570724> Server Rules | قوانين السيرفر",
        description=(
            "__**English Rules:**__\n"
            "**1. Respect Everyone**\n"
            "Treat all members with kindness. No insults, racism, sexism, or harassment.\n\n"
            
            "**2. No Spamming**\n"
            "Avoid spam messages, reactions, mentions, or unnecessary noise.\n\n"

            "**3. Stay on Topic**\n"
            "Use each channel for its purpose.\n\n"

            "**4. No NSFW Content**\n"
            "No 18+ or disturbing content.\n\n"

            "**5. No Advertising**\n"
            "Do not promote servers or products without permission.\n\n"

            "**6. Follow Discord TOS**\n"
            "All members must follow Discord Terms.\n\n"

            "**7. Keep It Friendly**\n"
            "No toxic behavior.\n\n"

            "**8. No Hacks**\n"
            "No cheats or exploits.\n\n"

            "**9. Respect Staff**\n"
            "Follow moderator instructions.\n\n"

            "__**Arabic Rules (بالعربي):**__\n"
            "**1. احترم الجميع**\n"
            ".ممنوع السب والعنصرية والتحرش.\n\n"

            "**2. ممنوع السبام**\n"
            "ممنوع تكرار الرسائل والمنشنات.\n\n"

            "**3. استخدم القنوات المناسبة**\n"
            "كل روم لغرض معيّن.\n\n"

            "**4. ممنوع المحتوى المخالف**\n"
            "محتوى +18 أو عنيف ممنوع.\n\n"

            "**5. ممنوع الإشهار**\n"
            "بدون إذن الإدارة.\n\n"

            "**6. اتبع قوانين ديسكورد**\n"
            "لازم تتبع TOS.\n\n"

            "**7. خليك محترم**\n"
            "ممنوع السمية والشجار.\n\n"

            "**8. ممنوع الغش والهكات**\n"
            "ممنوع نشر برامج غش.\n\n"

            "**9. احترام الإدارة**\n"
            "اتبع أوامر المشرفين.\n\n"
        ),
        color=0x1E90FF
    )

    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTl0dDB2ZjB6cWRoeTVqeWY5cHZvd2oyZzJ0ejR2M2FscHpqc3c1OCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/p9WGfmQMEENR9zRmCO/giphy.gif")
    embed.set_footer(text= "<:53867waringsquare:1448419679680069813>مخالفة القوانين = Ban | Breaking the rules = Ban <:53867waringsquare:1448419679680069813>")
    await channel.send(embed=embed)


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

