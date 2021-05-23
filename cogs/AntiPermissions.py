import discord
from discord.ext import commands
import datetime

class AntiPermissions(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        whitelistedUsers = self.db.find_one({ "guild_id": role.guild.id })["users"]
        async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_create):
            if i.user.bot:
                return
            
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await role.guild.ban(i.user)
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        whitelistedUsers = self.db.find_one({ "guild_id": role.guild.id })["users"]
        async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_delete):
            if i.user.bot:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await role.guild.ban(i.users)
            return

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        whitelistedUsers = self.db.find_one({ "guild_id": after.guild.id })["users"]
        async for i in after.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_update):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            if not before.permissions.ban_members and after.permissions.ban_members:
                await after.guild.ban(i.user)
                return

            if not before.permissions.kick_members and after.permissions.kick_members:
                await after.guild.ban(i.user)
                return

            if not before.permissions.administrator and after.permissions.administrator:
                await after.guild.ban(i.user)
                return

            if i.target.id == before.guild.id:
                if after.permissions.kick_members or after.permissions.ban_members or after.permissions.administrator or after.permissions.mention_everyone or after.permissions.manage_roles:
                    await after.guild.ban(i.user)
                    await after.edit(permissions=1166401)
                    
            return