#!/bin/sh

export EXECBOT_DISCORD_TOKEN=""
export EXECBOT_ENV_TYPE="MASTER"
export EXECBOT_LOGGING_WEBHOOK=""

mkdir -p discord/playground

cd discord && python main.py
