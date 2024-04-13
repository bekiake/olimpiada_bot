from aiogram.dispatcher.filters.state import State, StatesGroup

class OlimpicsDataState(StatesGroup):
    code = State()
    true_answers = State()
    start_time = State()
    end_time = State()
    