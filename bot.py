import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from config import BOT_TOKEN, CHANNEL_ID, ADMIN_IDS
import database as db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class AddAnimeState(StatesGroup):
    waiting_for_code = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@dp.startup()
async def on_startup():
    db.init_db()
    logging.info("Bot ishga tushdi, baza tayyor.")


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Salom! 👋\n\n"
        "Anime kodini yuboring, men sizga o'sha qismni jo'nataman.\n"
        "Masalan: AN001\n\n"
        "Buyruqlar ro'yxati uchun /help yozing."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 Yordam:\n\n"
        "— Anime kodini yozing (masalan: AN001), men sizga videoni yuboraman.\n"
    )
    if is_admin(message.from_user.id):
        text += (
            "\n👤 Admin buyruqlari:\n"
            "— Kanaldagi postni to'g'ridan-to'g'ri menga forward qiling, "
            "so'ng so'ralganda kod kiriting.\n"
            "/list — barcha kodlar ro'yxati\n"
            "/count — nechta anime borligini ko'rish\n"
            "/delete <kod> — kodni o'chirish\n"
        )
    await message.answer(text)


# Admin kanaldan postni bevosita botga forward qilganda ishga tushadi
@dp.message(F.forward_from_chat, F.forward_from_chat.id == CHANNEL_ID)
async def handle_channel_forward(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.update_data(message_id=message.forward_from_message_id)
    await state.set_state(AddAnimeState.waiting_for_code)
    await message.answer(
        "✅ Post qabul qilindi.\n"
        "Endi shu anime/qism uchun kod kiriting (masalan: AN001):"
    )


@dp.message(AddAnimeState.waiting_for_code)
async def save_anime_code(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    data = await state.get_data()
    message_id = data.get("message_id")
    code = message.text.strip()

    db.add_anime(code=code, message_id=message_id, title=code)
    await state.clear()
    await message.answer(
        f"✅ Saqlandi!\nKod: {code.upper()}\n"
        f"Endi foydalanuvchilar shu kodni yozib, ushbu qismni olishlari mumkin."
    )


@dp.message(Command("list"))
async def cmd_list(message: Message):
    if not is_admin(message.from_user.id):
        return
    rows = db.list_anime()
    if not rows:
        await message.answer("Hozircha hech qanday anime qo'shilmagan.")
        return
    text = "📋 Barcha kodlar:\n\n" + "\n".join(f"• {code} — {title}" for code, title in rows)
    await message.answer(text)


@dp.message(Command("count"))
async def cmd_count(message: Message):
    if not is_admin(message.from_user.id):
        return
    n = db.count_anime()
    await message.answer(f"Jami: {n} ta anime bazada.")


@dp.message(Command("delete"))
async def cmd_delete(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Foydalanish: /delete <kod>")
        return
    code = parts[1].strip()
    if db.delete_anime(code):
        await message.answer(f"🗑 {code.upper()} o'chirildi.")
    else:
        await message.answer("Bunday kod topilmadi.")


# Oddiy foydalanuvchi kod yozganda — eng oxirida turishi kerak
@dp.message(F.text)
async def handle_code_request(message: Message):
    code = message.text.strip()
    row = db.get_anime(code)
    if row:
        message_id, title = row
        try:
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=message_id,
            )
        except Exception as e:
            logging.error(f"Copy xatosi: {e}")
            await message.answer("❌ Xatolik yuz berdi, keyinroq urinib ko'ring.")
    else:
        await message.answer("❌ Bunday kod topilmadi. Kodni tekshirib qayta yuboring.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
