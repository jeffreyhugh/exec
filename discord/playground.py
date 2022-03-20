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
from code_processing import _processing


# Define a separate function so it can be run on a different thread
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

        self.lang_emojis = {"py": "<:python:831113611107368970>",
                            "go": "<:go:831114835852918815>",
                            "c": "<:c_:831116196660903987>",
                            "rs": "<:rust:831116517679693825>",
                            "bash": "<:bash:831116845133332500>",
                            "zsh": "<:bash:831116845133332500>",
                            "js": "<:nodejs:834358450309300265>",
                            "cpp": "<:cpp:917582153544507442>",
                            "java": "<:java:955167082658558024>",
                            "hs": "<:haskell:955167472850464768>"}

    async def log(self, message_id, language):
        """Store the message ID and language in the database for statistical purposes"""
        self.c.execute('''INSERT INTO playground
                        (executed_at, message_id, lang)
                        VALUES(?, ?, ?)''', (datetime.datetime.now().timestamp(), str(message_id), language.lower()))
        self.conn.commit()

        emoji = self.lang_emojis[language.lower()]
        if emoji is None:
            emoji = "?"

        await self.logger.log_string(emoji)

    @commands.command(name="ute")
    @commands.max_concurrency(1, commands.BucketType.user, wait=False)
    async def _exec(self, ctx):
        """Execute a code snippet and post the result."""

        code = ""
        lang = ""
        # TODO read from JSON
        regexes = ["```(?:python|py)([\s\S]*?)```",
                   "```(?:c\+\+|cpp)([\s\S]*?)```",
                   "```(?:c)([\s\S]*?)```",
                   "```(?:golang|go)([\s\S]*?)```",
                   "```(?:bash|sh)([\s\S]*?)```",
                   "```(?:zsh)([\s\S]*?)```",
                   "```(?:rust|rs)([\s\S]*?)```",
                   "```(?:javascript|js)([\s\S]*?)```",
                   "```(?:java)([\s\S]*?)```",
                   "```(?:haskell|hs)([\s\S]*?)```"]
        langs = ["py",
                 "cpp",
                 "c",
                 "go",
                 "bash",
                 "zsh",
                 "rs",
                 "js",
                 "java",
                 "hs"]
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
            await ctx.reply("Unknown language. Please use a formatted code block (e.g. ` ```c`).")
            return

        await ctx.message.add_reaction("⏳")

        # add default code (#include, etc) if it doesn't have it
        code = _processing(code=code, lang=lang)

        os.makedirs("playground", exist_ok=True)
        with open("playground/{}.{}".format(ctx.message.id, lang), mode="w") as f:
            f.write(code)

        try:
            self.dockerHost.images.build(path="./",
                                         dockerfile="dockerfiles/{}-Dockerfile".format(
                                             lang),
                                         buildargs={
                                             "MESSAGE_ID": str(ctx.message.id)},
                                         tag="execbot/" + str(ctx.message.id),
                                         forcerm=True)
        except docker.errors.BuildError as e:
            self.logger.error(repr(e))
            await ctx.message.remove_reaction("⏳", ctx.me)
            await ctx.message.add_reaction("❌")
            await ctx.reply("Your snippet failed to compile. Please double-check syntax and try again.")

            os.remove("playground/{}.{}".format(ctx.message.id, lang))
            return

        container = self.dockerHost.containers.run("execbot/" + str(ctx.message.id),
                                                   name=str(ctx.message.id),
                                                   auto_remove=False,
                                                   stdout=True,
                                                   stderr=True,
                                                   detach=True,
                                                   cpu_shares=512,
                                                   mem_limit="512m",
                                                   device_write_bps=[
                                                       {"Path": "/dev/sda", "Rate": 500000}],
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
            await ctx.message.remove_reaction("⏳", ctx.me)
            await ctx.message.add_reaction("❌")
            await ctx.reply("Your snippet was terminated because it took too long".format(ctx.author.id))
        else:
            await ctx.message.remove_reaction("⏳", ctx.me)
            await ctx.message.add_reaction("✅")
            await ctx.reply(file=discord.File("playground/{}.log".format(ctx.message.id)))
            await self.log(ctx.message.id, lang)

        try:
            os.remove("playground/{}.log".format(ctx.message.id))
        except FileNotFoundError:
            pass

    @_exec.error
    async def _exec_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MaxConcurrencyReached):
            await ctx.message.add_reaction("❌")
            await ctx.reply("You may only run one instance of this command at a time.")
        else:
            raise error
