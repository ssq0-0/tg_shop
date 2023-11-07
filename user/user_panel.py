from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from buttons.buttons import buttons_panel, send_category_keyboard, account_info, wallet_info, _send_cups, valid_articul
from registrations.registration import start

class AwaitArct(StatesGroup):
    articul = State()

router = Router()


@router.message(Command('menu'))
async def react_to_menu(message: Message):
    await buttons_panel(message)


@router.message(F.text == 'Каталог')
async def send_catalog(message: Message):
    await send_category_keyboard(message)


@router.callback_query(F.data == 'Cups')
async def cup_catalog(callback: types.CallbackQuery):
    await _send_cups()


@router.callback_query(F.data == 'Sweatshirt')
async def sweatshirt_ctalog(callback: types.CallbackQuery):
    await callback.message.answer('Вы выбрали свитшоты')


@router.callback_query(F.data == 'Others')
async def others_catalog(callback: types.CallbackQuery):
    await callback.message.answer('Вы выбрали прочее')


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


@router.message(F.text == 'Удалить товар')
async def pre_delete_product_from_catalog(message: Message, state: FSMContext):
    await message.answer('Напишите артикул удаляемого товара')
    await state.set_state(AwaitArct.articul)


@router.message(AwaitArct.articul)
async def _delete_product_from_catalog(message: Message, state: FSMContext):
    articul = message
    await state.clear()
    await valid_articul(articul)

