from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramForbiddenError

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            "Привіт! 👋\n"
            "Ти потрапив до *Солодкого світу* — місця, де панує гармонія цукру, ніжності й позитиву. Тут на тебе чекає:\n\n"
            "🍰 Солодкі картинки, що зігріють серце\n"
            "🎂 Рецепти на кожен настрій\n"
            "🍬 Цікаві факти про улюблені смаколики\n"
            "🎁 А ще — приємні сюрпризи!\n\n"
            "Натискай кнопки нижче та поринь у світ, де завжди тепло, смачно й красиво! 💕"
        )
    except TelegramForbiddenError:
        print(f"⚠️ Користувач {message.from_user.id} заблокував бота.")

