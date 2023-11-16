from utils import convert_to_data
from mongoDB import get_aggregate_data
from settings import TOKEN_TG, WEBHOOK_HOST, WEBHOOK_PATH
from settings import WEBAPP_HOST, WEBAPP_PORT, help_message
import logging

from aiogram import Bot, types
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

logging.basicConfig(level=logging.INFO)

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


@dp.message_handler(commands=['start', 'help'])
async def process_help_command(message: types.Message):
    await message.answer(help_message)


@dp.message_handler(content_types=['text'])
async def currency_command(message: types.Message):
    input_data = convert_to_data(message.text)

    if isinstance(input_data, str):
        output_msg = f"** Error: {input_data}"
    else:
        output_msg = get_aggregate_data(input_data)

    print(f"** Result: {output_msg}")

    await message.answer(output_msg)


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

