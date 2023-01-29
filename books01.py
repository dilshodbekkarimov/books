
import logging
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from baza_book import * 
from buttan import *
from book_token
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

###########################################################################################################################################################









#state uchun importlar
from aiogram.contrib.fsm_storage.memory import  MemoryStorage # vaqtinchalik xotra uchun 
from aiogram.dispatcher import FSMContext #state uchun 
from state import StateData
# from baza_book01 import Database


dp = Dispatcher(bot, storage=MemoryStorage())#vaqtinchalik xotira
db = Database()


db.create_category()
db.create_table_products()



@dp.message_handler(commands="book_add", state="*",user_id=admin)
async def send_welcome(message: types.Message,  state: FSMContext):
    await message.answer("Kitobning nomini kiriting:")
    await state.set_state(StateData.name)
    print(message)


@dp.message_handler(state=StateData.name)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("kitobning nomini matin ko'rinishida kiriting")
        return
    await state.update_data(name=message.text)
    await message.answer("category idsini kiriting: ")
    await StateData.next()

@dp.message_handler(state=StateData.category_id)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await message.answer("category idisini raqam ko'rinishida kiriting")
        return
    await state.update_data(category_id=message.text)
    await message.answer("kitobga tarif bering: ")
    await StateData.next()
    
@dp.message_handler(state=StateData.description)
async def echo(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("kitobning muallifini kiriting: ")
    await StateData.next()




@dp.message_handler(state=StateData.muallif)
async def echo(message: types.Message, state: FSMContext):
    await state.update_data(muallif=message.text)
    await message.answer("kitob chiqqan yilini kiriting ")
    await StateData.next()


@dp.message_handler(state=StateData.yili)
async def echo(message: types.Message, state: FSMContext):
    await state.update_data(yili=message.text)
    await message.answer(" kitobning narxini kiriting: ")
    await StateData.next()



@dp.message_handler(state=StateData.narxi)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await message.answer("kitobning narxini raqam ko'rinishida kiriting")
        return
    await state.update_data(narxi=message.text)
    await message.answer("kitobni /file/  yuboring:  ")
    await StateData.next()



@dp.message_handler(content_types='any', state=StateData.book)
async def echo(message: types.Message, state: FSMContext):
    if message.content_type != "document":
        await message.answer("kitoblarni fayl ko'rinishida joylang")
        return
    # print(message)
    await state.update_data(book=message.document['file_id'])
    await message.answer("kitobning rasimini  kiriting")
    await StateData.next()
    # print(message)



@dp.message_handler(content_types="any", state=StateData.photo)
async def echo(message: types.Message, state: FSMContext):
    if message.content_type != "photo":
        await message.answer("rasimni jpg farmatda kiriting")
    await state.update_data(photo=message.photo[-1]['file_id'])
    print(message.photo[-1]['file_id'])
    data = await state.get_data()
    name_ = data.get("name")
    category_id_ = data.get("category_id")
    description_ = data.get("description")
    muallif_ = data.get("muallif")
    yili_ = data.get("yili")
    narxi_ = data.get("narxi")
    book_ = data.get("book")
    photo_ = data.get("photo")

    db.insert_products(name_,category_id_,description_,muallif_,yili_,narxi_,book_,photo_)



    await state.finish()
    await state.reset_state()
    await message.answer("Ma'lumotlar saqlandi!!!")
    # print(name_,description_,muallif_,yili_,photo_,book_,category_id_)
    await message.answer_photo(photo=photo_,caption=f"kitobning nomi: {name_},\n\nkitobingiz category idsi {category_id_}\n\nkitonga qisqacha tarif: {description_},\n\nkitob {yili_}-yili chiqqan,\nkitobning muallifi: {muallif_}\n\n\nUshbu kitob narxi {narxi_}")
    await message.answer_document(document=book_)

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)









############################################################################################################################################################################################

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("assalomu alaykum\nxo'sh kelibsiz",reply_markup=menu)

@dp.message_handler(text='Kitoblar')
async def send_welcome(message: types.Message):
    markup = await for_catefory_get_all()
    await message.reply("bo'limlardan birini tanlang: ",reply_markup=markup)

@dp.callback_query_handler(Text(startswith="productall_"))
async def send_welcome(call: types.CallbackQuery):
    index = call.data.index("_")
    id = call.data[index+1:]
    products = await get_category_id(id)
    # print('salom',products)
    await call.message.reply("kitoblardan birini tanlang!!!",reply_markup=products)



# @dp.message_handler(content_types="any", state=StateData.photo)
# async def echo(message: types.Message, state: FSMContext):

@dp.callback_query_handler(Text(startswith="products_"))
async def send_welcome(call: types.CallbackQuery):
    index = call.data.index("_")
    id = call.data[index+1:]
    product = db.select_product_id(id)
    print(product)
    await call.message.answer_photo(photo=product[8],caption=f"kitobning nomi: {product[2]},\n\nkitonga qisqacha tarif: {product[3]},\n\nkitob {product[5]}-yili chiqqan,\nkitobning muallifi: {product[4]}\n\n\nUshbu kitob narxi {product[6]}")
    await call.message.answer_document(document=product[7])







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)