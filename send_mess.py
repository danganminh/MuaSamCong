import time
import telegram
from telegram.error import RetryAfter, TimedOut


api_key = '6422892988:AAGUP63bMTfcP6NXZJ49-CxKU66kN6R1_-0'
user_id = '-4158750986'

# Function to send message to Telegram
async def telegram_send(message):
    tries = 0
    max_tries = 2
    retry_delay = 45
    while tries < max_tries:
        try:
            print(message)
            bot = telegram.Bot(token=api_key)
            await bot.send_message(chat_id=user_id, text=message)
            break
        except RetryAfter:
            time.sleep(retry_delay)
            tries += 1
        except TimedOut:
            time.sleep(retry_delay)
            tries += 1