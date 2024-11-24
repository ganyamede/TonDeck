from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from server.App.Storage.config import BOT_TOKEN, WEBAPP_URL
from aiogram.utils import executor
import UpdateGecko

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    webapp_button = InlineKeyboardButton("Open TonDeck", web_app=WebAppInfo(url=WEBAPP_URL))
    keyboard.add(webapp_button)

    await message.answer("Hi, here you will find all your ton tokens, track their price conveniently and keep track of tokens!", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
