from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("contact"))
async def cmd_contact(message: types.Message):
    await message.answer(
        "📞 *Контакт із розробником бота*\n\n"
        "Якщо у вас виникли питання, пропозиції або потрібна допомога — "
        "звертайтеся напряму будь-яким зручним способом:\n\n"
        "👤 *Ім’я розробника:* Кіріл Капнік\n"
        "🧑‍💻 *Посада:* Розробник Telegram-ботів / Python-розробник\n"
        "🔹 *Telegram:* [@good_man17_17](https://t.me/good_man17_17)\n"
        "📧 *Email:* kapnikkiril0@gmail.com\n"
        "🌐 *Вебсайт:* https://example.com\n"
        "📍 *Місто:* Житомир, Україна\n\n"
        "⏰ *Час для зв’язку:* Пн-Пт з 10:00 до 18:00\n\n"
        "Ми завжди поруч, щоб зробити ваш досвід ще солодшим! 🍬"
    )
