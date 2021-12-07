# exec - run code straight from Discord

## Usage

| **Command** | **Description** |
|---|---|
`execute ```lang` | Execute a snippet with the specified language. A syntax-highlighted code block must be used for the bot to recognize code. For example, to run Python code, use `execute ```py`, then your code on a new line.
`@exec help` | Display help
`@exec info` | Display info

## Hosting
*(I built this before the message content intent and before slash commands were a big deal. If you want to host your own copy of the bot, I **strongly** recommend adding slash command support. If you make a PR with slash command support, I'll give you a cookie :)*

1. Install `docker`, `python`, and `discord.py`
2. Add a `playground` directory at `discord/playground`
2. Update `launcher.template.sh`
    1. You can get a token from [discord.com/developers/applications](https://discord.com/developers/applications)
    2. Set the environment to `MASTER`
    2. Add a callback webhook for logging new executions and guild joins
2. Run the launcher script

## Expanding
Adding languages is supposed to be fairly streamlined. In theory, any language is supported.

The last two steps are "vanity" steps and probably aren't necessary to make the new language work. Probably.

1. Decide on an extension for the language. For example, `rust` is `rs`.
2. Design a regex string to detect when a syntax-highlighted code block is in a message. See `discord/playground.py/_exec()`
2. Add a new Dockerfile in `discord/dockerfiles` to run the code. Look at the existing Dockerfiles for inspiration. At a minimum, a new Dockerfile needs to
    1. Be named `extension-Dockerfile` (e.g. `rs-Dockerfile`)
    2. Install dependencies to compile/run the code
    2. Accept a `MESSAGE_ID` build arg
    2. Import the code from the `discord/playground` directory based on the `MESSAGE_ID` build arg
    2. (If the language is compiled) compile the code
    2. Run the code
2. If you want to add code wrapping (e.g. wrapping a `main()` function around snippets), add that to the dictionary in `discord/code_processing.py`
2. Add an emoji to represent the language in the callback. The emoji should be in `discord/playground.py/__init__()` and `discord/help.py/__init__()`

## License

Do whatever you want. [unlicense.org](https://unlicense.org)

```
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
```

## Support

[queue.bot/link/discord](https://queue.bot/link/discord) feel free to drop me a DM (no need to send a friend request)
