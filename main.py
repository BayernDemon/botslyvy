import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from datetime import datetime
from aiogram.types import Message
import os

API_TOKEN = '8351428999:AAF-P-0Lu5d3olDGIpRBKoXLhZ9jkZUSdno'
CHANNEL_URL = "https://t.me/+Z4Eqdz8K6o8yNDVi"
ADMIN_ID = 1938874314

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

got_probnik = set()

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Купить слив", callback_data="buy")],
        [InlineKeyboardButton(text="✅ Пробник", callback_data="probnik")],
        [InlineKeyboardButton(text="📢 Наш канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="💡 Предложка", callback_data="offer")],
        [InlineKeyboardButton(text="🛠 Поддержка", callback_data="support")]

    ])

# Назад
def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    name = message.from_user.first_name or "NoName"

    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"{username} | {user_id}\n")

    await message.answer(
        f"👋 Привет, {name}!\n\n"
        "📸 Тут ты можешь получить пробник или купить полный архив c сливами: Парадокси, Инстасамки, Хофманиты.\n"
        "💬 Также можешь оставить пожелание кого добавить!",
        reply_markup=main_menu()
    )

# Обработка кнопки "Купить слив"
@dp.callback_query(F.data == "buy")
async def send_buy(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "💳 Выбери способ оплаты 200 грн / 500 руб / 5 USDT:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 DonationAlerts", url="https://www.donationalerts.com/r/genetika52")],
            [InlineKeyboardButton(text="🪙 TON (крипта)", callback_data="pay_ton")],
            [InlineKeyboardButton(text="🪙 USDT (крипта)", callback_data="pay_usdt")],
            [InlineKeyboardButton(text="🧾 Инструкция", callback_data="pay_info")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ])
    )

# Оплата через TON
@dp.callback_query(F.data == "pay_ton")
async def send_ton(callback: types.CallbackQuery):
    await callback.message.delete()

    ton_address = "UQBJfMNwZw6C6r_yB_3odEqh1Q4plxZ8idGF1HlcSWBgOB4G"
    qr_url = f"https://tonhub.com/transfer/{ton_address}"

    await callback.message.answer(
        f"🪙 <b>TON (TRC20)</b>\n\n"
        f"<b>Адрес:</b>\n<code>{ton_address}</code>\n\n"
        f"💡 Отправь любую сумму от <b>5 USDT в TON</b> и после оплаты нажми /check\n\n"
        f"<a href='{qr_url}'>💳 Оплатить через TON Hub</a>",
        reply_markup=back_button()
    )

@dp.callback_query(F.data == "pay_usdt")
async def send_usdt(callback: CallbackQuery):
    await callback.message.delete()

    usdt_address = "TH6wBmtu2rmnijnPG99AiyGATWLw75iPm1"  # Вставьте свой адрес USDT
    binance_url = "https://www.binance.com/ru-UA"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="usdt_paid")],
        [InlineKeyboardButton(text="💰 Купить через Binance", url=binance_url)],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])

    await callback.message.answer(
        "**Оплата через USDT (TRC20)**\n\n"
        f"💸 Сумма: `5 USDT`\n"
        f"📬 Адрес: `{usdt_address}`\n\n"
        "После оплаты нажмите кнопку ниже:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# Инструкция по оплате
@dp.callback_query(F.data == "pay_info")
async def pay_info(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "📌 <b>Инструкция по оплате</b>\n\n"
        "1. Выбери удобный способ оплаты.\n"
        "2. Отправь оплату.\n"
        "3. Нажми /check и отправь скрин или ник, с которого платил.\n\n"
        "После проверки мы вышлем архив 📦",
        reply_markup=back_button()
    )



# Проверка оплаты
@dp.message(Command("check"))
async def check_payment(message: types.Message):
    await message.answer("🔍 Напиши сюда, что ты оплатил или отправь скрин.\nПосле проверки мы отправим архив 📦")
    await bot.send_message(ADMIN_ID, f"🧾 Пользователь @{message.from_user.username or 'NoUsername'} ({message.from_user.id}) запросил проверку оплаты.")

# Пробник
@dp.callback_query(F.data == "probnik")
async def send_probnik(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id

    if user_id in got_probnik:
        await callback.message.answer("⚠️ Ты уже получал пробник. Чтобы получить полный слив — нажми «Купить слив».", reply_markup=back_button())
    else:
        got_probnik.add(user_id)
        file = FSInputFile("files/probnik.jpg")
        await callback.message.answer_photo(file, caption="Вот пробник 😏\nПолный архив доступен после оплаты 💰", reply_markup=back_button())

# Предложка
@dp.callback_query(F.data == "offer")
async def handle_offer(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("💡 Напиши сюда, кого хочешь видеть в следующих сливах. Мы всё читаем 👀", reply_markup=back_button())

# Поддержка
@dp.callback_query(F.data == "support")
async def support_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "🛠 Если бот работает некорректно или возникли вопросы — напиши сюда: @spb52nggFT\n\n"
        "Мы стараемся отвечать быстро 💬",
        reply_markup=back_button()
    )

# Назад
@dp.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        f"👋 Привет, {callback.from_user.first_name}!\n\n"
        "📸 Тут ты можешь получить пробник или купить полный архив.\n"
        "💬 Также можешь оставить пожелание кого добавить!",
        reply_markup=main_menu()
    )

# Отправка архива вручную (только для админа)
@dp.message(Command("s_a3129"))
async def send_archive(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    file = FSInputFile("files/full_archive.zip")
    await message.answer_document(file, caption="📦 Вот твой полный слив. Спасибо за оплату!")

# Обработка ошибок
@dp.errors()
async def error_handler(update, exception):
    await bot.send_message(ADMIN_ID, f"⚠️ Ошибка у пользователя:\n{exception}")
    return True

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
