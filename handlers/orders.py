import re
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.order_fsm import OrderFSM
from services.orders_service import insert_order, get_order_status, update_order_status, get_pending_orders, get_order_details

router = Router()
ADMIN_USER_IDS = [1038982882]  # Ваш Telegram ID

# ... FSM-хендлери (без змін, окрім використання нових функцій)

@router.message(F.text == "/orders")
async def start_order(message: types.Message, state: FSMContext):
    await message.answer("🛍️ Введіть назву товару:")
    await state.set_state(OrderFSM.waiting_for_product_name)

@router.message(OrderFSM.waiting_for_product_name)
async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text.strip()
    if not product_name:
        return await message.answer("❗ Введіть назву товару. Це поле не може бути порожнім.")
    await state.update_data(product_name=product_name)
    await message.answer("📦 Скільки одиниць бажаєте?")
    await state.set_state(OrderFSM.waiting_for_quantity)

@router.message(OrderFSM.waiting_for_quantity)
async def get_quantity(message: types.Message, state: FSMContext):
    quantity = message.text.strip()
    if not quantity.isdigit() or int(quantity) <= 0:
        return await message.answer("❗ Введіть кількість у числовому форматі більше 0.")
    await state.update_data(quantity=int(quantity))
    await message.answer("👤 Введіть ваше ім’я:")
    await state.set_state(OrderFSM.waiting_for_customer_name)

@router.message(OrderFSM.waiting_for_customer_name)
async def get_customer_name(message: types.Message, state: FSMContext):
    customer_name = message.text.strip()
    if not customer_name.replace(" ", "").isalpha():
        return await message.answer("❗ Ім’я повинно складатися тільки з літер та пробілів.")
    await state.update_data(customer_name=customer_name)
    await message.answer("📞 Введіть номер телефону:")
    await state.set_state(OrderFSM.waiting_for_phone_number)

@router.message(OrderFSM.waiting_for_phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text.strip()
    if not re.match(r'^\+?\d{10,15}$', phone_number):
        return await message.answer("❗ Введіть номер у правильному форматі, наприклад: +380XXXXXXXXX")
    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    order_id = await insert_order(data, message.from_user.id)
    await message.answer(
        f"✅ Замовлення на товар: {data['product_name']}, Кількість: {data['quantity']} прийнято! Ваше ID замовлення: {order_id}. Ми з вами зв’яжемося."
    )
    await state.clear()

@router.message(F.text.startswith("/check_status"))
async def check_status(message: types.Message):
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("❗ Формат: /check_status [ID]")
    order_id = parts[1]
    status = await get_order_status(order_id)
    if status:
        await message.answer(f"✅ Статус вашого замовлення з ID {order_id}: {status}.")
    else:
        await message.answer("❗ Замовлення не знайдено.")

def get_status_buttons(order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Підтвердити", callback_data=f"confirm_{order_id}"),
            InlineKeyboardButton(text="❌ Відхилити", callback_data=f"reject_{order_id}")
        ]
    ])

@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_order(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split("_")[1]
    user_id = await update_order_status(order_id, "підтверджено")
    await callback_query.message.answer(f"✅ Замовлення #{order_id} підтверджено!")
    if user_id:
        await callback_query.bot.send_message(
            chat_id=user_id,
            text=f"ℹ️ Статус вашого замовлення #{order_id} оновлено на: підтверджено"
        )

@router.callback_query(lambda c: c.data.startswith("reject_"))
async def reject_order(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split("_")[1]
    user_id = await update_order_status(order_id, "відхилено")
    await callback_query.message.answer(f"❌ Замовлення #{order_id} відхилено!")
    if user_id:
        await callback_query.bot.send_message(
            chat_id=user_id,
            text=f"ℹ️ Статус вашого замовлення #{order_id} оновлено на: відхилено"
        )

@router.message(F.text == "/view_orders")
async def view_orders(message: types.Message):
    if message.from_user.id not in ADMIN_USER_IDS:
        return await message.answer("⛔ У вас немає доступу.")
    orders = await get_pending_orders()
    if orders:
        order_list = "\n".join([f"ID: {o[0]}, Товар: {o[1]}, Статус: {o[2]}" for o in orders])
        await message.answer(f"📝 Замовлення на обробку:\n{order_list}")
    else:
        await message.answer("ℹ️ Немає замовлень на обробку.")

@router.message(F.text.startswith("/manage_order"))
async def manage_single_order(message: types.Message):
    if message.from_user.id not in ADMIN_USER_IDS:
        return await message.answer("⛔ У вас немає доступу.")
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("❗ Формат: /manage_order [ID]")
    order_id = int(parts[1])
    result = await get_order_details(order_id)
    if not result:
        return await message.answer("❗ Замовлення не знайдено.")
    product, quantity, name, phone, status = result
    text = (
        f"📝 Замовлення #{order_id}\n"
        f"👤 Ім’я: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 Товар: {product}\n"
        f"🔢 Кількість: {quantity}\n"
        f"📌 Статус: {status}"
    )
    await message.answer(text, reply_markup=get_status_buttons(order_id))
