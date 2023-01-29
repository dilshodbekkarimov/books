from aiogram.dispatcher.filters.state import State, StatesGroup

class StateData(StatesGroup):
	name = State()
	category_id = State()
	description = State()
	muallif = State()
	yili = State()
	narxi = State()
	book = State()
	photo = State()

