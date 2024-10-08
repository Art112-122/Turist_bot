from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

class State_Find(StatesGroup):
    city=State()