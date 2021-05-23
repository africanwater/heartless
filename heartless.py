import discord
from discord.ext import commands
import pymongo
import datetime
import os
import logging
import time
import json
from dotenv import load_dotenv
import random
load_dotenv()
import asyncio
import requests
import io
import aiohttp
import typing
from PIL import Image
from discord.ext.commands import clean_content
from time import sleep
from random import randint
import sys
import sqlite3
import traceback
import re
from discord import user
import math
from discord.ext.commands import BucketType
from discord.ext.commands import cooldown
from cogs.afk import AFK
from discord.ext.commands import Context, command
from discord import user
from discord import Member
intents = discord.Intents.default()
intents = intents
import discord,asyncio,random,youtube_dl,string,os
from discord.ext import commands
from googleapiclient.discovery import build
from discord.ext.commands import command
from cogs.music import Music
import ffmpeg
import collection



from cogs.AntiChannel import AntiChannel
from cogs.AntiRemoval import AntiRemoval
from cogs.AntiPermissions import AntiPermissions
from cogs.AntiWebhook import AntiWebhook

mongoClient = pymongo.MongoClient(os.environ["MONGO_DB_URL"].replace("<password>", os.environ["MONGO_DB_PASSWORD"]))
db = mongoClient.get_database("botdb").get_collection("whitelists")

webhook = discord.Webhook.partial(
    os.environ["WEBHOOK_ID"],
    os.environ["WEBHOOK_TOKEN"],
    adapter=discord.RequestsWebhookAdapter(),
)

LASTFM_APPID = os.environ.get("LASTFM_APIKEY")
LASTFM_TOKEN = os.environ.get("LASTFM_SECRET")
GOOGLE_API_KEY = os.environ.get("GOOGLE_KEY")
AUDDIO_TOKEN = os.environ.get("AUDDIO_TOKEN")



intents = discord.Intents.default()
intents.members = True
client = commands.Bot(description="", command_prefix=">", case_insensitive=True, intents=intents)
client.add_cog(AntiChannel(client, db, webhook))
client.add_cog(AntiRemoval(client, db, webhook))
client.add_cog(AntiPermissions(client, db, webhook))
client.add_cog(AntiWebhook(client, db, webhook))
client.add_cog(AFK(client))
client.add_cog(Music(client))
client.remove_command('help')



def is_owner(ctx):
    return ctx.message.author.id == 694624137901113365, 746859176256340010

def is_whitelisted(ctx):
    return ctx.message.author.id in db.find_one({ "guild_id": ctx.guild.id })["users"] or ctx.message.author.id == 694624137901113365, 746859176256340010
    
def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 694624137901113365, 746859176256340010



@client.event
async def on_member_join(member):
    whitelistedUsers = db.find_one({ "guild_id": member.guild.id })["users"]
    if member.bot:
        async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await member.ban()
            await i.user.ban()

@client.event
async def on_ready():
    for i in client.guilds:
            if not db.find_one({ "guild_id": i.id }):
                db.insert_one({
                    "users": [],
                    "guild_id": i.id
                })
                
    webhook.send(embed=discord.Embed(description=f" is online | loaded {len(client.guilds)} whitelists"))

    print("bot: {0} ".format(client.user))
    await client.change_presence(activity= discord.Streaming(name = "Prefix >", url = "https://twitch.tv/monstercat"))

@client.event
async def on_guild_join(guild):
    db.insert_one({
        "users": [guild.owner_id],
        "guild_id": guild.id
    })

    webhook.send(embed=discord.Embed(description=f"Joined {guild.name} - {guild.member_count} members"))

@client.event
async def on_guild_leave(guild):
    db.delete_one({ "guild_id": guild.id })

    webhook.send(embed=discord.Embed(description=f"Left {guild.name} - {guild.member_count} members"))
           

@client.command(aliases=["wl"])
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user")
        return

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user.")
        return

    if user.id in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        await ctx.send("That user is already in the whitelist.")
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$push": { "users": user.id }})

    await ctx.send(f"{user} has been added to the whitelist successfully.")

@client.command(aliases=["dwl"])
@commands.check(is_server_owner)
async def dewhitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user.")

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user.")

    if user.id not in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        await ctx.send("That user is not in the whitelist.")
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$pull": { "users": user.id }})

    await ctx.send(f"{user} has been removed from the whitelist successfully.")

@client.command()
@commands.check(is_whitelisted)
async def massunban(ctx):
    async for i in ctx.guild.bans():
        print(i)

@client.command(aliases=["wld"])
@commands.check(is_whitelisted)
async def whitelisted(ctx):
    data = db.find_one({ "guild_id": ctx.guild.id })['users']

    embed = discord.Embed(title=f"Whitelist for {ctx.guild.name}", description="")

    for i in data:
        embed.description += f"{client.get_user(i)} - {i}\n"

    await ctx.send(embed=embed)

    




@client.event
async def on_guild_join(guild):
    db.insert_one({
        "users": [guild.owner_id],
        "guild_id": guild.id
    })
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(color=(0x36393F))
            embed.set_author(name=f"Stranded", icon_url='https://cdn.discordapp.com/attachments/750807114020159579/784469613319553024/image0.jpg')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/750807114020159579/784469613319553024/image0.jpg')
            embed.set_footer(text=f"{guild.name}")
            embed.title="Thank you for adding me!"
            embed.description = "**Protection Stranded Serves**\nStranded is one of the best anti nukes and protecters on discord, below are my defences against nukers and people who want to do harm to your server!\n\nalthough this isn't all my main defences there are many more, by doing >help\nuser removals\nuser unbans\nchannel creations\nchannel deletions\nrole creations\nrole deletions\nguild settings changes"
            await channel.send(embed=embed)
        break
    webhook.send(embed=discord.Embed(description=f"Joined {guild.name} - {guild.member_count} members"))





@client.command(name="clear", aliases=["c"])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f" {ctx.author}  ***cleared***  {amount}  ***messages in***  {ctx.message.channel} ", delete_after=5)


