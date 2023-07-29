from telegram import Bot, Update
import logging
import asyncio
from keys import tele_token

BOT_TOKEN = tele_token

async def get_chat_id(bot_token):
    try:
        bot = Bot(token=bot_token)
        updates = await bot.get_updates()
        chat_id = updates[-1].message.chat_id
        return chat_id
    except Exception as e:
        logging.error(f"Failed to get chat_id: {e}")
        return None

async def main():
    chat_id = await get_chat_id(BOT_TOKEN)
    if chat_id:
        print(f"Chat ID: {chat_id}")
    else:
        print("Failed to retrieve chat ID.")

if __name__ == "__main__":
    asyncio.run(main())