import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import datetime
import os

TOKEN = "Bot_token"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Tugmalar
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ertalab topshirish")],
        [KeyboardButton(text="Kechki topshirish")],
        [KeyboardButton(text="Umumiy hajm")]
    ],
    resize_keyboard=True
)

file_name = "milk_data.txt"

# 🔹 Kunni chiqarish (Dushanba, Seshanba...)
def get_today():
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    return days[datetime.datetime.now().weekday()]

# 🔹 Faylni tozalash (faqat dushanba kuni)
def reset_file_if_monday():
    if get_today() == "Dushanba":
        open(file_name, "w", encoding="utf-8").close()

# 🔹 Faylga yozish
def save_milk(shift, litr):
    day = get_today()
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{day}: {shift} {litr} litr\n")

# 🔹 Umumiy hisob (faqat hozirgi kungacha)
def get_summary():
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    today_index = datetime.datetime.now().weekday()  # 0 = Dushanba, 6 = Yakshanba

    total = 0
    if not os.path.exists(file_name):
        return 0, 0

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            for i in range(today_index + 1):  # hozirgi kungacha bo'lganlar
                if line.startswith(days[i]):
                    litr = int(line.split()[-2])  # "5 litr" -> 5
                    total += litr
                    break
    return total, total * 5800

# Start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    reset_file_if_monday()  # har startda tekshiradi
    await message.answer("👋 Assalomu alaykum!\nSut topshirish botiga xush kelibsiz.", reply_markup=menu)

# Ertalab
@dp.message(lambda msg: msg.text == "Ertalab topshirish")
async def morning_milk(message: types.Message):
    await message.answer("Ertalab nechchi litr sut topshirdingiz?")

@dp.message(lambda msg: msg.text.isdigit() and msg.text != "Umumiy hajm")
async def save_morning(message: types.Message):
    last_message = (await bot.get_chat_history(message.chat.id, limit=2))[1].text
    litr = int(message.text)
    if "Ertalab" in last_message:
        save_milk("Kunduzgi", litr)
        await message.answer(f"✅ {litr} litr ertalab yozildi.", reply_markup=menu)
    elif "Kechki" in last_message:
        save_milk("Kechki", litr)
        await message.answer(f"✅ {litr} litr kechki yozildi.", reply_markup=menu)

# Kechki
@dp.message(lambda msg: msg.text == "Kechki topshirish")
async def evening_milk(message: types.Message):
    await message.answer("Kechqurun nechchi litr sut topshirdingiz?")

# Umumiy hajm
@dp.message(lambda msg: msg.text == "Umumiy hajm")
async def total_milk(message: types.Message):
    total, summa = get_summary()
    today = get_today()
    await message.answer(
        f"📅 Dushanbadan {today}gacha\n"
        f"🧾 Umumiy hajm: {total} litr\n"
        f"💰 Umumiy summa: {summa} so'm"
    )

# Run bot
async def main():
    reset_file_if_monday()  # bot ishga tushganda ham tekshiradi
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