@client.command(pass_context=True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    embed=discord.Embed(title=None, description='Ping : {}'.format(round((t2-t1)*1000)), color=0x2f3136)
    await channel.send(embed=embed)
client.command(pass_context=True)


@client.command(aliases=["userinfo"])
async def userinf(ctx, *, member: discord.Member):
    embed=discord.Embed(
        color=discord.Color.from_rgb(000, 000, 00)
    )
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/%7Bmember.id%7D/%7Bmember.avatar%7D.png?size=128%22%22")
    embed.add_field(name="Name:", value=member.name, inline=True)
    embed.add_field(name="tag:", value=f"#{member.discriminator}", inline=True)
    embed.add_field(name="ID:", value=member.id, inline=True)
    embed.add_field(name="Created:", value=member.created_at.strftime("%B %d %Y,\n%H:%M:%S %p"), inline=True)
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%B %d %Y,\n%H:%M:%S %p"), inline=True)
    embed.add_field(name="Highest Role:", value=member.top_role, inline=True)
    await ctx.send(embed=embed)

@client.command(aliases=['servericon'])
async def guildicon(ctx): # b'\xfc'
    em = discord.Embed(title=ctx.guild.name)
    em.set_image(url=ctx.guild.icon_url)
    await ctx.send(embed=em)

@client.command()
async def kiss(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} kisses {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def hug(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/hug")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} hugs {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def slap(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/slap")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} slaps {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def pat(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} pats {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def smug(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/smug")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} gives a smug smile to {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def tickle(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/tickle")
    res = r.json()
    em = discord.Embed(
         timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} tickles {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def pet(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} pets {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)

@client.command()
async def feed(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/feed")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} feeds {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)


@client.command()
async def serverinfo(ctx):
      embed = discord.Embed(
      color=0x2f3136,
      timestamp=datetime.datetime.utcnow(),
      )
      embed.add_field(name='Owner', value=f"{ctx.guild.owner}", inline=False)
      embed.add_field(name='Region', value=f"{ctx.guild.region}", inline=False)
      embed.add_field(name='Member Count', value=f"{ctx.guild.member_count}", inline=False)
      embed.add_field(name='Creation Date', value=f"{ctx.guild.created_at.strftime('%d %b %Y %H:%M')}", inline=False)
      embed.add_field(name='Roles', value="{}".format(len(ctx.guild.roles)-1),     inline=False)
      embed.add_field(name='Text Channels', value="{}".format(len(ctx.guild.text_channels)),     inline=True)
      embed.add_field(name='Voice Channels', value="{}".format(len(ctx.guild.voice_channels)),     inline=True)
      if ctx.guild.system_channel:
          embed.add_field(name='Standard Channel', value=f'#{ctx.guild.system_channel}', inline=False)
      embed.add_field(name='AFK Voice Timeout', value=f'{int(ctx.guild.afk_timeout / 60)} minutes', inline=True)
      embed.add_field(name='AFK Channel', value=f'#{ctx.guild.afk_channel}', inline=True)
      embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
      embed.set_thumbnail(url=ctx.guild.icon_url)
      embed.set_footer(text=f'ID: {ctx.guild.id}')
      await ctx.send(embed=embed)


snipes = dict()

def snipe_embed(context_channel, message, user):
    if message.author not in message.guild.members or message.author.color == discord.Colour.default():
        embed = discord.Embed(description = message.content, timestamp = message.created_at)
    else:
        embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
    embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
    if message.attachments:
        embed.add_field(name = 'Attachment(s)', value = '\n'.join([attachment.filename for attachment in message.attachments]) + '\n\nAttachment URLs are invalidated once the message is deleted.')
    if message.channel != context_channel:
        embed.set_footer(text = 'Sniped By: ' + str(user) + ' | in channel: #' + message.channel.name)
    else:
        embed.set_footer(text = 'Sniped By: ' + str(user))
    return embed


@client.event
async def on_message_delete(message):
        if message.guild and not message.author.bot:
            try:
                snipes[message.guild.id][message.channel.id] = message
            except KeyError:
                snipes[message.guild.id] = {message.channel.id: message}

@client.command()
async def snipe(ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        try:
            sniped_message = snipes[ctx.guild.id][channel.id]
        except KeyError:
            await ctx.send(embed=discord.Embed(description=f":Error: No messages to be sniped! {ctx.author.mention}", colour=0xf04947), delete_after=7)
        else:
            await ctx.send(embed = snipe_embed(ctx.channel, sniped_message, ctx.author))

@client.command(aliases=['ri'])
async def roleinfo(ctx, *, role: discord.Role):
      guild = ctx.guild
      since_created = (ctx.message.created_at - role.created_at).days
      role_created = role.created_at.strftime("%d %b %Y %H:%M")
      created_on = "{} ({} days ago)".format(role_created, since_created)
      users = len([x for x in guild.members if role in x.roles])
      if str(role.colour) == "#2f31360":
          colour = "#2f31360"
          color = ("#%06x" % random.randint(0, 0xFFFFFF))
          color = int(colour[1:], 16)
      else:
          colour = str(role.colour).upper()
          color = role.colour
      embed = discord.Embed(
          colour=color,
          timestamp=datetime.datetime.utcnow(),
      )
      embed.add_field(name='Role Name', value=f"{role.name}", inline=False)
      embed.add_field(name='Role ID', value=f"{role.id}", inline=False)
      embed.add_field(name="Users", value=f"{users}", inline=False)
      embed.add_field(name="Mentionable", value=f"{role.mentionable}", inline=True)
      embed.add_field(name="Hoisted", value=f"{role.hoist}", inline=True)
      embed.add_field(name="Position", value=f"{role.position}", inline=False)
      embed.add_field(name="Managed", value=f"{role.managed}", inline=True)
      embed.add_field(name="Colour", value=f"{colour}", inline=True)
      embed.add_field(name='Creation Date', value=f"{created_on}", inline=False)
      embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
      embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
      embed.set_footer(text=f"Role ID: {role.id}")
      await ctx.send(embed=embed)

@client.command()
async def banner(ctx, *, guild=None):
        """gets a guild's banner image
        Parameters
        • guild - the name or id of the guild
        """
        if guild is None:
            guild = ctx.guild
        elif type(guild) == int:
            guild = discord.utils.get(ctx.bot.guilds, id=guild)
        elif type(guild) == str:
            guild = discord.utils.get(ctx.bot.guilds, name=guild)
        banner = await guild.banner_url_as(format="png").read()
        with io.BytesIO(banner) as f:
            await ctx.send(file=discord.File(f, "banner.png"))            


@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.Member, *, reason = None):
 if not user:
    await ctx.send("Please mention a user to ban.")
 else:
    embed = discord.Embed(color=(0x36393F))
    embed.title=("Success")
    embed.description=f"{user.mention} was banned."  
    embed.set_footer(text=f"{reason}")
    await user.ban(reason = reason)
    await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to ban.")
    if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permissons to use this command.")
    if isinstance(error, (commands.BadArgument)):     
        await ctx.send("user was not found.")      

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.Member, *, reason = None):  
    embed = discord.Embed(color=(0x36393F))
    embed.title=("Success")
    embed.description=f"{user.mention} was kicked."  
    embed.set_footer(text=f"{reason}")
    await user.kick(reason = reason)
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to kick.")
    if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permissons to run this command.")

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, user=None):

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Error: user could not be found!")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            await ctx.send("User not banned!")
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("Unbanning failed!")
        return

    await ctx.send(f"Successfully unbanned {user.mention}!")

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member=None):
      if not member:
          await ctx.send("You forgot to mention a user dumbass!")
          return
      role = discord.utils.get(ctx.guild.roles, name="mute")
      await member.add_roles(role)
      await ctx.send(f"{member.name}#{member.discriminator} was muted by {ctx.author}.")
@mute.error
async def mute_error(ctx, error):
      if isinstance(error, commands.CheckFailure):
          await ctx.send("**You are not allowed to mute people**")

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member=None):
      if not member:
          await ctx.send("You forgot to mention a user dumbass!")
          return
      role = discord.utils.get(ctx.guild.roles, name="mute")
      await member.remove_roles(role)
      await ctx.send(f"{member.name}#{member.discriminator} was unmuted by {ctx.author}.")
@unmute.error
async def unmute_error(ctx, error):
      if isinstance(error, commands.CheckFailure):
          await ctx.send("**You are not allowed to unmute people**")

@client.command(name="invitebackground", aliases=["invback"])
async def invitebackround(ctx, *, guild=None):
        """gets a guild's invite splash(invite background)
        Parameters
        • guild - the name or id of the guild
        """
        if guild is None:
            guild = ctx.guild
        elif discord.utils.get(ctx.bot.guilds, id=int(guild)) is not None:
            guild = discord.utils.get(ctx.bot.guilds, id=int(guild))
        elif type(guild) == str:
            guild = discord.utils.get(ctx.bot.guilds, name=guild)
        splash = await guild.splash_url_as(format="png").read()
        with io.BytesIO(splash) as f:
            await ctx.send(file=discord.File(f, "splash.png"))

@client.command(aliases=["nickname"])
@commands.has_permissions(administrator=True)
async def nick(ctx, user: discord.Member, *, nickname: str = None):
        """change a user's nickname
        Parameter
        • user - the name or id of the user
        • nickname - the nickname to change to
        """
        prevnick = user.nick or user.name
        await user.edit(nick=nickname)
        newnick = nickname or user.name
        await ctx.send(f"Changed {prevnick}'s nickname to {newnick}")


@client.command(name="botbc", aliases=["bc"])
async def botbc(ctx, messages_to_delete: int = 15):
        """deletes messages sent by bots
        Parameters
        • messages_to_delete - number of messages to delete
        """
        deleted = 0
        async for m in ctx.channel.history(limit=200):
            if m.author.bot:
                await m.delete()
                deleted += 1
                if deleted == messages_to_delete:
                    break
        await ctx.message.delete()

@client.command(aliases=["ar"])
@commands.check(is_server_owner)
async def addrole(ctx, member: discord.Member, *, role: discord.Role):
        """Add a role to someone else
        Parameter
        • member - the name or id of the member
        • role - the name or id of the role"""
        if not role:
            return await ctx.send("That role does not exist.")
        await member.add_roles(role)
        await ctx.send(f"Added:  {role.name} ")
        
@client.command(aliases=["rr"])
@commands.check(is_server_owner)
async def removerole(ctx, member: discord.Member, *, role: discord.Role):
        """Remove a role from someone else
        Parameter
        • member - the name or id of the member
        • role - the name or id of the role"""
        await member.remove_roles(role)
        await ctx.send(f"Removed:  {role.name} ")

def RColor(): 
    randcolor = discord.Color(random.randint(0x2f31360, 0xFFFFFF))
    return randcolor

@client.command(aliases=["ibc"])
@commands.has_permissions(manage_messages=True)
async def imagebc(ctx, images_to_delete: int = 10):
        """deletes messages containing images
        Parameters
        • images_to_delete - number of images to delete
        """
        deleted = 0
        async for m in ctx.channel.history(limit=200):
            if m.attachments:
                await m.delete()
                deleted += 1
                if images_to_delete == deleted:
                    break
        await ctx.message.delete()

@client.command(aliases=['8ball'])
async def eightball(ctx, *, _ballInput: clean_content):
        """extra generic just the way you like it"""
        choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = random.choice(["It is certain ", 
                                        "It is decidedly so ", 
                                        "Without a doubt lol ", 
                                        "Yes, definitely ", 
                                        "You may rely on it ", 
                                        "As I see it, yes ",
                                        "Most likely ", 
                                        "Outlook good ", 
                                        "Yes ", 
                                        "Signs point to yes "]) + ":8ball:"

            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x2f31360, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = random.choice(["Reply hazy try again ", 
                                        "Ask again later ", 
                                        "Better not tell you now ", 
                                        "Cannot predict now ", 
                                        "Concentrate and ask again "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x2f31360, description=prediction))
        elif choiceType == "(Negative)":
            prediction = random.choice(["Don't count on it ", 
                                        "My reply is no ", 
                                        "My sources say no ", 
                                        "Outlook not so good ", 
                                        "Very doubtful "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x2f31360, description=prediction))
        emb.set_author(name='8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await ctx.send(embed=emb)

@client.command()
async def couple(ctx, user: discord.Member, number=100):
      '''
      Rates A Relationship In The Server
      '''
      if user is None:
          user = ctx.author
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Couple", 
          description=f"{ctx.author.mention} and {user.mention}'s Relationship has a...", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
     
      await ctx.send(embed=embed)
      sleep(1)
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Couple", 
          description=f" {randint(1, number)}%  Chance of Succeeding!", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")

      await ctx.send(embed=embed)
  
@client.command()
async def loyal(ctx, user: discord.Member = None, number=100):
      '''
      Rates A Loyalty In The Server
      '''
      if user is None:
          user = ctx.author
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Loyalty", 
          description=f"Ooou **{user}** saying they loyal...", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
          
      await ctx.send(embed=embed)
      sleep(1)
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Loyalty", 
          description=f"Turns Out They're  {randint(1, number)}%  Loyal!", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
          
      await ctx.send(embed=embed)
  
@client.command()
async def cute(ctx, user: discord.Member = None, number=100):
      '''
      Rates A Cutie In The Server
      '''
      if user is None:
          user = ctx.author
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Cuteness", 
          description=f"UwU, how cute is **{user}**? :thinking:", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
          
      await ctx.send(embed=embed)
      sleep(1)
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Cuteness", 
          description=f"They are  {randint(1, number)}%  cute! :flushed:", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
          
      await ctx.send(embed=embed)

@client.command()
async def coinflip(ctx):
      """ Flips A Coin """
      coin = [
          " Heads ",
          " Tails ",
          ]
      await ctx.send(f" {ctx.author}  has flipped a coin... lets see what they're gonna get!")
      sleep(1)
      await ctx.send(random.choice(coin))

@client.command()
async def dick(ctx, user: discord.Member = None):
      if user is None:
          user = ctx.author
      size = random.randint(1, 15)
      dong = ""
      for _i in range(0, size):
          dong += "="
      em = discord.Embed(title=f"**{user}'s** Dick size", description=f"8{dong}D", color= discord.Color(random.randint(0x2f3136, 0x2f3136)))
      await ctx.send(embed=em)



@client.command()
async def combine(ctx, name1: clean_content, name2: clean_content):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = (discord.Embed(color=0x2f3136, description = f"{ship}"))
        emb.set_author(name=f"{name1} + {name2}", icon_url='https://i1.sndcdn.com/artworks-000671702488-7zmfaw-t500x500.jpg')
        await ctx.send(embed=emb)

@client.command()
async def invite(ctx):
    embed = discord.Embed(
      description=f"[Click This Link To Add Stranded To Your Server!](https://discord.com/oauth2/authorize?client_id=793750521587564554&permissions=8&scope=bot)", 
      timestamp=datetime.datetime.utcnow(), 
      colour=0x2f3136
    )
    embed.add_field(name="Requested By", value="{}".format(ctx.author.mention), inline=True)
    embed.set_author(name=f"Stranded Invite Requested!", icon_url=ctx.guild.icon_url)
    embed.set_footer(text=f"{ctx.guild.name}")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@client.command()
async def ship(ctx, name1 : clean_content, name2 : clean_content):
        shipnumber = random.randint(0,100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(", 
                                                            'Just "friends"', 
                                                            '"Friends"', 
                                                            "Little to no love ;(", 
                                                            "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone", 
                                                     "Still in that friendzone ;(", 
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!", 
                                                     "But there's a small bit of love somewhere", 
                                                     "I sense a small bit of love!", 
                                                     "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!", 
                                                      "There is a bit of love there...", 
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", 
                                                          "It appears one sided!", 
                                                          "There's some potential!", 
                                                          "I sense a bit of potential!", 
                                                          "There's a bit of romance going on here!", 
                                                          "I feel like there's some romance progressing!", 
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!", 
                                                      "There's some love in the air!", 
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!", 
                                                       "I can see the love is there! Somewhere...", 
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(random.choice(["Love is in the air!", 
                                                              "I can definitely feel the love", 
                                                              "I feel the love! There's a sign of a match!", 
                                                              "There's a sign of a match!", 
                                                              "I sense a match!", 
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!", 
                                                           "There's a match made in heaven!", 
                                                           "It's definitely a match!", 
                                                           "Love is truely in the air!", 
                                                           "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0x2f31360
        elif 33 < shipnumber < 66:
            shipColor = 0x2f31360
        else:
            shipColor = 0x2f31360

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                        ":sparkling_heart:", 
                                                                                                        ":heart_decoration:", 
                                                                                                        ":heart_exclamation:", 
                                                                                                        ":heartbeat:", 
                                                                                                        ":heartpulse:", 
                                                                                                        ":hearts:", 
                                                                                                        ":blue_heart:", 
                                                                                                        ":green_heart:", 
                                                                                                        ":purple_heart:", 
                                                                                                        ":revolving_hearts:", 
                                                                                                        ":yellow_heart:", 
                                                                                                        ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="shipping", icon_url="https://pbs.twimg.com/profile_images/1187024252362481665/d3k6IdPk.jpg")
        await ctx.send(embed=emb)

@client.command()
async def uptime(ctx):
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]
    await ctx.send(f"Current Uptime: "+''+uptime+'')

start_time = datetime.datetime.utcnow()


@client.command()
async def info(ctx):
    servers = ctx.bot.guilds
    guilds = len(ctx.bot.guilds)
    servers.sort(key=lambda x: x.member_count, reverse=True)
    y = 0
    for x in ctx.bot.guilds:
        y += x.member_count
    embed = discord.Embed(
      description=f"[Click To Add Stranded To Your Server!](https://discord.com/oauth2/authorize?client_id=793750521587564554&permissions=8&scope=bot)", 
      timestamp=datetime.datetime.utcnow(), 
      colour=0x2f3136
    )
    embed.set_author(name=f"Stranded info.", icon_url=ctx.bot.user.avatar_url)
    embed.add_field(name="**Gen Info.**", value=f" Current Users  — {y}\n Current Guilds  — {guilds}\n Created Date  — 11/08/2020\n Creators  —<@746859176256340010>", inline=False)
    embed.set_footer(text=f"{ctx.guild.name}")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.send(embed=embed)


role_mention = re.compile("<@&(\d+)>")
regex_id = re.compile("(^\d+$)")

def get_role(ctx, role):
    if role_mention.match(role):
        role = ctx.guild.get_role(int(role_mention.match(role).group(1)))
    elif regex_id.match(role):
        role = ctx.guild.get_role(int(regex_id.match(role).group(1)))
    else:
        try:
            role = list(filter(lambda x: x.name.lower() == role.lower(), ctx.guild.roles))[0]
        except IndexError:
            try:
                role = list(filter(lambda x: x.name.lower().startswith(role.lower()), ctx.guild.roles))[0]
            except IndexError:
                try:
                    role = list(filter(lambda x: role.lower() in x.name.lower(), ctx.guild.roles))[0]
                except IndexError:
                    return None
    return role



@client.command(name="cinfo", aliases=["ci"])
async def channelinfo(ctx, *, channel_or_category: str=None):
        if not channel_or_category:
            channel = ctx.channel
        else:
            channel = arg.get_voice_channel(ctx, channel_or_category)
        if not channel:
            channel = arg.get_text_channel(ctx, channel_or_category)
        if not channel:
            channel = arg.get_category(ctx, channel_or_category)
        if not channel:
            return await ctx.send("Invalid channel/category :trident:")
        perms = "\n".join(list(map(lambda x: x[0].replace("_", " ").title(), filter(lambda x: x[1] == True, channel.permissions_for(ctx.author)))))
        if isinstance(channel, discord.TextChannel):
            s=discord.Embed(colour=0x2f3136, description=ctx.channel.topic)
            s.set_author(name=channel.name, icon_url=ctx.guild.icon_url)
            s.set_thumbnail(url=ctx.guild.icon_url)
            s.add_field(name="ID", value=channel.id)
            s.add_field(name="NSFW Channel", value="Yes" if channel.is_nsfw() else "No")
            s.add_field(name="Channel Position", value=channel.position + 1)
            s.add_field(name="Slowmode", value="{} {}".format(channel.slowmode_delay, "second" if channel.slowmode_delay == 1 else "seconds") if channel.slowmode_delay != 0 else "Disabled")
            s.add_field(name="Channel Category", value=channel.category.name if channel.category else "None")
            s.add_field(name="Members", value=len(channel.members))
            s.add_field(name="Author Permissions", value=perms if perms else "None", inline=False)
        elif isinstance(channel, discord.VoiceChannel):
            s=discord.Embed(colour=0x2f3136, description=ctx.channel.topic)
            s.set_author(name=channel.name, icon_url=ctx.guild.icon_url)
            s.set_thumbnail(url=ctx.guild.icon_url)
            s.add_field(name="ID", value=channel.id)
            s.add_field(name="Channel Position", value=channel.position + 1)
            s.add_field(name="Channel Category", value=channel.category.name if channel.category else "None")
            s.add_field(name="Members Inside", value=len(channel.members))
            s.add_field(name="User Limit", value="Unlimited" if channel.user_limit == 0 else channel.user_limit)
            s.add_field(name="Bitrate", value="{} kbps".format(round(channel.bitrate/1000)))
            s.add_field(name="Author Permissions", value=perms if perms else "None", inline=False)
        elif isinstance(channel, discord.CategoryChannel):
            channels = "\n".join(map(lambda x: x.mention if isinstance(x, discord.TextChannel) else x.name, channel.channels))
            s=discord.Embed(colour=0x2f3136, description=ctx.channel.topic)
            s.set_author(name=channel.name, icon_url=ctx.guild.icon_url)
            s.set_thumbnail(url=ctx.guild.icon_url)
            s.add_field(name="ID", value=channel.id)
            s.add_field(name="NSFW Category", value="Yes" if channel.is_nsfw() else "No")
            s.add_field(name="Category Position", value=channel.position + 1, inline=False)
            s.add_field(name="Author Permissions", value=perms if perms else "None", inline=True)
            s.add_field(name="Channels", value=channels if channels else "None", inline=True)
        await ctx.send(embed=s)

@client.command(name="invites")
async def _invites(ctx, *, user: str=None):
        """View how many invites you have or a user has"""
        if not user:
            user = ctx.author
        else:
            user = await arg.get_member(ctx, user)
            if not user:
                return await ctx.send("I could not find that user :trident:")
        amount = 0
        total = 0
        entries = {}
        for x in await ctx.guild.invites():
            if user == x.inviter:
                amount += x.uses
            total += x.uses
        for x in await ctx.guild.invites():
            if x.uses > 0:
                if "user" not in entries:
                    entries["user"] = {}
                if str(x.inviter.id) not in entries["user"]:
                    entries["user"][str(x.inviter.id)] = {}
                if "uses" not in entries["user"][str(x.inviter.id)]:
                    entries["user"][str(x.inviter.id)]["uses"] = 0
                entries["user"][str(x.inviter.id)]["uses"] += x.uses
        try: 
            entries["user"]
        except:
            return await ctx.send("No-one has made an invite in this server :trident:")
        if str(user.id) not in entries["user"]:
            await ctx.send("{} has no invites :trident:".format(user))
            return
        sorted_invites = sorted(entries["user"].items(), key=lambda x: x[1]["uses"], reverse=True)
        place = 0
        percent = (amount/total)*100
        if percent < 1:
            percent = "<1"
        else:
            percent = round(percent)
        for x in sorted_invites:
            place += 1
            if x[0] == str(user.id):
                break 
        await ctx.send("{} has **{}** invites which means they have the **{}** most invites. They have invited **{}%** of all users.".format(user, amount, ctx.prefixfy(place), percent))
        del entries

@client.command(aliases=["lbinvites", "lbi", "ilb"])
async def inviteslb(ctx, page: int=None):
        """View a leaderboard sorted by the users with the most invites"""
        if not page:
            page = 1
        entries, total = {}, 0
        for x in await ctx.guild.invites():
            if x.uses > 0:
                if "user" not in entries:
                    entries["user"] = {}
                if str(x.inviter.id) not in entries["user"]:
                    entries["user"][str(x.inviter.id)] = {}
                if "uses" not in entries["user"][str(x.inviter.id)]:
                    entries["user"][str(x.inviter.id)]["uses"] = 0
                entries["user"][str(x.inviter.id)]["uses"] += x.uses
                total += x.uses
        try: 
            entries["user"]
        except:
            return await ctx.send("No-one has made an invite in this server :trident:")
        if page < 1 or page > math.ceil(len(entries["user"])/10):
            return await ctx.send("Invalid Page :trident:")
        sorted_invites = sorted(entries["user"].items(), key=lambda x: x[1]["uses"], reverse=True)
        msg, i = "", page*10-10
        try:
            place = list(map(lambda x: x[0], sorted_invites)).index(str(ctx.author.id)) + 1
        except:
            place = None
        for x in sorted_invites[page*10-10:page*10]:
            i += 1
            percent = (x[1]["uses"]/total)*100
            if percent < 1:
                percent = "<1"
            else:
                percent = round(percent)
            user = ctx.guild.get_member(int(x[0]))
            if not user:
                user = x[0]
            msg += "{}.  {}  - {:,} {} ({}%)\n".format(i, user, x[1]["uses"], "invite" if x[1]["uses"] == 1 else "invites", percent)
        s=discord.Embed(title="Invites Leaderboard", description=msg, colour=0x2f3136)
        s.set_footer(text="{}'s Rank: {} | Page {}/{}".format(ctx.author.name, "#{}".format(place) if place else "Unranked", page, math.ceil(len(entries["user"])/10)), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=s)



@client.command()
async def horny(ctx, user: discord.Member = None, number=100):
      '''
      Rates A Cutie In The Server
      '''
      if user is None:
          user = ctx.author
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="horny", 
          description=f"ouu, how horny is **{user}**? :thinking:", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
          
      await ctx.send(embed=embed)
      sleep(1)
      embed=discord.Embed(
          colour=0x2f3136,
          timestamp=datetime.datetime.utcnow(),
          title="Horniness", 
          description=f"They are  {randint(1, number)}%  horny! :flushed:", color=0x2f3136)
      embed.set_footer(text=f"{ctx.guild.name}")
          
      await ctx.send(embed=embed)


@client.command()
async def spank(ctx, user: discord.Member): # b'\xfc'
    r = requests.get("https://nekos.life/api/v2/img/spank")
    res = r.json()
    em = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        description=f"{ctx.author.mention} spanks {user.mention}")
    em.set_image(url=res['url'])
    em.set_footer(text=f"{ctx.guild.name}")
    await ctx.send(embed=em)


@client.command(description="Set the guild banner image")
async def setbanner(ctx, url: str):
    """Set the guild banner image."""
    if ctx.message.guild is None:
        return

    permissions = ctx.message.author.permissions_in(ctx.channel)
    if not permissions.administrator:
        print("user is not admin")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file sir.')
            data = io.BytesIO(await resp.read())
            await ctx.message.guild.edit(banner=data.read())
            ctx.send("Banner set")
            await ctx.send(embed=em)


@client.command(description="Set the guild icon")
async def seticon(ctx, url: str):
    """Set the guild icon."""
    if ctx.message.guild is None:
        return

    permissions = ctx.message.author.permissions_in(ctx.channel)
    if not permissions.administrator:
        print("user is not admin")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file.')
            data = io.BytesIO(await resp.read())
            await ctx.message.guild.edit(icon=data.read())
            await ctx.send("Icon set.")
            await ctx.send(embed=em)

@client.command()
@commands.has_permissions(administrator=True)
async def servername(ctx, * , name):
        if ctx.author != ctx.guild.owner:
            await ctx.send('you are not the owner of this server.')
            return
        await ctx.guild.edit(name=name)
        em = discord.Embed(description = f'successfully changed server name to  {name} .', color = discord.Color.from_rgb(000,000,000))
        await ctx.send(embed=em)


@client.command()
@commands.has_permissions(manage_guild=True)
@cooldown(2, 6, BucketType.member)
async def massunbans(ctx, *, reason=None): 
        if ctx.message.guild == None:
            pass
        else:          
            banlist = await ctx.guild.bans()          
            i = discord.Embed(description=' Mass unban Process starting ', color = discord.Colour.from_rgb(112, 226, 255))
            await ctx.send(embed=i)            
            for users in banlist:
                try:
                    await ctx.guild.unban(user=users.user)
                except:
                    pass      
            members = [str(f'{users.user} - {users.user.id}') for users in banlist]
            if len(members) == 0:
                await ctx.send(' There are no banned users! ')
                return
            per_page = 10 
            pages = math.ceil(len(members) / per_page)
            cur_page = 1
            chunk = members[:per_page]
            linebreak = "\n"
            
            em = discord.Embed(title=f"{len(members)} Users unbanned:", description=f"{linebreak.join(chunk)}", color=discord.Colour.from_rgb(112, 226, 255))
            em.set_footer(text=f"Page {cur_page}/{pages}:")            
            message = await ctx.send(embed=em)
            await message.add_reaction("◀️")
            await message.add_reaction("▶️")
            active = True

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
                             # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

            while active:
                try:
                    reaction, user = await ctx.client.wait_for("reaction_add", timeout=60, check=check)
                
                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        if cur_page != pages:
                            chunk = members[(cur_page-1)*per_page:cur_page*per_page]
                        else:
                            chunk = members[(cur_page-1)*per_page:]
                        e = discord.Embed(title=f"{len(members)} Users unbanned:", description=f"{linebreak.join(chunk)}", color=discord.Colour.from_rgb(112, 226, 255))
                        e.set_footer(text=f"Page {cur_page}/{pages}:")
                        await message.edit(embed=e)
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        chunk = members[(cur_page-1)*per_page:cur_page*per_page]
                        e = discord.Embed(title=f"{len(members)} Users unbanned:", description=f"{linebreak.join(chunk)}", color=discord.Colour.from_rgb(112, 226, 255))
                        e.set_footer(text=f"Page {cur_page}/{pages}:")
                        await message.edit(embed=e)
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    await message.delete()
                    active = False




@client.command(aliases=['dr',])
@commands.has_permissions(administrator=True)
async def deleterole(ctx, *, role : discord.Role):
        await role.delete()
        emb = discord.Embed(description=f'successfully deleted the role  {role} ', color = discord.Colour.from_rgb(47,49,54))
        await ctx.send(embed=emb)



@client.command(aliases=['av'])
async def avatar(ctx, *, member: discord.Member=None):
        if not member: 
            member = ctx.message.author
        userAvatar = member.avatar_url
        embed = discord.Embed(color = discord.Color.from_rgb(47,49,54), title=f'{member.name}\'s avatar:')
        embed.set_image(url=userAvatar)
        await ctx.send(embed=embed)


@client.command(aliases=['cr',])
@commands.has_permissions(administrator=True)
async def create_role(ctx, *, role):
        guild = ctx.guild
        await guild.create_role(name=role)
        emb = discord.Embed(description=f'successfully created the role  {role} ', color = discord.Colour.from_rgb(47,49,54))
        await ctx.send(embed=emb)

@client.command(aliases=["mc"])
async def member_count(ctx):

    a=ctx.guild.member_count
    emb = discord.Embed(title=f"members in {ctx.guild.name}",description=a,color=discord.Color((0x2f3136)))
    await ctx.send(embed=emb)


@client.command()
async def support(ctx):
        try:
            await ctx.author.send(" https://discord.gg/QkxgYDrZkk \nHeres my support server")
            helpMsg = await ctx.send(" Sent invite in your dms. ")
        except Exception:
            helpMsg = await ctx.send(f" {ctx.author.mention} https://discord.gg/QkxgYDrZkk\n*if you need help ping <@694624137901113365>  ")



@client.command(aliases=["setavatar"])
@commands.is_owner()
async def updateavatar(ctx, *, url=None):
    if not url:
        if ctx.message.attachments:
            url = ctx.message.attachments[0].url
        else:
            await ctx.send("provide a valid image :no_entry:")
            return
    avatar = requests.get(url).content
    try:
        await ctx.bot.user.edit(password=None, avatar=avatar)
    except:
        return await ctx.send("cant change pfp anymore")
    await ctx.send("ive changed my profile picture")




@client.command()
@commands.has_permissions(manage_emojis=True)
async def add(ctx, emote = None):
    if emote == None:
        emb = discord.Embed(description=f'please provide an emote to steal.', color = discord.Color.red())
        await ctx.send(embed=emb)
        return
    try:
        if emote[0] == '<':
            name = emote.split(':')[1]
            emoji_name = emote.split(':')[2][:-1]
            anim = emote.split(':')[0]
            if anim == '<a':
                url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
            else:
                url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
            try:
                response = requests.get(url) 
                img = response.content
                emote = await ctx.guild.create_custom_emoji(name=name, image=img) 
                em = discord.Embed(description=f'the emote "{emote}" has been added.', color=discord.Color.from_rgb(0,0,0))
                await ctx.send(embed= em)
            except Exception as e:
                em = discord.Embed(description=f"{e}.", color=discord.Color.from_rgb(0,0,0))
                await ctx.send(embed= em)
                return
        else:
            em = discord.Embed(description=f"please provide a valid emote.", color=discord.Color.from_rgb(0,0,0))
            await ctx.send(embed= em)
            return
    except Exception as e:
        em = discord.Embed(description=f"{e}.", color=discord.Color.from_rgb(0,0,0))
        await ctx.send(embed= em)
        return

@client.command()
@commands.bot_has_permissions(manage_emojis=True)
@commands.has_permissions(manage_emojis=True)
async def delete(ctx, emote : discord.Emoji = None):
    if emote == None:
        emb = discord.Embed(description=f'please provide an emote to delete.', color = discord.Color.from_rgb(0,0,0))
        await ctx.send(embed=emb)
        return
        
    em = discord.Embed(description=f' the emote "{emote}" has been deleted.', color=discord.Color.from_rgb(0,0,0))
    await ctx.send(embed = em)
    await emote.delete() 


@client.command()
@commands.guild_only()
async def enlarge(ctx, emoji = None): 
    if emoji == None:
        emb = discord.Embed(description=f'Please provide an emote to enlarge.', color = discord.Color.red())
        await ctx.send(embed=emb)
        return
    if emoji[0] == '<':
        name = emoji.split(':')[1]
        emoji_name = emoji.split(':')[2][:-1]
        anim = emoji.split(':')[0]
        if anim == '<a':
            url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
        else:
            url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
    else:
        em = discord.Embed(description=f"Please provide a valid emote.", color=discord.Color.red())
        await ctx.send(embed= em)
        return
    em = discord.Embed(title='Enlarged Emote:', color = discord.Color.from_rgb(0,0,0))
    em.set_image(url=url)
    await ctx.send(embed=em)

@client.command(aliases=["emotes"])
async def serveremotes(ctx):
        msg = ""
        for x in ctx.guild.emojis:
            if x.animated:
                msg += "<a:{}:{}> ".format(x.name, x.id)
            else:
                msg += "<:{}:{}> ".format(x.name, x.id)
        if msg == "":
            await ctx.send("There are no emojis in this server")
            return
        else:
            i = 0 
            n = 2000
            for x in range(math.ceil(len(msg)/2000)):
                while msg[n-1:n] != " ":
                    n -= 1
                s=discord.Embed(description=msg[i:n])
                i += n
                n += n
                if i <= 2000:
                    s.set_author(name="{} Emojis".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                await ctx.send(embed=s)




@client.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_channels=True)
@commands.bot_has_guild_permissions(manage_channels=True)
async def lockdown(ctx, channel: discord.TextChannel=None):
    await ctx.message.delete()
    channel = channel or ctx.channel

    if ctx.guild.default_role not in channel.overwrites:
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
        }
        await channel.edit(overwrites=overwrites)
        await ctx.send(f" {channel.name}  is now on lockdown.")
    elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        await ctx.send(f"I have put  {channel.name}  is now on lockdown.")
    else:
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        await ctx.send(f"I have removed  {channel.name}  from lockdown.")

@client.command()
@commands.has_permissions(administrator=True)
async def jail(ctx, member: discord.Member=None):
    embed= discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=(discord.Color
        (0x2f3136)),
        title=f"jailed",
        description=f"you have been jailed in {ctx.guild.name}\n moderator : {ctx.message.author}"
    )
    await member.send(embed=embed)
    if member == None:
        await ctx.send('please provide a member to jail.')
        return
    role = discord.utils.get(ctx.guild.roles, name="jailed")
    if not role:
        await ctx.guild.create_role(name='jailed')
    jail = discord.utils.get(ctx.guild.text_channels, name="jail")
    if not jail:
        try:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }            
            prison = await ctx.guild.create_text_channel('jail', overwrites=overwrites)
            await ctx.send(f'successfully made <#{prison.id}>')
                
        except discord.Forbidden:
            
            return await ctx.send("i have no permissions to create a jail channel")       
    for channel in ctx.guild.channels:
        if channel.name == 'jail':
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            perms.read_messages = True
            await channel.set_permissions(member, overwrite=perms)
        else:
            perms = channel.overwrites_for(member)
            perms.send_messages = False
            perms.read_messages = False
            perms.view_channel = False
            await channel.set_permissions(member, overwrite=perms)
    role = discord.utils.get(ctx.guild.roles, name="jailed")
    await member.add_roles(role)
    await ctx.send(f'jailed {member.mention}')

@client.command(aliases=['free'])
@commands.has_permissions(administrator=True)
async def unjail(ctx, member : discord.Member):
    embed= discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=(discord.Color
        (0x2f3136)),
        title=f"unjailed",
        description=f"you have been unjailed in {ctx.guild.name}\n moderator : {ctx.message.author}"
    )
    await member.send(embed=embed)
    role = discord.utils.get(ctx.guild.roles, name="jailed")
    for channel in ctx.guild.channels:
        if channel.name == 'jail':
            perms = channel.overwrites_for(member)
            perms.send_messages = None
            perms.read_messages = None
            await channel.set_permissions(member, overwrite=perms)
        else:
            perms = channel.overwrites_for(member)
            perms.send_messages = None
            perms.read_messages = None
            perms.view_channel = None
            await channel.set_permissions(member, overwrite=perms)
    await member.remove_roles(role)
    await ctx.send(f'{member.mention} is now free')
   
