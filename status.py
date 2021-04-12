from discord.ext import commands

from logger import Logger


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        print("{} is now logged in and ready".format(self.bot.user))

    # TODO add event queue for log messages (similar to Neptune)
