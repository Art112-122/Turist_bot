import asyncio
import logging
import sys
from config import BOT_TOKEN as TOKEN
import json

import random
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from command import (
    BOT_START_COMMAND,
    BOT_INTEREST_PLACE,
    INTEREST_PLACE,
    RANDOM_FIND,
    FIND_FOR_CITY,
    BOT_FIND_FOR_CITY,
    BOT_RANDOM_FIND,
)
from keybord import *
from models_bot import Place
from states import State_Find


dp = Dispatcher()


from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy='http://proxy.server:3128')

bot = Bot(token=TOKEN, session=session)




def set_pol(list_to_pol=[1])->list:
    """
    Функція для того щоб залишити тільки унікальні елементи
    """
    lis=set(list_to_pol)
    return list(lis)



def get_json(file_path: str = "places.json", place_id: int or None = None) -> list[dict] or dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        places = json.load(fp)
        if place_id != None and place_id < len(places):
            return places[place_id]
        return places


def get_city(list: str, city: str or None = None) -> list:
    places = list
    cities = []
    indexes = []
    for id, place in enumerate(places):
        cities.append(place.get("city"))
        if place.get("city") == city:
            indexes.append(id)
    if city != None:
        return indexes
    return cities


@dp.message(RANDOM_FIND)
async def random_find(ms: Message) -> None:
    js = get_json()
    place_id = random.randint(0, len(js) - 1)
    place_data = get_json(place_id=place_id)
    place = Place(**place_data)

    text = f"{html.bold('Назва')}: {place.name}\n" \
           f"{html.bold('Місто')}: {place.city}\n" \
           f"{html.bold('Опис')}: {place.description}\n" \
           f"{html.bold('Рейтинг')}: {place.rating}\n" \
           f"{html.bold('Google maps')}: {html.link(value='maps.link', link=place.google)}"

    await ms.answer_photo(caption=text, photo=URLInputFile(place.poster,filename=f"{place.name}_poster.{place.poster.split('.')[-1]}", ))
    await ms.answer(text=f"Несподобався результат?", reply_markup=random_keyboad_markup())


@dp.callback_query(RandomCallback.filter())
async def callb_place(callback: CallbackQuery, callback_data: RandomCallback) -> None:
    js = get_json()
    place_id = random.randint(0, len(js) - 1)
    place_data = get_json(place_id=place_id)
    place = Place(**place_data)

    text = f"{html.bold('Назва')}: {place.name}\n" \
           f"{html.bold('Місто')}: {place.city}\n" \
           f"{html.bold('Опис')}: {place.description}\n" \
           f"{html.bold('Рейтинг')}: {place.rating}\n" \
           f"{html.bold('Google maps')}: {html.link(value='maps.link', link=place.google)}"

    await callback.message.answer_photo(caption=text, photo=URLInputFile(place.poster,filename=f"{place.name}_poster.{place.poster.split('.')[-1]}"))
    await callback.message.answer(text=f"Несподобався результат?", reply_markup=random_keyboad_markup())


@dp.message(FIND_FOR_CITY)
async def city_found(ms: Message, state: FSMContext) -> None:
    await state.set_state(State_Find.city)
    await ms.answer(html.bold('Введіть назву міста:'), reply_markup=ReplyKeyboardRemove())


@dp.message(State_Find.city)
async def city_found(ms: Message, state: FSMContext) -> None:
    sities = get_city(list=get_json())

    if ms.text.capitalize() in sities:
                data = []
                places = get_json()
                ids = get_city(list=places, city=ms.text.capitalize())
                for id in ids:
                    data.append(places[id])
                pl_markup = place_02_keyboad_markup(place_list=data, ids = ids)
                await ms.answer(
                    f"Перелік цікавих місць в місті {ms.text.capitalize()}. Натисніть на назву міста для опису - 🤖",reply_markup=pl_markup)
                await state.clear()
    elif ms.text.lower() == "exit":
                await ms.answer(f"Пошук завершений🔍")
                await state.clear()
    else:
                all_sities=get_city(list=get_json())
                sities_filted=set_pol(all_sities)
                await ms.answer(f'Місто не знайдено, якщо ви хочете закінчити пошук напишіть ("exit")\n\nПерелік усіх міст: \n\n{html.bold(html.italic("\n".join(sities_filted)))}')



@dp.message(INTEREST_PLACE)
async def interest_plase(message: Message) -> None:
    data = get_json()
    pl_markup = place_keyboad_markup(place_list=data)
    await message.answer(f"Перелік усіх цікавих місць. Натисніть на назву міста для опису - 🤖", reply_markup=pl_markup)


@dp.callback_query(PlaceCallback.filter())
async def callback_place(callback: CallbackQuery, callback_data: PlaceCallback) -> None:
    place_id = callback_data.id
    place_data = get_json(place_id=place_id)
    place = Place(**place_data)

    text = f"{html.bold('Назва')}: {place.name}\n" \
           f"{html.bold('Місто')}: {place.city}\n" \
           f"{html.bold('Опис')}: {place.description}\n" \
           f"{html.bold('Рейтинг')}: {place.rating}\n" \
           f"{html.bold('Google maps')}: {html.link(value='maps.link', link=place.google)}"

    await callback.message.answer_photo(caption=text, photo=URLInputFile(place.poster,filename=f"{place.name}_poster.{place.poster.split('.')[-1]}"))


@dp.message(CommandStart)
async def start(message: Message) -> None:
    print(f"INFO:NEW.USER.DETECTED:ID={message.from_user.id}; NAME={message.from_user.full_name}")
    await message.answer(
        f"Вітаю, {html.italic(html.bold(message.from_user.full_name))}!\n"
        f"Я бот якій допоможе знайти цікаві місця для подорожі!\n\n"
        f"Ось перелік моїх команд ({html.bold('ти можеш їх переглянути в меню внизу')}):\n\n"
        f"/start - стартове меню\n"
        f"/places - перелік усіх місць (від найвишого рейтингу)\n"
        f"/find_for_location - Шукати по місту\n"
        f"/random - Випадкове цікаве місце"
    )


@dp.message()
async def message_error(message: Message) -> None:
    await message.answer("Я не вмію читати повідомленя, використовуй команди будь ласка😄!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands([
        BOT_START_COMMAND,
        BOT_INTEREST_PLACE,
        BOT_FIND_FOR_CITY,
        BOT_RANDOM_FIND
    ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
