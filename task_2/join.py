from telethon.sync import TelegramClient
from telethon import functions
from env import env

with TelegramClient(
        env['session_name'],
        env['api_id'],
        env['api_hash']
) as client:
    result = client(functions.channels.JoinChannelRequest(
        channel=env["listen_group"]
    ))