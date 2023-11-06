from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import Message

"""Раздел обработки кнопок, связанных с каталогом товаров"""
async def buttons_panel(message: Message):
    kb = [
        [
            types.KeyboardButton(text='Каталог'),
            types.KeyboardButton(text='Аккаунт'),
            types.KeyboardButton(text='Кошелек')
        ],
    ]
    keyboards = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие'
    )
    await message.answer('Куда отправимся?', reply_markup=keyboards)


async def send_catalog_keyboard(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Кружки", callback_data="Cups"
        ),
        types.InlineKeyboardButton(
            text="Свитшоты", callback_data="Sweatshirt"
        ),
        types.InlineKeyboardButton(
            text="Прочее", callback_data="Others"
        )
    )
    await message.answer('Выберите раздел.', reply_markup=builder.as_markup())


"""Раздел обработки аккаунта"""


async def account_info(message: Message):
    account = {
        'Имя': 'Тут',
        'Возраст': 'пока что',
        'Номер телефона': 'ничего',
        'Адрес': 'нет',
    }
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
            text='Изменить', callback_data='Change')
    )
    account_text = "\n".join([f"{key}: {value}" for key, value in account.items()])

    await message.answer(account_text, reply_markup=builder.as_markup())


"""раздел обработки кнопки кошелька"""

async def wallet_info(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text='Перевести другому пользователю', callback_data='Transfer'
        ))

    await message.answer('пока ничего нет', reply_markup=builder.as_markup())


