import datetime

import discord
from discord.ext import commands

from discord.logger import Logger


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        print("{} is now logged in and ready".format(self.bot.user))

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild):
        e = discord.Embed(title="joined guild", color=discord.Color(9510889),
                          timestamp=datetime.datetime.now())
        e.add_field(name="name", value=guild.name.lower())
        e.add_field(name="members", value=str(guild.member_count))
        e.add_field(name="total guilds", value=str(len(self.bot.guilds)))
        e.set_footer(text="exec", icon_url="https://cdn.discordapp.com/avatars/830972631917789265"
                                           "/5e97d058954d564c39b6e1d91ad09e39.png")
        await self.logger.log_embed(e)

    @commands.command(name="guilds")
    async def _guilds(self, ctx):
        """Display guild count"""
        await ctx.send("{} guilds".format(len(self.bot.guilds)))

    # TODO add event queue for log messages (similar to Neptune)
