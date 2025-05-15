from aiogram.fsm.state import State, StatesGroup

class OrderFSM(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_quantity = State()
    waiting_for_customer_name = State()
    waiting_for_phone_number = State()
