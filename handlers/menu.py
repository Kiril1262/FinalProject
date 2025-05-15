from aiogram import Router, types
from aiogram.filters import Command

router = Router()

# список ID адміністраторів
ADMIN_USER_IDS = [1038982882]  # заміни на свої ID

@router.message(Command("menu"))
async def show_menu(message: types.Message):
    is_admin = message.from_user.id in ADMIN_USER_IDS

    base_menu = """
📋 <b>Меню команд</b>

👤 <b>Для користувача:</b>
/start — запустити бота
/orders — оформити нове замовлення
/check_status [ID] — перевірити статус замовлення
/feedback — залишити відгук
/menu — переглянути це меню
"""

    admin_menu = """
🛠️ <b>Команди для адміністратора:</b>
/view_orders — переглянути всі замовлення
/manage_order [ID] — підтвердити або відхилити замовлення
/admin_add_product — додати товар до каталогу
"""

    full_menu = base_menu
    if is_admin:
        full_menu += admin_menu

    await message.answer(full_menu, parse_mode="HTML")
