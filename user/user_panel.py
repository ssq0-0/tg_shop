from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from buttons.buttons import buttons_panel, send_category_keyboard, account_info, wallet_info, _send_cups, valid_articul, _send_sweatshirt, _send_others
from registrations.registration import start
from config.base import catalog

articul_product, name_product, price_product, count_product, category_product, photo_product = "", "", 0, 0, "", ""


class AwaitArct(StatesGroup):
    articul = State()
    name_product = State()
    price_product = State()
    count_product = State()
    ctaegory_product = State()
    image_product = State()
    delete = State()


router = Router()


@router.message(Command('menu'))
async def react_to_menu(message: Message):
    await buttons_panel(message)


@router.message(F.text == 'Каталог')
async def send_catalog(message: Message):
    await send_category_keyboard(message)


@router.callback_query(F.data == 'кружки')
async def cup_catalog(callback: types.CallbackQuery):
    await _send_cups(callback, category='кружки')


@router.callback_query(F.data == 'свитшоты')
async def sweatshirt_ctalog(callback: types.CallbackQuery):
    await _send_sweatshirt(callback, category='свитшоты')


@router.callback_query(F.data == 'прочее')
async def others_catalog(callback: types.CallbackQuery):
    await _send_others(callback, category='прочее')


@router.message(F.text == 'Аккаунт')
async def print_account_info(message: Message):
    await account_info(message)


@router.callback_query(F.data == 'Change')
async def change_user_info(callback: types.CallbackQuery, state: FSMContext):
    await start(callback.message, state)


@router.message(F.text == 'Кошелек')
async def print_wallet_info(message: Message):
    await wallet_info(message)


@router.callback_query(F.data == 'Transfer')
async def transfer_from_to(callback: types.CallbackQuery):
    await callback.message.answer('Трансфера потом')


@router.message(F.text == 'Добавить товар')
async def append_product(message: Message, state: FSMContext):
    await message.answer('Введите артикул товара')
    await state.set_state(AwaitArct.articul)


@router.message(AwaitArct.articul)
async def _input_arcticul(message: Message, state: FSMContext):
    global articul_product
    articul_product = message.text
    await message.answer('Введите название товара')
    await state.set_state(AwaitArct.name_product)


@router.message(AwaitArct.name_product)
async def _input_name_product(message: Message, state: FSMContext):
    global name_product
    name_product = message.text
    await message.answer('Введите цену товара')
    await state.set_state(AwaitArct.price_product)


@router.message(AwaitArct.price_product)
async def _input_price_product(message: Message, state: FSMContext):
    global price_product
    price_product = message.text
    await message.answer('Введите количество товара')
    await state.set_state(AwaitArct.count_product)


@router.message(AwaitArct.count_product)
async def _input_count_price(message: Message, state: FSMContext):
    global count_product
    count_product = message.text
    await message.answer('Введите категорию товара')
    await state.set_state(AwaitArct.ctaegory_product)


@router.message(AwaitArct.ctaegory_product)
async def _input_category_product(message: Message, state: FSMContext):
    global category_product
    category_product = message.text
    await message.answer('Отправьте фотографию товара')
    await state.set_state(AwaitArct.image_product)


@router.message(AwaitArct.image_product)
async def _send_image(message: Message, state: FSMContext):
    url_link = message.text
    catalog(articul_product, category_product, price_product, count_product, name_product, url_link)
    await message.answer('Товар добавлен')
    await state.clear()


@router.message(F.text == 'Удалить товар')
async def react_to_delete(message: Message, state: FSMContext):
    await message.answer('Напишите артикул удаляемого товара')
    await state.set_state(AwaitArct.delete)


@router.message(AwaitArct.delete)
async def _delete_product_from_catalog(message: Message, state: FSMContext):
    articul_product = message
    await state.clear()
    await valid_articul(articul_product)

