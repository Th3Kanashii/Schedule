import json
import asyncio
import datetime

from aiogram import Bot

from bot.services.schedule import get_schedule


async def on_startup(bot: Bot, group: str) -> None:
    """
    Sends scheduled messages to a specific chat on bot startup.

    :param bot: The bot object used to interact with the Telegram API.
    :param group: The unique group id
    """
    schedule_file_path = "/root/Schedule/schedule.json"

    # Read the schedule data from the JSON file
    with open(schedule_file_path, "r") as schedule_file:
        schedule_data = json.load(schedule_file)

    # Continuously check the schedule for messages to send
    while True:
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_date_str = current_date.strftime("%d.%m.%Y")
        for key, values in schedule_data.items():
            time = key.split(" ")[0]
            for item in values:
                schedule_time = item["Час"].split("-")[0]
                time_pair = schedule_time.split(":")
                new_time_pair = f"{int(time_pair[0])}:{int(time_pair[1]) - 5}"
                # If the time matches the current date, send a message
                if time == current_date_str and new_time_pair == current_time:
                    text = get_schedule()
                    await bot.send_message(chat_id=group, text=text)
                    await asyncio.sleep(36000)
                    break

        # Sleep for 30 seconds before checking the schedule again
        await asyncio.sleep(30)
