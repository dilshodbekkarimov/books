from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from books01 import db 
from baza_book import Database
#oddiy usul 


menu = ReplyKeyboardMarkup(
	keyboard = [
					[
						KeyboardButton(text="Kitoblar"),
						KeyboardButton(text="Qidirish"),
					],
					[
						KeyboardButton(text="Aloqa"),
					],
				],
	resize_keyboard=True
)


#tsikl

async def for_catefory_get_all():
	x = db.select_category_all()
	categories = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		# print('ebee',i)
		button_text = i[1]
		callback_data = i[0]
		categories.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"productall_{callback_data}")
				)
	return categories

async def get_category_id(id):
	x = db.select_products_for_category_id(id)
	# print('assalom,',x)
	products = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		# print('vaaaaa',products)
		button_text = i[3]
		callback_data = i[0]
		products.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"products_{callback_data}")
				)
	return products