import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# تحميل متغيرات البيئة
load_dotenv()

# إعداد intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# إنشاء البوت
bot = commands.Bot(command_prefix="!", intents=intents)

# معرف القنوات
WELCOME_CHANNEL_ID = 1441901995794501714
INFO_CHANNEL_ID = 1441902361416302642

# رسالة معلومات السيرفر
server_info_message = None

# حدث تشغيل البوت
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    bot.loop.create_task(server_info_loop())  # بدء تحديث معلومات السيرفر

# تحديث معلومات السيرفر كل دقيقة
async def server_info_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await update_server_info()
        await asyncio.sleep(60)  # تحديث كل 60 ثانية

# وظيفة تحديث معلومات السيرفر
async def rename_all(ctx):
    for member in ctx.guild.members:
        if not member.bot:  # éviter les bots
            try:
                new_nick = f"si.{member.name}"
                await member.edit(nick=new_nick)
                print(f"Nickname de {member.name} changé en {new_nick}")
            except discord.Forbidden:
                print(f"Pas de permission pour {member.name}")
            except discord.HTTPException as e:
                print(f"Erreur pour {member.name}: {e}")
    await ctx.send("Tous les nicknames ont été changés !")
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
                    value=f"**{guild.member_count}** members", inline=False)

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
    embed.set_image(url="https://dl.dropboxusercontent.com/scl/fi/rzaag0vjxc5bcbcyveg7p/Design-sans-titre-3.png?rlkey=2mtrxe2yuysigg2zgwtv5dkip&e=1&st=u9sd1js8&dl=0")

    # تعديل الرسالة إذا موجودة
    if server_info_message:
        try:
            await server_info_message.edit(embed=embed)
            return
        except:
            server_info_message = None

    # إنشاء رسالة جديدة إذا لم توجد
    server_info_message = await channel.send(embed=embed)

# حدث دخول عضو جديد
@bot.event
async def on_member_join(member):
    try:
        await member.edit(nick=f"〢T.E.H・{member.name}")
    except:
        print(f"Cannot change nickname for {member.name}")
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

# تشغيل البوت
token = os.getenv("DISCORD_TOKEN")
if not token:
    print("❌ ERROR: DISCORD_TOKEN not found in environment variables")
    exit(1)

bot.run(token)





