import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
token = "5985672740:AAGmCPleUSgF8y3pmA2j_Ojcqms14z7hSk8"
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()

b2 = KeyboardButton(text='/Добавить')
b3 = KeyboardButton(text='/Нет')
b4 = KeyboardButton(text='/Да')
b5 = KeyboardButton(text='/Отмена')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pk1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyboard_client.add(b2)
pk.add(b3)
pk.add(b4)
pk1.add(b5)

class FormToEnter(StatesGroup):
    nextphoto=State()
    message1=State()
    time=State()
    media1 = [ ]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Выберите, что вы хотите сделать", reply_markup=keyboard_client)

@dp.message_handler(state=FormToEnter.nextphoto, commands=['Отмена'])
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer('Хорошо, теперь введите сообщение', reply_markup=ReplyKeyboardRemove())
    await FormToEnter.next()

@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Остановлено',reply_markup=keyboard_client)

@dp.message_handler(content_types=['photo'],state=FormToEnter.nextphoto)
async def chat_ser(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['messagable'] = True
    photoSize: PhotoSize = message.photo[-1]
    FormToEnter.media1.append(types.InputMediaPhoto(photoSize.file_id, ''))
    await message.answer('Хорошо, теперь введите следующее',reply_markup=pk1)

@dp.message_handler(state=FormToEnter.message1)
async def chat_ser(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message1'] = message.text
    await FormToEnter.next()
    await message.answer('Теперь временной промежуток(в секундах)')

@dp.message_handler(commands=['Добавить'],state='*')
async def dob(message: types.Message):
    await message.answer('Хорошо, добавить картинки?', reply_markup=pk)

@dp.message_handler(commands=['Да'])
async def dob(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['messagable'] = True
        data['is_running'] = False
        print(data['is_running'])
    await message.answer("Хорошо, добавьте картинку(если этого не требуется, нажмите Отмена)",reply_markup=pk1)
    await FormToEnter.nextphoto.set()

@dp.message_handler(commands=['Нет'])
async def dob(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['messagable'] = False
        data['is_running'] = False
    await FormToEnter.message1.set()
    await message.answer('Хорошо, введите сообщение', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=FormToEnter.time)
async def get_message1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    if data['is_running'] == False:
            await message.reply(text='Готово!')
            async with state.proxy() as data:
                data['is_running'] = True
            if data['messagable'] == True and FormToEnter.media1 != []:
                FormToEnter.media1[-1]['caption'] = data['message1']
                while True:
                    current = await state.get_state()
                    if current != 'FormToEnter:time':
                        break
                    await bot.send_media_group(chat_id=message.chat.id, media=FormToEnter.media1)
                    await asyncio.sleep(int(data['time']))
            else:
                while True:
                    current = await state.get_state()
                    if current != 'FormToEnter:time':
                        break
                    await message.answer(data['message1'])
                    await asyncio.sleep(int(data['time']))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)