@client.command()
async def jailed(ctx):
    users_in = []  
    jail_role = discord.utils.get(ctx.guild.roles, name="jailed")   
    muted_list = jail_role.members
    for member in muted_list:
        users_in.append(f'{member} - {member.id}\n') 
    members = [str(m) for m in users_in]
    if len(members) == 0:
        await ctx.send(' There are no members in jail! ')
        return
    per_page = 10 
    pages = math.ceil(len(members) / per_page)
    cur_page = 1
    chunk = members[:per_page]
    linebreak = "\n"
        
    em = discord.Embed(title=f"Members in the jail:", description=f"{linebreak.join(chunk)}", color=discord.Colour.from_rgb(255,255,250))
    em.set_footer(text=f"Page {cur_page}/{pages}:")            
    message = await ctx.send(embed=em)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    active = True

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
                        # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

    while active:
        try:
            reaction, user = await ctx.client.wait_for("reaction_add", timeout=60, check=check)
            
            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                if cur_page != pages:
                    chunk = members[(cur_page-1)*per_page:cur_page*per_page]
                else:
                    chunk = members[(cur_page-1)*per_page:]
                e = discord.Embed(title=f"Members in the jail:", description=f"{linebreak.join(chunk)}", color=discord.Colour.from_rgb(0,0,250))
                e.set_footer(text=f"Page {cur_page}/{pages}:")
                await message.edit(embed=e)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                chunk = members[(cur_page-1)*per_page:cur_page*per_page]
                e = discord.Embed(title=f"Members in the jail:", description=f"{linebreak.join(chunk)}", color=discord.Colour.from_rgb(0,0,0))
                e.set_footer(text=f"Page {cur_page}/{pages}:")
                await message.edit(embed=e)
                await message.remove_reaction(reaction, user)
        except asyncio.TimeouStranded:
            await message.delete()
            active = False 
            pass

