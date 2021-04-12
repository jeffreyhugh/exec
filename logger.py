import os
from discord import Webhook, AsyncWebhookAdapter
import aiohttp


class Logger:
    def __init__(self):
        self.logging_webhook = os.getenv("EXECBOT_LOGGING_WEBHOOK")

    async def log_embed(self, embed):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(self.logging_webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=embed)