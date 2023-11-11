import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4
import requests # pip install requests
# project imports
from config import TOKEN
from keyboards.admin_kb import main_keyboard, second_keyboard
from database.sqlite_db import add_to_db, read_db, start_database, del_from_db

# project variables
storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)

# global variable
ID = None


# finite state machine class
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    descr = State()
    price = State()


# start func
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=main_keyboard)

# 'Program languages' block
@dp.message(Command('Progr_lang-s'))
async def second_keyboard_show(message: Message):
    await message.answer('Ok', reply_markup=second_keyboard)

@dp.message(Command('Python'))
async def python_read(message: Message):
    with open('database/python.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=second_keyboard)

@dp.message(Command('C++'))
async def python_read(message: Message):
    with open('database/cpp.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=second_keyboard)

@dp.message(Command('PHP'))
async def python_read(message: Message):
    with open('database/php.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=second_keyboard)

@dp.message(Command('Java'))
async def python_read(message: Message):
    with open('database/java.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=second_keyboard)

@dp.message(Command('<Back'))
async def python_read(message: Message):
    await message.answer('Ok', reply_markup=main_keyboard)

# send document func
@dp.message(Command('Read_me_doc'))
async def send_readme_doc(message: Message):
    file = FSInputFile('database/readme.txt')
    await bot.send_document(document=file, chat_id=message.from_user.id)

# parse func
@dp.message(Command('Show_info'))
async def parse_web_func(message: Message):
    headers_for_parse = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"
    }
    url = 'https://privatbank.ua/rates-archive'
    parse_url = requests.get(url, headers=headers_for_parse)
    result = bs(parse_url.text, 'html.parser')
    val_names = result.findAll("div", class_="currency-pairs")
    values = []
    for i in val_names[:5]:
        chars = ['\n', ' ']
        vlt = i.find("div", class_="names")
        vlt = vlt.text
        vlt = vlt.translate(str.maketrans('','',''.join(chars)))

        purchase = i.find("div", class_="purchase")
        purchase = purchase.text
        purchase = purchase.translate(str.maketrans('', '', ''.join(chars)))

        sale = i.find("div", class_="sale")
        sale = sale.text
        sale = sale.translate(str.maketrans('', '', ''.join(chars)))

        mess = (f'{vlt[:3]}-{vlt[3:]} - PURCASE: {purchase} | SALE: {sale}\n')
        values.append(mess)
    values_str = ''.join(values)
    await message.answer(values_str, reply_markup=main_keyboard)

# Finite State Machine block
@dp.message(Command('Download'))
async def cm_start(message: Message, state: FSMContext):
    global ID
    ID = message.from_user.id
    await state.set_state(FSMAdmin.photo)
    #await FSMAdmin.photo.set()
    await message.answer('Загрузи фото \n\nЯкщо хочете припинити ввід даних - скористайтесь командою /Cancel')


@dp.message(Command('Cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.clear()
        await message.answer('Введення даних припинено')

@dp.message(FSMAdmin.photo)
async def load_photo(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(photo=message.photo[0].file_id) # message.text
        await state.set_state(FSMAdmin.name)
        await message.answer('Введи назву')

@dp.message(FSMAdmin.name)
async def load_name(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(name=message.text)
        await state.set_state(FSMAdmin.descr)
        await message.answer('Введи опис')

@dp.message(FSMAdmin.descr)
async def load_name(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(descr=message.text)
        await state.set_state(FSMAdmin.price)
        await message.answer('Введи ціну')

@dp.message(FSMAdmin.price)
async def load_name(message: Message, state: FSMContext):
    if message.from_user.id == ID:
        await state.update_data(price=message.text)
        data = await state.get_data()
        add_to_db(data)
        await state.clear()
        await message.answer('Введення даних завершено')

# func for show data from DB
@dp.message(Command('Show_goods'))
async def show_data_from_db(message: Message):
    info_db = read_db()
    for i in info_db:
        await message.answer_photo(i[0],
                             f'Назва: {i[1]}\n'
                             f'Опис: {i[2]}\n'
                             f'Ціна: {i[3]}')

@dp.message(Command('Delete'))
async def delete(message: Message):
    info_db = read_db()
    for i in info_db:
        await message.answer_photo(i[0],
                             f'Назва: {i[1]}\n')
        builder_inline = InlineKeyboardBuilder()
        builder_inline.add(types.InlineKeyboardButton(text='Видалити', callback_data=f'del {i[1]}'))
        await message.answer('^^^', reply_markup=builder_inline.as_markup())


@dp.callback_query(F.data.startswith("del"))
async def delete_item_from_db(callback: types.CallbackQuery):
    query = (callback.data.split(' ')[1],)
    del_from_db(query)
    await callback.answer(f'"{query}" deleted')


# echo message func
@dp.message()
async def echo_function(message: Message):
    await message.answer(message.text)


# func start bot
async def main():
    print('BOT online')
    start_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


