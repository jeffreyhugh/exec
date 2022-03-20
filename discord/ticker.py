import discord
from discord.ext import commands, tasks


class Ticker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.ticker_messages = [
            "@exec help | {{guilds}} guilds",
            "@exec help | github.com/qbxt/exec",
        ]

        self.ticker_loop.start()

    @tasks.loop(seconds=20)
    async def ticker_loop(self):
        m = self.fix_message(
            self.ticker_messages[self.index % len(self.ticker_messages)])
        await self.bot.change_presence(activity=discord.Game(m))
        self.index %= len(self.ticker_messages)
        self.index += 1

    def fix_message(self, message):
        m = message.replace("{{guilds}}", "{}".format(len(self.bot.guilds)))
        return m

    @ticker_loop.before_loop
    async def before_ticker_loop(self):
        await self.bot.wait_until_ready()
