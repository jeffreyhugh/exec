import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def _info(self, ctx):
        description = """exec is developed by QueueBot. 
    
To report a vulnerability, please email [q@queue.bot](mailto:q@queue.bot?subject=execbot%2FURGENT).

For suggestions, feel free to [join my server](https://discord.gg/gMEZvJC) and DM me.
"""
        e = discord.Embed(color=discord.Color(9510889), description=description)
        e.set_footer(text="queue.bot/exec", icon_url="https://cdn.discordapp.com/avatars/830972631917789265"
                                                     "/5e97d058954d564c39b6e1d91ad09e39.png")

        await ctx.send(embed=e)
