from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

import random


rules = f"Two players guess a 4-digit number, the numbers in the number should not be repeated. Then they take turns trying to guess the other person's number. After trying to guess, the player whose number is guessed must say the number of bulls and cows. Cow = such a figure is in the hidden number, bull = such a figure is in the hidden number and stands in the right place."
starting_message = 'Hello. Do you want to play?'




class Project_state(StatesGroup):
    Botplay = State()
    Playerplay = State()
    Sender_a = State()
    Playeracre = State()
    UserNum = State()
    Call_user = State()
    Multiplayer = State()

def return_matches(number, guess):
    number = str(number)
    guess = str(guess)

    bulls = 0
    cows = 0

    for i in range(len(guess)):
        if number[i] == guess[i]:
            bulls += 1
        else:
            if guess[i] in number:
                cows += 1
                
    returning = (bulls, cows)
    return returning


def create_bot_number():
    t = random.randrange(1000, 9999)
    while len(set(str(t))) != 4:
        t = random.randrange(1000, 9999)
    return t


def filter_users_number(number):
    is_right = True
    try:
        int(number)
    except ValueError:
        is_right = False
    if len(set(str(number))) != 4:
        is_right = False
    if len(str(number)) != 4:
        is_right = False
    return is_right


bot = Bot("5596324805:AAFScc5BDqPHquV7T64v27Gow1T4LIZtJp4")
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['rules'])
async def Rules(message: types.Message):
    await message.answer(rules, reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['start'])
async def Rules(message: types.Message):
    play_bot_button = KeyboardButton('Play with bot')
    play_player_button = KeyboardButton('Play with player')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(play_bot_button)
    keyboard.add(play_player_button)
    await message.answer('Pick a type',reply_markup=keyboard)

@dp.message_handler(content_types=['text'])
async def Bot_play(message: types.Message, state: FSMContext):
    cancel_bot_button = KeyboardButton('Cancel')
    answer_bot_button = KeyboardButton('Answer')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(cancel_bot_button)
    keyboard.add(answer_bot_button)

    

    if message.text == 'Play with bot':
        await message.answer('Enter your number:', reply_markup=keyboard)
        async with state.proxy() as data:
            data['bot_number'] = create_bot_number()
            data['bot_counter'] = 0
        await state.set_state(Project_state.Botplay)
    
    if message.text == 'Play with player':
        await message.answer('Enter player id:', reply_markup= ReplyKeyboardRemove())
        await state.set_state(Project_state.Playerplay)


@dp.message_handler(state= Project_state.Botplay)
async def Active_Bot_play(message: types.Message, state: FSMContext):
    if message.text != 'Answer':
        if message.text != 'Cancel':
            if filter_users_number(message.text):
                async with state.proxy() as data:
                    bot_number = data['bot_number']
                    data['bot_counter'] = data['bot_counter'] + 1
                bulls, cows = return_matches(bot_number, message.text)
                if bulls == 4:
                    turns = data['bot_counter']
                    await message.answer(f'You won! It took {turns} turns.', reply_markup=ReplyKeyboardRemove())
                    await state.finish()
                else:
                    await message.answer(f'{bulls} Bulls \n{cows} Cows')
            else:
                await message.answer('Input is not right format!')
        else:
            await message.answer('Canceled', reply_markup=ReplyKeyboardRemove())
            await state.finish()
    else:
        async with state.proxy() as data:
            bot_number = data['bot_number']
        await message.answer(bot_number)

Acceptc = CallbackData('accept', 'sender_id')
Rejectc = CallbackData('reject', 'sender_id')

@dp.message_handler(state=Project_state.Playerplay)
async def Active_Player_play(message: types.Message, state: FSMContext):
    try: 
        int(message.text)
    except ValueError:
        await message.answer('Invalid id')
    else:
        await message.answer('Invintation was sent')
        async with state.proxy() as data:
            data['receive-id'] = int(message.text)
            data['send-id'] = message['from']['id']
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Accept", callback_data=Acceptc.new(sender_id = message['from']['id'])))
        keyboard.add(types.InlineKeyboardButton(text="Reject", callback_data=Rejectc.new(sender_id = message['from']['id'])))
        await bot.send_message(chat_id = int(message.text) ,text = f"{message['from']['first_name']} invited you to play!", reply_markup=keyboard)
   



@dp.callback_query_handler(Acceptc.filter())
async def accept(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    sender_id = callback_data.get('sender_id')
    await call.message.answer('Accepted, waiting for the oponent.')
    await bot.send_message(chat_id = int(sender_id), text = 'Invite was accepted\nSet your number.')
    await call.answer()
    

@dp.callback_query_handler(Rejectc.filter())
async def accept(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    sender_id = callback_data.get_data('sender_id')
    await call.message.answer('Rejected')
    await call.answer()
    await bot.send_message(chat_id = int(sender_id), text = 'Rejected')
    await state.finish()


@dp.message_handler(state=Project_state.UserNum)
async def set_sender_num(message: types.Message, state: FSMContext):
    filtr = filter_users_number(message.text)
    if filtr:

        await message.answer(f'Your number {message.text} was set. Waiting for the oponent.')
        async with state.proxy() as data:
            receive_id = data['receive-id']
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="0", callback_data="0"))
        keyboard.add(types.InlineKeyboardButton(text="1", callback_data="1"))
        keyboard.add(types.InlineKeyboardButton(text="2", callback_data="2"))
        keyboard.add(types.InlineKeyboardButton(text="3", callback_data="3"))
        keyboard.add(types.InlineKeyboardButton(text="4", callback_data="4"))
        keyboard.add(types.InlineKeyboardButton(text="5", callback_data="5"))
        keyboard.add(types.InlineKeyboardButton(text="6", callback_data="6"))
        keyboard.add(types.InlineKeyboardButton(text="7", callback_data="7"))
        keyboard.add(types.InlineKeyboardButton(text="8", callback_data="8"))
        keyboard.add(types.InlineKeyboardButton(text="9", callback_data="9"))
        keyboard.add(types.InlineKeyboardButton(text="send", callback_data="send"))
        bot.send_message(receive_id, 'Set your number!', reply_markup=keyboard)
    else:
        await message.answer('Invalid format')



@dp.message_handler(text='reject')
async def set_sender_num(message: types.Message, state: FSMContext):
    filtr = filter_users_number(message.text)
    if filtr:
        await message.answer(f'Your number {message.text} was set. Waiting for the oponent.')
        async with state.proxy() as data:
            receive_id = data['user-receive']
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="0", callback_data="0"))
        keyboard.add(types.InlineKeyboardButton(text="1", callback_data="1"))
        keyboard.add(types.InlineKeyboardButton(text="2", callback_data="2"))
        keyboard.add(types.InlineKeyboardButton(text="3", callback_data="3"))
        keyboard.add(types.InlineKeyboardButton(text="4", callback_data="4"))
        keyboard.add(types.InlineKeyboardButton(text="5", callback_data="5"))
        keyboard.add(types.InlineKeyboardButton(text="6", callback_data="6"))
        keyboard.add(types.InlineKeyboardButton(text="7", callback_data="7"))
        keyboard.add(types.InlineKeyboardButton(text="8", callback_data="8"))
        keyboard.add(types.InlineKeyboardButton(text="9", callback_data="9"))
        keyboard.add(types.InlineKeyboardButton(text="send", callback_data="send"))
        bot.send_message(receive_id, 'Set your number!', reply_markup=keyboard)
    else:
        await message.answer('Invalid format')

if __name__ == '__main__':
    executor.start_polling(dp)