from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

INTEREST_PLACE = Command("places")
FIND_FOR_CITY = Command("find_for_location")
RANDOM_FIND = Command("random")

BOT_INTEREST_PLACE=BotCommand(command="places",description="Перелік усіх цікавих місць")
BOT_START_COMMAND=BotCommand(command="start",description="Стартове меню")
BOT_FIND_FOR_CITY=BotCommand(command="find_for_location",description="Шукати по місту")
BOT_RANDOM_FIND=BotCommand(command="random", description="Випадкове цікаве місце")