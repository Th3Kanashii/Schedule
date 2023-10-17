import asyncio
import json
import re

from selenium import webdriver
from bs4 import BeautifulSoup


async def parse_schedule(url: str) -> None:
    """
    Parse a class schedule from a given URL and save it as a JSON file.

    :param url: The URL of the schedule page to be parsed.
    """
    # Initialize a WebDriver for Selenium
    driver = webdriver.Firefox()
    driver.get(url)

    # Pause for 1 second to allow the page to load
    await asyncio.sleep(1)

    # Get the page source and quit the driver
    page_source = driver.page_source
    driver.quit()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page_source, features="html.parser")

    # Find all divs with class "col-md-6"
    schedule_divs = soup.find_all(name="div", class_="col-md-6")

    # Create a dictionary to store the schedule data
    schedule_data = {}

    for div in schedule_divs:
        # Extract the date from the h4 tag
        date = div.find("h4").get_text()

        # Find the table containing schedule information
        table = div.find("table")
        pairs_list = []

        # Iterate through table rows to extract schedule details
        for row in table.find_all("tr"):
            cells = row.find_all("td")

            if len(cells) == 3:
                pair = cells[0].get_text()
                period = cells[1].get_text()
                subject_info = cells[2].get_text().replace("\xa0", " ")
                time = f"{period[:5]}-{period[5:]}"

                if subject_info.strip():
                    # Extract link (if any)
                    link_match = re.search(r"http[s]?://[^\s]+", subject_info)
                    link = link_match.group() if link_match else ""

                    # Extract professor (if available)
                    professor_match = re.search(r"\b[А-ЯІЇЄҐ][а-яіїєґ]+ [А-ЯІЇЄҐ]\.[А-ЯІЇЄҐ]\.", subject_info)
                    professor = professor_match.group() if professor_match else ""

                    # Clean the subject information
                    subject_info = re.sub(r"http[s]?://[^\s]+", "", subject_info).strip()
                    subject_info = re.sub(r"\b[А-ЯІЇЄҐ][а-яіїєґ]+ [А-ЯІЇЄҐ]\.[А-ЯІЇЄҐ]\.", "", subject_info).strip()

                    # Create a dictionary for the schedule entry
                    pair_data = {
                        "Пара": pair,
                        "Час": time,
                        "Предмет": subject_info,
                        "Викладач": professor,
                        "Посилання": link
                    }
                    pairs_list.append(pair_data)

        # Add the schedule entry to the dictionary
        if pairs_list:
            schedule_data[date] = pairs_list

    # Save the schedule data as a JSON file
    with open("/home/kanashii/Projects/Notify/schedule.json", "w", encoding="utf-8") as json_file:
        json.dump(schedule_data, json_file, ensure_ascii=False, indent=4)
