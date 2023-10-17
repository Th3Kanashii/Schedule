import json
import datetime


def get_schedule() -> str:
    """
    Read a schedule from a JSON file and return a formatted text for the current date.

    :return: A formatted text containing the schedule for the current date, or a message indicating it's a day off.
    """
    schedule_file_path = "/home/kanashii/Projects/Notify/schedule.json"

    # Open the JSON file with the schedule.
    with open(schedule_file_path, "r") as schedule_file:
        schedule_data = json.load(schedule_file)

    # Get the current date and day of the week.
    current_date = datetime.date.today()
    current_day_of_week = current_date.weekday()
    days_of_week = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]

    current_date_str = current_date.strftime("%d.%m.%Y")
    current_day = days_of_week[current_day_of_week]

    # Initialize the schedule text.
    schedule_text = f"Розклад на {current_date_str} ({current_day}) 📆\n<b>ІПЗМ-1</b>\n\n"
    found_today = False

    # Iterate through the schedule data to find entries for the current date.
    for date_key, schedule_entries in schedule_data.items():
        date_parts = date_key.split(" ")
        if date_parts[0] == current_date_str:
            found_today = True
            for item in schedule_entries:
                schedule_text += f"<b>{item['Пара']} Пара ⏰{item['Час']}</b>\n"
                schedule_text += f"{item['Предмет']}\n{item['Викладач']}\n{item['Посилання']}\n\n"

    # If no schedule entries were found for today, indicate it's a day off.
    if not found_today:
        schedule_text = "Сьогодні вихідний"

    return schedule_text
