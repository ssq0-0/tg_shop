import re
from aiogram import Router
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


router = Router()


class AwaitNext(StatesGroup):
    input_name_and_subname = State()
    input_age = State()
    input_number = State()
    input_address = State()


@router.message(Command('start'))
async def start(message: Message, state:FSMContext):
    await message.answer(text='Введите имя и фамилию')
    await state.set_state(AwaitNext.input_name_and_subname)


@router.message(AwaitNext.input_name_and_subname)
async def _name_input(message: Message, state: FSMContext):
    name = message.text

    if not is_russian_name(name):
        await message.answer('Введите имя на латинице.')
    else:
        await state.update_data(input_name_and_subname=message.text.lower())
        await message.answer(text='Теперь введите возраст.')
        await state.set_state(AwaitNext.input_age)


@router.message(AwaitNext.input_age)
async def _age_input(message: Message, state: FSMContext):
    await state.update_data(input_age=message.text)

    if int(message.text) > 80:
        await message.answer('Меньше шуток, назовите свой настоящий возраст.')
    else:
        await message.answer('Введте номер телефона начиная с "8".')
        await state.set_state(AwaitNext.input_number)


@router.message(AwaitNext.input_number)
async def _number_input(message: Message, state: FSMContext):
    number = message.text

    if not is_real_number(number):
        await message.answer('Введите реальный номер телефона начиная с "8".')
    else:
        await state.update_data(input_number=message.text)
        await message.answer('Введите адрес проживания/доставки.')
        await state.set_state(AwaitNext.input_address)


@router.message(AwaitNext.input_address)
async def _address_input(message: Message, state: FSMContext):
    address = message.text

    if not is_real_address(address):
        await message.answer('Введите адрес на латинице.')
    else:
        await state.update_data(input_address=message.text)
        await message.answer('Информация принята, спасибо!')
        await state.clear()


# Чек на легит нейм/адрес/номер. !ВАЖНО! Нет проверки существует ли такое имя/адрес/номер, проверяется только язык

def is_russian_name(name):
    pattern = re.compile(r'^[а-яА-ЯёЁ\s]+$')
    return bool(pattern.match(name))


def is_real_number(number):
    pattern = re.compile(r'^8[ \-]?(\d[ \-]?){10}$')
    return bool(pattern.match(number))


def is_real_address(address):
    pattern = re.compile(r'^[а-яА-ЯёЁ\s]+$')
    return bool(pattern.match(address))
