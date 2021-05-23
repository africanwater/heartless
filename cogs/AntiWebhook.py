import discord
from discord.ext import commands
import datetime

class AntiWebhook(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook

    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
        whitelistedUsers = self.db.find_one({ "guild_id": webhook.guild.id })["users"]
        async for i in webhook.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_create):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await i.user.ban()
            await i.target.delete()
            return