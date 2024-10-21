from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import BufferedInputFile

from PIL import Image

from io import BytesIO
import asyncio
import qrcode
import random

from bot_answers import bot_answers
bot_language = 'uk'

BOT_NAME = 'LoyaltySystemPolitehTestBot'
API_TOKEN = '7733063051:AAFga3c0dHXRIgbs7Dw4RAjknnZ6CbVr_S0'

KEY_CHARS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789-'

admins = [567826785]

bot = Bot(token=API_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)

database = {
    "567826785": {
        "token": 0,
        "token_expired": True
    },
}

def generate_token() -> str:
    return ''.join([random.choice(KEY_CHARS) for chr in range(13)])

@dp.message(Command("start"))
async def send_welcome(message: types.Message, command: CommandStart):
    user_id = message.from_user.id
    print(user_id)
    deep_link_argument = command.args
    if deep_link_argument and user_id in admins:
        student_id = deep_link_argument.split('_')[1]
        key = deep_link_argument.split('_')[3]
        await bot.send_message(chat_id=user_id, text=f"yeah boy, {key}")

        user = database.get(student_id, {})
        if user: print("VALID" if user.get("token_expired", False) else "INVALID")
        return

    await bot.send_message(chat_id=user_id, text=bot_answers[bot_language]['start-need-register'])

@dp.message(Command("register"))
async def register_new_user(message: types.Message):
    ...

@dp.message(Command("image"))
async def send_image(message: types.Message):
    user_id = message.from_user.id
    user = database.get(user_id, {})
    random_key = user.get("token", None)

    if user:
        if user.get("token_expired"):
            random_key = generate_token()
            user["token_expired"] = False

    else:
        # user does not exist in db, so we add it there
        database[user_id] = {"token": 0, "token_expired": False}

    deep_link_url = f"https://t.me/{BOT_NAME}?start=userId_{user_id}_key_{random_key}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(deep_link_url)

    img: Image = qr.make_image(fill="black", back_color="white").convert('RGB')
    img = img.resize((500, 500), Image.Resampling.LANCZOS)

    bg: Image = Image.open('./bg.jpg').convert("RGBA")

    img_w, img_h = img.size
    bg_w, bg_h = bg.size

    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

    bg.paste(img, offset)

    img_bytes = BytesIO()
    bg.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    await bot.send_photo(chat_id=user_id, photo=BufferedInputFile(file=img_bytes.read(), filename='qr.png'))

    # expire token after 3 minutes
    await asyncio.sleep(3)
    user["token_expired"] = True

async def main():
    print(123)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
