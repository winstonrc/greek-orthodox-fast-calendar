import argparse
import os
import re
import sys
from urllib.parse import urlparse

import requests
from ics import Calendar

DATA_FILE_PATH = "data/"

parser = argparse.ArgumentParser(description="Extract the fasting events from the\
Greek Orthodox Planner calendar.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--url', type=str, help="The URL of the calendar to fetch.")
group.add_argument('--cal', type=str, help="The file of the calendar to process.")


def download_calendar(url: str) -> str | None:
    parsed_url = urlparse(url)
    # Find the segment of the url ending with .ics
    ics_segments = [segment for segment in parsed_url.path.split('/') 
        if segment.endswith('.ics')]

    if ics_segments:
        file_name = os.path.basename(ics_segments[0])
    else:
        print("Error retrieving the .ics for the provided URL.")
        return None

    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    calendar_file_path = os.path.join(DATA_FILE_PATH, file_name)

    # Request the file if it is not downloaded
    if not os.path.exists(calendar_file_path):
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(calendar_file_path, 'wb') as file:
                file.write(response.content)
                print(f"File downloaded from provided URL & saved to: {calendar_file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download file at the provided URL: {e}")
            return None
    else:
        print(f"The file already exists at {calendar_file_path}. Skipping download.")

    return calendar_file_path


def process_calendar(calendar_file_path: str):
    fast_types = {
        "Strict Fast": "Refrain from meat, fish, oil, wine, dairy, and eggs.",
        "Fast Day (Wine and Oil Allowed)": "Wine and oil are allowed.\nRefrain from meat, fish, dairy, and eggs.",
        "Fast Day (Fish Allowed)": "Refrain from meat, dairy and eggs.",
        "Fast Day (Dairy, Eggs, and Fish Allowed)": "Dairy, eggs, fish, oil and wine are allowed.\nRefrain from meat."
    }

    output_file_name = "greek-orthodox-fast"
    year_pattern = r'\d{4}'
    match = re.search(year_pattern, calendar_file_path)
    if match:
        calendar_year = match.group(0)
        output_file_name = f"{output_file_name}-{calendar_year}"

    output_file_path = os.path.join(DATA_FILE_PATH, f"{output_file_name}-en.ics")

    c = Calendar()

    # Parse the old calendar for fast events
    with open(calendar_file_path, 'rb') as file:
        calendar_data = file.read().decode('utf-8')
        calendar = Calendar(calendar_data)

        for event in calendar.timeline:
            if "Fast" in event.description:
                for fast_type, description in fast_types.items():
                    if fast_type in event.description:
                        fast_type_emoji = ""
                        match fast_type:
                            case "Strict Fast":
                                fast_type_emoji = "🚫"
                            case "Fast Day (Wine and Oil Allowed)":
                                fast_type_emoji = "🍇"
                            case "Fast Day (Fish Allowed)":
                                fast_type_emoji = "🐟"
                            case "Fast Day (Dairy, Eggs, and Fish Allowed)":
                                fast_type_emoji = "🧀"

                        event.name = f"{fast_type_emoji} {fast_type}"
                        event.description = description
                        c.events.add(event)

    print(f"{len(c.events)} events extracted.")
    # Save the new calendar
    with open(output_file_path, 'w') as file:
        # Write headers
        file.write("BEGIN:VCALENDAR\n")
        file.write("VERSION:2.0\n")

        for event in c.timeline:
            file.write(event.serialize())
            file.write("\n")

        # Write footer
        file.write("END:VCALENDAR\n")
        print(f"New calendar saved to: {output_file_path}")


if __name__ == "__main__":
    args = parser.parse_args()

    calendar_file_path = ""
    if args.url:
        calendar_file_path = download_calendar(args.url)
    elif args.cal:
        calendar_file_path = args.cal
    else:
        print("Error: Missing a required arg. Provide either a url or a calendar file.")
        sys.exit()

    if calendar_file_path:
        process_calendar(calendar_file_path)
    else:
        print("Error: Improper calendar_file_path.")
        sys.exit()

