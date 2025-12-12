import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1441901995794501714
INFO_CHANNEL_ID = 1441902361416302642
TEAM_CHANEL_ID = 1441909604031140053
ADMIN_ROLE_ID = 1441912482770845849
OWNER_ROLE_ID = 1441911447159570552
DEV_ROLE_ID = 1441913119910793298
DES_ROLE_ID = 1441913392486158458

server_info_message = None
admin_info_message = None

# =========================
# SERVER INFO
# =========================
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        title=f"{member.name}'s Profile",
        color=0x1E90FF
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Username", value=str(member), inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=False)

    await ctx.send(embed=embed)


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


    if server_info_message:
        try:
            await server_info_message.edit(embed=embed)
            return
        except:
            server_info_message = None

    # إذا مش موجودة → يعمل رسالة جديدة
    server_info_message = await channel.send(embed=embed)

# =========================
# ADMINS / OWNERS / BOTS PANEL
# =========================
async def update_admins_panel():
    global admin_info_message
    channel = bot.get_channel(TEAM_CHANEL_ID)
    if channel is None:
        print("❌ SERVER INFO CHANNEL NOT FOUND")
        return

    guild = channel.guild

    embed = discord.Embed(
        title="<:14551staff:1449092416945520730>Team",
        color=0x1E90FF
    )
        
    dev_role_obj = guild.get_role(DEV_ROLE_ID)
    if dev_role_obj:
        dev_list = [member.mention for member in dev_role_obj.members]  
        dev_role = ", ".join(dev_list) if dev_list else "لا يوجد Developers"
        embed.add_field(name="<:75071developer:1449092442874839131> Developers", value=dev_role, inline=False)
    else:
        embed.add_field(name="<:75071developer:1449092442874839131> Developers", value="لا يوجد", inline=False)

    
    owners_role = guild.get_role(OWNER_ROLE_ID)
    if owners_role:
        owners_list = [member.mention for member in owners_role.members]
        owners_text = ", ".join(owners_list) if owners_list else "لا يوجد Owners"
        embed.add_field(name="<:43165owner:1449092429964902430> Owners", value=owners_text, inline=False)
    else:
        embed.add_field(name="<:43165owner:1449092429964902430> Owners", value="لا يوجد", inline=False)

    admins_role = guild.get_role(ADMIN_ROLE_ID)
    if admins_role:
        admins_list = [member.mention for member in admins_role.members]
        admins_text = ", ".join(admins_list) if admins_list else "لا يوجد Admins"
        embed.add_field(name="<:88726admin:1449092447996219599> Admins", value=admins_text, inline=False)
    else:
        embed.add_field(name="<:88726admin:1449092447996219599> Admins", value="لا يوجد", inline=False)

    bots = [member.mention for member in guild.members if member.bot]
    if bots:
        embed.add_field(name="<:68882bot:1449092440664309962> Bots", value=", ".join(bots), inline=False)
    else:
        embed.add_field(name="<:68882bot:1449092440664309962> Bots", value="لا يوجد", inline=False)

    embed.set_footer(text="Auto Updating Panel 🔄")
    embed.set_image(url="https://dl.dropboxusercontent.com/scl/fi/rzaag0vjxc5bcbcyveg7p/Design-sans-titre-3.png?rlkey=2mtrxe2yuysigg2zgwtv5dkip&e=1&st=u9sd1js8&dl=0")

    try:
        if admin_info_message:
            await admin_info_message.edit(embed=embed)
        else:
            admin_info_message = await channel.send(embed=embed)
    except:
        admin_info_message = None

# =========================
# LOOPS
# =========================
@tasks.loop(seconds=60)
async def update_server_info_loop():
    await update_server_info()

@tasks.loop(seconds=60)
async def update_admin_panel_loop():
    await update_admins_panel()

# =========================
# MEMBER JOIN EVENT
# =========================
@bot.event
async def on_member_join(member):
    # Nickname تلقائي يبدأ بـ 〢T.E.H・
    try:
        await member.edit(nick=f"〢T.E.H・{member.name}")
    except:
        print(f"Cannot change nickname for {member.name}")

    # رسالة ترحيب
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

# =========================
# ON READY
# =========================
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    update_server_info_loop.start()
    update_admin_panel_loop.start()

# =========================
# RUN BOT
# =========================
token = os.getenv("DISCORD_TOKEN")
if not token:
    print("❌ ERROR: DISCORD_TOKEN not found in environment variables")
    exit(1)

bot.run(token)







