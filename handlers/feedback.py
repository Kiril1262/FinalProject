from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.feedback import insert_feedback  # Ти створиш цю функцію

router = Router()

# Клас станів FSM
class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()

# Команда /feedback запускає FSM
@router.message(Command("feedback"))
async def feedback_start(message: Message, state: FSMContext):
    await message.answer("Будь ласка, залиште ваш відгук:")
    await state.set_state(FeedbackStates.waiting_for_feedback)

# Отримання тексту відгуку та збереження
@router.message(FeedbackStates.waiting_for_feedback)
async def feedback_received(message: Message, state: FSMContext):
    feedback_text = message.text
    user_id = message.from_user.id

    # Збереження в базу даних
    await insert_feedback(user_id=user_id, feedback_text=feedback_text)

    await message.answer("Дякуємо за ваш відгук!")
    await state.clear()

