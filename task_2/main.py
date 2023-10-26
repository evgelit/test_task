from telethon import TelegramClient, events
from env import env
from bot_processor import BotProcessor

client = TelegramClient(
    env['session_name'],
    env['api_id'],
    env['api_hash']
)


@client.on(events.NewMessage(chats=(env["listen_group"])))
async def listener(event):
    user = await client.get_entity(
        event.message.from_id.user_id
    )
    if user.bot is True:
        processor = BotProcessor()
        answer = processor.process(
            event.message.from_id.user_id,
            event.message.message
        )
        if answer is not None:
            group_entity = await client.get_entity(env["listen_group"])
            await client.send_message(entity=group_entity, message=answer)


client.start()
client.run_until_disconnected()