@client.command(aliases=['joined'])
@commands.guild_only()
async def jp(ctx, member: discord.Member = None):
    if not member: 
        member = ctx.author 
    date_format = "%a, %d %b %Y %I:%M %p"
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    duration = datetime.datetime.now() - member.joined_at 

    hours, remainder = divmod(int(duration .total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    em = discord.Embed(description=f'{member.mention} joined on {member.joined_at.strftime(date_format)} | {days}d, {hours}h, {minutes}m, {seconds}s ago | Join position: {(members.index(member)+1)}', color = discord.Color.from_rgb(47,49,54))
    await ctx.send(embed=em)


@client.command()
async def (ctx):
    embed=discord.Embed(
        title=f"Prefix >",
        description="anti is coming soon!"
    )
    embed.add_field(name="Anti", value="Coming Soon!!!")
    embed.add_field(name="Fun", value="The name says it all")
    embed.add_field(name="Admin", value="Utility")
    embed.add_field(name="Misc", value="General Server Commands")
    embed.add_field(name="Emojis", value="Emote ")
    embed.add_field(name="Server", value="Configs")
    embed.add_field(name="Bot", value="Bot Info")
    embed.add_field(name="Economy", value="Economy stuff")
    embed.add_field(name="Music", value="Music Bot")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def anti(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (3)",
        description=f"whitelist\ndewhitelist\nwhitelisted"
    )
    embed.set_footer(text=f">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)

@client.command()
async def misc(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (5)",
        description=f"avatar\nuserinfo\nmembercount\nbanner\njp(joined)"
    )
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.set_footer(text=f">[command]")
    
    await ctx.channel.send(embed=embed)

@client.command()
async def admin(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (16)",
        description=f"ban\nunban\nkick\njail\nunjail\nbotclear\nclear\nimageclear\nlockdown\nnickname\nrolecolor\naddrole\nremoverole\ncreaterole\ndeleterole\nslowmode\ninrole\nroleinfo\nslowmode"
    )
    embed.set_footer(text=">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)

@client.command()
async def server(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (6)"
        description=f"\nseticon\nservername\nsetbanner\ninvitebackground\nguildicon\nserverinfo"
    )
    embed.set_footer(text=f">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)

@client.command()
async def emojis(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (4)",
        description=f"add\ndelete\nenlarge\nserveremotes"
    )
    embed.set_footer(text=f">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)


@client.command()
async def fun(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (17)",
        description=f" snipe \nkiss\nhug \n slap \n pat \n smug \n couple \n dick \n cute \n loyal \n coinflip \n tickle \n horny \n spank \n 8ball \n feed \n combine \n fact "
    )
    embed.set_footer(text=f">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)    

@client.command()
async def Bot(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (5)",
        description=f" ping \n uptime \n stats \n invite \n support "
    )
    embed.set_footer(text=f">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)   



@client.command()
async def music(ctx):
    embed = discord.Embed(
        color=(discord.Color
        (0x2f3136)),
        title=f"Commands (12)",
        description=f" play \n skip \n queue \n repeat \n stop \n pause \n resume \n np \n volume \n join \n leave "
    )
    embed.set_footer(text=f">[command]")
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    await ctx.channel.send(embed=embed)





@client.command()
@commands.has_permissions(administrator=True)
async def embed(ctx,message,*,url):
    Embed = discord.Embed(description=message)
    Embed.set_image(url=url)
    await ctx.send(embed=Embed)

@client.command()
@commands.has_permissions(administrator=True)
async def embedm(ctx,*,message):
    Embed = discord.Embed(description=message, color=discord.Colour.from_rgb(0,0,0))
    await ctx.send(embed=Embed)



@client.command()
@commands.has_permissions(administrator=True)
async def embedi(ctx,*,url):
    Embed = discord.Embed(color=discord.Color.from_rgb(0,0,0))
    Embed.set_image(url=url)
    await ctx.send(embed=Embed)




@client.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int, channel: discord.TextChannel=None):
    channel = channel or ctx.channel
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(embed=discord.Embed(description=f"set {channel.name} to {seconds} second!", colour=0x36393F))

@slowmode.error
async def slowmode(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permissons to use this command.")


@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx, channel: discord.TextChannel = None):
  channel = channel or ctx.channel
  try:
      message = await ctx.send("Nuking the channel...")
      position = channel.position
      await channel.delete()
      newchannel = await channel.clone(reason=f"Chat Nuked by {ctx.author}")
      embed = discord.Embed(color=(0x2f3136))
      embed.title=f"Chat Nuked by {ctx.author}"
      embed.set_thumbnail(url="https://tenor.com/view/blank-stare-really-idontbelieveyou-side-gif-6151149")
      await message.delete()
      newchannel.edit(position=position)
      await asyncio.sleep(2)
      await newchannel.send(embed=embed)
  except:
      pass




@client.command(pass_context=True)
async def inrole(ctx, *, role: str):
        """Check who's in a specific role"""
        role = get_role(ctx, role)
        if not role:
            return await ctx.send("Invalid role")
        server = ctx.guild
        page = 1
        number = len(role.members)
        if number < 1:
            return await ctx.send("There is no one in this role")
        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
        s=discord.Embed(description=users, colour=0x2f3136)
        s.set_author(name="Users in " + role.name + " ({})".format(number), icon_url=server.icon_url)
        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
        message = await ctx.send(embed=s)
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "▶" or reaction.emoji == "◀":
                        return True
        page2 = True
        while page2:
            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", timeout=30, check=reactioncheck)
                if reaction.emoji == "▶":
                    if page != math.ceil(number / 20):
                        page += 1
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, colour=0x2f3136)
                        s.set_author(name="Users in " + role.name + " ({})".format(number), icon_url=server.icon_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
                    else:
                        page = 1
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, colour=0x2f3136)
                        s.set_author(name="Users in " + role.name + " ({})".format(number), icon_url=server.icon_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
                if reaction.emoji == "◀":
                    if page != 1:
                        page -= 1
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, colour=0x2f3136)
                        s.set_author(name="Users in " + role.name + " ({})".format(number), icon_url=server.icon_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
                    else:
                        page = math.ceil(number / 20)
                        users = "\n".join([str(x) for x in sorted(role.members, key=lambda x: x.name.lower())][page*20-20:page*20])
                        s=discord.Embed(description=users, colour=0x2f3136)
                        s.set_author(name="Users in " + role.name + " ({})".format(number), icon_url=server.icon_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(number / 20)))
                        await message.edit(embed=s)
            except asyncio.TimeoutError:
                try:
                    await message.remove_reaction("◀", ctx.me)
                    await message.remove_reaction("▶", ctx.me)
                except:
                    pass
                page2 = False

    
@client.command()
async def fact(ctx: Context) -> None:
        """Send a random fact."""
        try:
            embed = discord.Embed(
                color=0x2f3136,
                timestamp=datetime.datetime.utcnow(),
                title=f"Fact",
                description=f"{nekos.fact()}",)
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)
        except nekos.errors.NothingFound:
            await ctx.send('Couldn\'t Fetch any "Fact" :(')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
     await ctx.send(f'that is not a valid command, use  >  or  >[category]  to see the categories and commands.')
     raise error





@client.command()
async def assist(ctx, category=None):
   if category is None:
        embed = discord.Embed(color=(0x36393F))
        embed.title="help"
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/750807114020159579/784469613319553024/image0.jpg")
        embed.description = f"for regular commands in Stranded use  >help \nto seek help to a category use  >setup [category]  \n\nto check whos in the whitelist cache do  >whitelisted  it will then show the whitelisted users in that guild.\n\n**Categories**\n\n  anti, fun, music, moderation, misc, info, server  \n\n**Support Team**\n\nTo join the support server and ask questions and learn more about Stranded, [Click Here](https://media.discordapp.net/attachments/773711629409058836/784134945437646879/Stranded_lol3.png://discord.com/api/oauth2/authorize?client_id=781692126748475473&permissions=8&scope=bot)"
        embed.set_footer(text ='Stranded')
        await ctx.send(embed=embed, delete_after=25)
   elif str(category).lower() == "ban":
        embed = discord.Embed(color=(0x2f3136))
        embed.add_field(name="ban", value="bans user from the guild", inline=False)
        embed.add_field(name="usage", value=" >ban @thief ", inline=False)
        embed.add_field(name="permissons required", value="admin, ban members.", inline=False)
        embed.set_footer(text ='Stranded')
        await ctx.send(embed=embed)
   elif str(category).lower() == "kick":
        embed = discord.Embed(color=(0x2f3136))
        embed.add_field(name="kick", value="kicks user from the guild", inline=False)
        embed.add_field(name="usage", value=" >kick @thief ", inline=False)
        embed.add_field(name="permissons required", value="admin, kick members.", inline=False)
        embed.set_footer(text ='Stranded')
        await ctx.send(embed=embed)    
   elif str(category).lower() == "mute":
        embed = discord.Embed(color=(0x2f3136))
        embed.add_field(name="mute", value="mutes user from speaking in the guild", inline=False)
        embed.add_field(name="usage", value=" >mute @thief ", inline=False)
        embed.add_field(name="permissons required", value="admin, mute members.", inline=False)
        embed.set_footer(text ='Stranded')
        await ctx.send(embed=embed)     
   elif str(category).lower() == "unmute":
        embed = discord.Embed(color=(0x2f3136))
        embed.add_field(name="mute", value="unmutes user and they can now speak", inline=False)
        embed.add_field(name="usage", value=" >unmute @thief ", inline=False)
        embed.add_field(name="permissons required", value="admin, unmute members.", inline=False)
        embed.set_footer(text ='Stranded')
        await ctx.send(embed=embed) 
   elif str(category).lower() == "unban":
        embed = discord.Embed(color=(0x2f3136))
        embed.add_field(name="unban", value="unbans user from the guild", inline=False)
        embed.add_field(name="usage", value=" >unban @thief ", inline=False)
        embed.add_field(name="permissons required", value="admin,", inline=False)
        embed.set_footer(text ='Stranded')
        await ctx.send(embed=embed)    

@client.command(name='boosters')
async def boosters_send(ctx):
    await ctx.message.delete()
    guildName = ctx.guild.name
    boosters = ""
    for user in {ctx.guild.premium_subscription_count}:
        boosters = boosters+str(user)+","
    if len(boosters)<=0:
        boosters="None"
    container = discord.Embed(title=guildName, color=0x2f3136)
    container.add_field(name="Current boosters:" ,value=boosters ,inline=False)
    container.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=container)





client.run(os.environ["CLIENT_TOKEN"])