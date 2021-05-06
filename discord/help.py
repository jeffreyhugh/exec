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
        self.js = "<:nodejs:834358450309300265>"

    @commands.command(name="help")
    async def _help(self, ctx):
        langs = "{}, {}, {}, {}, {}, and {}".format(self.python, self.go, self.c, self.rust, self.bash, self.js)
        description = """exec runs code snippets straight from Discord. Each snippet is completely isolated in its own container and runs for a maximum of 45 seconds.

To run a snippet, type `execute ` (note the space) followed by a [syntax-highlighted code block](https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51#syntax-highlighting) (e.g. Python is ` ```py`). After the code inside the block finishes running, the entire `.log` file will be posted.

exec supports {}. 
""".format(langs)
        e = discord.Embed(color=discord.Color(9510889), description=description)
        e.set_footer(text="queue.bot/exec", icon_url="https://cdn.discordapp.com/avatars/830972631917789265"
                                           "/5e97d058954d564c39b6e1d91ad09e39.png")
        await ctx.send(embed=e)