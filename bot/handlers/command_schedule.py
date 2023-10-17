from aiogram import Router, types
from aiogram.filters import Command

from bot.services import get_schedule

router = Router()


@router.message(Command(commands=["ro"], prefix="!"))
async def command_schedule(message: types.Message) -> None:
    """
    Command !ro to get the schedule

    :param message: The message from Telegram.
    """
    text = get_schedule()
    await message.answer(text=text)
