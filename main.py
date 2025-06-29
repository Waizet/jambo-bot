from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from languages import LANGUAGES

import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# 🔐 Впиши сюда свой токен от BotFather
BOT_TOKEN = "7616940079:AAHBGT6Xhs75dZzaxnuwPqdC1nalMUuqlUc"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Словарь для хранения языков пользователей
user_languages = {}

# Создание клавиатуры для выбора языка
def get_language_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for code, lang in LANGUAGES.items():
        row.append(KeyboardButton(lang['language_name']))
        if len(row) == 2:
            keyboard.add(*row)
            row = []
    if row:
        keyboard.add(*row)
    return keyboard

# Получение текста по ключу и языку пользователя
def get_text(user_id, key):
    lang_code = user_languages.get(user_id, 'en')
    return LANGUAGES.get(lang_code, LANGUAGES['en']).get(key, f"[{key}]")

# Поиск кода языка по названию
def get_language_code_by_name(name):
    for code, lang in LANGUAGES.items():
        if lang['language_name'] == name:
            return code
    return None

# Команда /start — выбор языка
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("🌍 Please select your language / Пожалуйста, выберите язык:", reply_markup=get_language_keyboard())

# Обработка выбора языка
@dp.message_handler(lambda message: message.text in [lang['language_name'] for lang in LANGUAGES.values()])
async def handle_language_selection(message: types.Message):
    lang_code = get_language_code_by_name(message.text)
    user_languages[message.from_user.id] = lang_code
    welcome = get_text(message.from_user.id, 'welcome')
    choose_role = get_text(message.from_user.id, 'choose_role')
    driver = get_text(message.from_user.id, 'driver')
    passenger = get_text(message.from_user.id, 'passenger')
    taxi = get_text(message.from_user.id, 'taxi')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(driver), KeyboardButton(passenger))
    keyboard.add(KeyboardButton(taxi))

    await message.answer(f"{welcome}\n\n{choose_role}", reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
