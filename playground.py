import asyncio
import os
import threading

import discord
from discord.ext import commands
import re
import docker

import sqlite3
import datetime

from logger import Logger


def get_logs_from_container(container, save_name):
    container.wait()

    output = container.logs()

    with open("playground/{}.log".format(save_name), mode="wb") as f:
        f.write(output)


class Playground(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dockerHost = docker.from_env()

        self.conn = sqlite3.connect("playground.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS playground (
                        id INTEGER PRIMARY KEY,
                        executed_at FLOAT,
                        message_id TEXT,
                        lang TEXT)''')

        self.logger = Logger()

    async def log(self, message_id, language):
        self.c.execute('''INSERT INTO playground
                        (executed_at, message_id, lang)
                        VALUES(?, ?, ?)''', (datetime.datetime.now().timestamp(), str(message_id), language.lower()))
        self.conn.commit()

        e = discord.Embed(title="exec log", description="new snippet executed", color=discord.Color(9510889),
                          timestamp=datetime.datetime.now())
        e.add_field(name="language", value=language, inline=False)
        e.add_field(name="message id", value=message_id, inline=False)
        e.set_footer(text="exec", icon_url="https://cdn.discordapp.com/avatars/830972631917789265"
                                               "/5e97d058954d564c39b6e1d91ad09e39.png")
        await self.logger.log_embed(e)

    @commands.command(name="ute")
    @commands.max_concurrency(1, commands.BucketType.user, wait=False)
    async def _exec(self, ctx):
        """Execute a code snippet and post the result."""

        async with ctx.typing():
            code = ""
            lang = ""
            # TODO read from JSON
            regexes = ["```(?:python|py)([\s\S]*?)```",
                       "```(?:c)([\s\S]*?)```",
                       "```(?:golang|go)([\s\S]*?)```",
                       "```(?:bash|sh)([\s\S]*?)```",
                       "```(?:zsh)([\s\S]*?)```",
                       "```(?:rust|rs)([\s\S]*?)```"]
            langs = ["py",
                     "c",
                     "go",
                     "bash",
                     "zsh",
                     "rs"]
            i = 0
            while i < len(regexes):
                r = re.compile(regexes[i])
                match = r.search(ctx.message.content)
                if match:
                    code = match.group(1)
                    lang = langs[i]
                    break

                i += 1

            if lang == "" or code == "":
                await ctx.message.add_reaction("❌")
                await ctx.send("Unknown language. Please use a formatted code block (e.g. ` ```c`).")
                return

            await ctx.message.add_reaction("⏳")

            os.makedirs("playground", exist_ok=True)
            with open("playground/{}.{}".format(ctx.message.id, lang), mode="w") as f:
                f.write(code)

            try:
                self.dockerHost.images.build(path="./",
                                             dockerfile="dockerfiles/{}-Dockerfile".format(lang),
                                             buildargs={"MESSAGE_ID": str(ctx.message.id)},
                                             tag="exec/" + str(ctx.message.id),
                                             forcerm=True)
            except docker.errors.BuildError:
                await ctx.message.remove_reaction("⏳", ctx.guild.me)
                await ctx.message.add_reaction("❌")
                await ctx.send("Your code failed to compile. Please double-check syntax and try again.")

                os.remove("playground/{}.{}".format(ctx.message.id, lang))
                return

            container = self.dockerHost.containers.run("exec/" + str(ctx.message.id),
                                                       name=str(ctx.message.id),
                                                       auto_remove=False,
                                                       stdout=True,
                                                       stderr=True,
                                                       detach=True,
                                                       cpu_shares=512,
                                                       mem_limit="512m",
                                                       device_write_bps=[{"Path": "/dev/sda", "Rate": 500000}],
                                                       network_disabled=True)

            t = threading.Thread(target=get_logs_from_container,
                                 name=str(ctx.message.id),
                                 args=(container, ctx.message.id))
            t.daemon = True
            t.start()

            os.remove("playground/{}.{}".format(ctx.message.id, lang))

            time_running = 0
            was_killed = False

            while not os.path.exists("playground/{}.log".format(ctx.message.id)):
                await asyncio.sleep(1)
                time_running += 1
                if time_running > 45:
                    try:
                        container.kill()
                    except docker.errors.APIError:
                        pass
                    was_killed = True
                    break

            if was_killed:
                await ctx.message.remove_reaction("⏳", ctx.guild.me)
                await ctx.message.add_reaction("❌")
                await ctx.send("<@{}> Your program was terminated because it took too long".format(ctx.author.id))
            else:
                await ctx.message.remove_reaction("⏳", ctx.guild.me)
                await ctx.message.add_reaction("✅")
                msg = await ctx.send("<@{}>".format(ctx.author.id),
                                     file=discord.File("playground/{}.log".format(ctx.message.id)))
                await msg.add_reaction("🗑️")
                await self.log(ctx.message.id, lang)

            try:
                os.remove("playground/{}.log".format(ctx.message.id))
            except FileNotFoundError:
                pass

        return

    @_exec.error
    async def _exec_error(self, ctx, error):
        if isinstance(error, commands.errors.MaxConcurrencyReached):
            await ctx.message.add_reaction("❌")
            await ctx.send("You may only run one instance of this command at a time.")
        else:
            raise error

    @commands.Cog.listener("on_raw_reaction_add")
    async def _on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        if channel is not None:
            message = channel.get_partial_message(payload.message_id)
        else:
            # DM
            return

        user_id = payload.user_id
        emoji = payload.emoji

        if emoji.name != "🗑️":
            return

        message = await message.fetch()
        if message.author.id != self.bot.user.id:
            return

        target = await guild.fetch_member(user_id)
        if target is None:
            return

        if target in message.mentions:
            await message.edit(content="<@{}> [redacted]".format(target.id))

        return
