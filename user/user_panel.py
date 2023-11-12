from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from buttons.buttons import buttons_panel, send_category_keyboard, account_info, wallet_info, _send_cups, valid_articul, _send_sweatshirt, _send_others
from registrations.registration import start
from config.base import catalog, get_account_info, change_balance, creating_order

articul_product, name_product, price_product, count_product, category_product, photo_product, Ballance, id_user, plus_money, plus_id = "", "", 0, 0, "", "", 0, "", 0, ""


class AwaitArct(StatesGroup):
    articul = State()
    name_product = State()
    price_product = State()
    count_product = State()
    ctaegory_product = State()
    image_product = State()
    delete = State()
    money = State()
    ID_user = State()
    Send = State()
    await_count_money = State()
    await_count_ID = State()
    await_art = State()


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
async def transfer_from_to(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите сумму перевода')
    await state.set_state(AwaitArct.money)


@router.message(AwaitArct.money)
async def AwaitMoney(message: Message, state: FSMContext):
    global Ballance
    Ballance = message.text
    real_balance = get_account_info(message.from_user.id)[2]
    if int(Ballance) < int(real_balance):
        await message.answer('Введите ID пользователя')
        await state.set_state(AwaitArct.ID_user)
    else:
        await message.answer('Недостаточно средств')
        await state.clear()


@router.message(AwaitArct.ID_user)
async def AwaitSend(message: Message, state: FSMContext):
    global id_user
    id_user = message.text
    await message.answer(f'Вы ввели: {id_user} ')
    await state.set_state(AwaitArct.Send)


@router.message(AwaitArct.Send)
async def AwaitID(message: Message, state: FSMContext):
    try:
        change_balance(message.from_user.id, -int(Ballance))
        change_balance(id_user, int(Ballance))
        await message.answer('Перевод успешно завершён')
        await state.clear()
    except:
        await message.answer(f'Ошибка')
        await state.clear()

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


@router.message(F.text.lower() == 'начислить монет')
async def react_to_upmoney(message: Message, state: FSMContext):
    await message.answer('Введите сумму начисления')
    await state.set_state(AwaitArct.await_count_money)


@router.message(AwaitArct.await_count_money)
async def await_moneyID(message: Message, state: FSMContext):
    global plus_money
    plus_money = message.text
    await message.answer('Введите ID:')
    await state.set_state(AwaitArct.await_count_ID)


@router.message(AwaitArct.await_count_ID)
async def plus_money_f(message: Message, state: FSMContext):
    global plus_id
    plus_id = message.text
    change_balance(plus_id, int(plus_money))
    await message.answer('Начисление завершено')
    await state.clear()


@router.message(F.text.lower() == 'купить товар')
async def try_buy(message: Message, state: FSMContext):
    await message.answer('Введите артикул товара')
    await state.set_state(AwaitArct.await_art)

@router.message(AwaitArct.await_art)
async def accept_buy(message: Message, state: FSMContext):
    global articul_product
    articul_product = message.text
    us_data = get_account_info(message.from_user.id)
    data = get_account_info(message.from_user.id)
    if us_data[2]>data[3]:
        creating_order(data[0], data[1], data[5], data[6], articul_product)
        await message.answer('Заказ создан')
    else:
        await message.answer('Недостаточно средств')
    await state.clear()






