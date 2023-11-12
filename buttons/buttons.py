from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import Message
from config.base import get_account_info, get_root, catalog, delete_product, send_product_from_catalog


"""Раздел обработки кнопок, связанных с каталогом товаров"""


async def buttons_panel(message: Message):
    if get_root(message.from_user.id) == 0:

        kb = [
            [
                types.KeyboardButton(text='Каталог'),
                types.KeyboardButton(text='Аккаунт'),
                types.KeyboardButton(text='Кошелек'),
                types.KeyboardButton(text='Купить товар')
            ],
        ]
        keyboards = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Выберите действие'
        )
    else:
        kb = [
            [
                types.KeyboardButton(text='Каталог'),
                types.KeyboardButton(text='Аккаунт'),
                types.KeyboardButton(text='Кошелек'),
            ],
            [
                types.KeyboardButton(text='Начислить монет'),
                types.KeyboardButton(text='Добавить товар'),
                types.KeyboardButton(text='Удалить товар'),
            ]
        ]
        keyboards = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Выберите действие'
        )

    await message.answer('Куда отправимся?', reply_markup=keyboards)


async def send_category_keyboard(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Кружки", callback_data="кружки"
        ),
        types.InlineKeyboardButton(
            text="Свитшоты", callback_data="свитшоты"
        ),
        types.InlineKeyboardButton(
            text="Прочее", callback_data="прочее"
        )
    )
    await message.answer('Выберите раздел.', reply_markup=builder.as_markup())


async def _send_cups(callback_query, category):
    cups = send_product_from_catalog(category)
    chat_id = callback_query.message.chat.id

    for cup in cups:
        articul, name, price, count, url = cup[2], cup[1], cup[3], cup[4], cup[5]
        response_message = f"Артикул: {articul}\nНазвание: {name}\nЦена: {price}\nКоличество: {count}\n Фото: {url}"
        await callback_query.bot.send_message(chat_id, response_message)

async def _send_sweatshirt(callback_query, category):
    sweatshirt = send_product_from_catalog(category)
    chat_id = callback_query.message.chat.id

    for sweatshirts in sweatshirt:
        articul, name, price, count, url = sweatshirts[2], sweatshirts[1], sweatshirts[3], sweatshirts[4], sweatshirts[5]
        response_message = f"Артикул: {articul}\nНазвание: {name}\nЦена: {price}\nКоличество: {count}\n Фото: {url}"
        await callback_query.bot.send_message(chat_id, response_message)

async def _send_others(callback_query, category):
    others = send_product_from_catalog(category)
    chat_id = callback_query.message.chat.id

    for other in others:
        articul, name, price, count, url = other[2], other[1], other[3], other[4], other[5]
        response_message = f"Артикул: {articul}\nНазвание: {name}\nЦена: {price}\nКоличество: {count}\n Фото: {url}"
        await callback_query.bot.send_message(chat_id, response_message)
async def valid_articul(message):
    articul = message.text
    print(articul)
    result = delete_product(articul)

    if result == 'deleted':
        await message.answer('Товар успешно удален')
    elif result == 'not_found':
        await message.answer('Товар не найден')


"""Раздел обработки аккаунта"""


async def account_info(message: Message):
    account_info = get_account_info(message.from_user.id)
    name, age, number, address = account_info[1], account_info[3], account_info[4], account_info[5]

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
            text='Изменить', callback_data='Change')
    )
    text = f"ID: {message.from_user.id}\nИмя: {name}\nВозраст: {age}\nНомер телефона: {number}\nАдрес: {address}"

    await message.answer(text, reply_markup=builder.as_markup())


"""раздел обработки кнопки кошелька"""


async def wallet_info(message: Message):
    account_info = get_account_info(message.from_user.id)
    ballance = account_info[2]

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text='Перевести другому пользователю', callback_data='Transfer'
        ))
    text = f"Ваш баланс: {ballance}"
    await message.answer(text, reply_markup=builder.as_markup())


