import logging from aiogram import Bot, Dispatcher, executor, types from languages import LANGUAGES

API_TOKEN = '7616940079:AAHBGT6Xhs75dZzaxnuwPqdC1nalMUuqlUc'  # Токен от BotFather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN) dp = Dispatcher(bot)

Временное хранилище выбранных языков пользователей

user_languages = {}

Получение текста на нужном языке

def get_text(user_id, key): lang = user_languages.get(user_id, 'en') return LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)

Команда /start

@dp.message_handler(commands=['start']) async def send_welcome(message: types.Message): keyboard = types.InlineKeyboardMarkup(row_width=2) for lang_code, lang_data in LANGUAGES.items(): keyboard.insert(types.InlineKeyboardButton(text=lang_data['lang_name'], callback_data=f"lang:{lang_code}"))

await message.answer("🌐 " + get_text

                     
