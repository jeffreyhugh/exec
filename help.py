import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.python = "<:python:831113611107368970>"
        self.go = "<:go:831114835852918815>"
        self.c = "<:c_:831116196660903987>"
        self.rust = "<:rust:831116517679693825>"
        self.bash = "<:bash:831116845133332500>"

    @commands.command(name="c help", aliases=["cute help"])
    async def _help(self, ctx):
        langs = "{}, {}, {}, {}, and {}".format(self.python, self.go, self.c, self.rust, self.bash)
        description = """exec runs code snippets sent through Discord. Each snippet is completely isolated in its own container and may run for a maximum of 45 seconds.

To run a snippet, type `exec ` followed by a syntax-highlighted code block (e.g. Python is ` ```py`). After the code inside the block finishes running, the first few lines of the log will be posted, along with the entire `.log` file.

exec supports {}. 

*📨 exec@queue.bot*
""".format(langs)
        e = discord.Embed(name="exec help", color=discord.Color(9510889), description=description)
        e.set_author(name="exec", icon_url="https://cdn.discordapp.com/avatars/830972631917789265"
                                           "/5e97d058954d564c39b6e1d91ad09e39.png")
        await ctx.send(embed=e)