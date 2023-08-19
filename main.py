import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaWebPage
import pandas as pd
import config

if config.api_id == '' or config.api_hash == '' or config.phone == '':
    print('Чогось нехватає, додайте будь ласка значення до config.py')
    quit()

# Замість `excel_file` введіть шлях та ім'я файлу для збереження даних у форматі Excel (наприклад, 'messages.xlsx')
excel_file = 'result.xlsx'

# Замість `chat_link` введіть ссилку на чат у форматі 'https://t.me/your_chat'
chat_link = input('Силка на телеграм канал: ')
if 't.me' not in chat_link:
    chat_link = input('Силка на телеграм канал у виді (https://t.me/.....): ')

client = TelegramClient('userbot_session', config.api_id, config.api_hash)
client.start(config.phone)

async def main():
    # Отримуємо інформацію про всі повідомлення у чаті
    tiny = []
    data = []

    offset_id = None
    limit = 4000

    while True:
        if offset_id is None:
            offset_id = 0
        messages = await client.get_messages(chat_link, limit=limit, offset_id=offset_id)
        if not messages:
            break

        for message in messages:
            try:
                msgs = message.message
                if any(keyword in msgs for keyword in ['.com', '.info', '.de', '.at', '.io', '.co', '.ai']):
                    link = msgs
                    sender = message.sender_id
                    date = (message.date.year, message.date.month, message.date.day)

                    data.append((link, sender, date))
                    print(data)

            except Exception as e:
                print('Error:', e)

        offset_id = messages[-1].id
        await asyncio.sleep(0.5)

    # Всі повідомлення знаходяться у списку all_messages
    df = pd.DataFrame(data, columns=['Link', 'Sender', 'Date'])
    df.to_excel(excel_file, index=False)

    print("Data saved to", excel_file)

with client:
    client.loop.run_until_complete(main())
