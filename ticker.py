import discord
from discord.ext import commands, tasks

class Ticker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.ticker_messages = ["@exec help"]

        self.ticker_loop.start()

    @tasks.loop(seconds=20)
    async def ticker_loop(self):
        await self.bot.change_presence(
            activity=discord.Game(self.ticker_messages[self.index % len(self.ticker_messages)]))
        if self.index % len(self.ticker_messages) == 0:
            self.index = 0
        self.index += 1

    @ticker_loop.before_loop
    async def before_ticker_loop(self):
        await self.bot.wait_until_ready()