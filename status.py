import discord
from discord.ext import commands

from logger import Logger


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        print("{} is now logged in and ready".format(self.bot.user))

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        e = discord.Embed(name="exec log", description="joined guild")
        e.add_field(name="name", value=guild.name.lower())
        e.add_field(name="members", value=str(len(guild.members)))

    # TODO add event queue for log messages (similar to Neptune)
