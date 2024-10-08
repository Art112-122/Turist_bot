from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class PlaceCallback(CallbackData, prefix="place",sep=";"):
    id: int
    name: str

def place_keyboad_markup(place_list:list[dict], offset:int|None = None, skip:int|None = None):
    bilder=InlineKeyboardBuilder()
    for index, place_data in enumerate(place_list):
        callback_data = PlaceCallback(id=index, **place_data)
        bilder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    bilder.adjust(1, repeat=True)
    return bilder.as_markup()



def place_02_keyboad_markup(place_list:list[dict],ids:list ,offset:int|None = None, skip:int|None = None):
    bilder=InlineKeyboardBuilder()
    for index in range(len(place_list)):
        callback_data = PlaceCallback(id=ids[index], **place_list[index])
        bilder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    bilder.adjust(1, repeat=True)
    return bilder.as_markup()





class RandomCallback(CallbackData, prefix="random",sep=";"):
    command:str

def random_keyboad_markup(offset:int|None = None, skip:int|None = None):
    callback_random=RandomCallback(command="random")
    bilder=InlineKeyboardBuilder()
    bilder.button(
            text=f"Спробувати ще раз",
            callback_data=callback_random.pack()
    )
    bilder.adjust(1, repeat=True)
    return bilder.as_markup()


