import discord
from discord.ext import commands

afkdict = {}

class AFK(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('AFK Cog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        global afkdict
        
        if ",afk" in message.content.lower():
         return


        for member in message.mentions:
            if member != message.author:
                if member in afkdict:
                    afkmsg = afkdict[member]
                    await message.channel.send(f" {member.name} is afk - {afkmsg}")
                    
        if message.author in afkdict:
            afkdict.pop(message.author)
            await message.channel.send(f'{message.author.mention} is no longer afk')


    @commands.command()
    async def afk(self, ctx, *, message):
        global afkdict
        
        if ctx.message.author in afkdict:
            afkdict.pop(ctx.message.author)
            await ctx.send('you are no longer afk')

        else:
            afkdict[ctx.message.author] = message
            await ctx.send(f"You are now afk with message - {message}")

def setup(client):
    client.add_cog(AFK(client))