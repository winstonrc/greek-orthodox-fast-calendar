# Greek Orthodox Fast Calendar

This tools extracts the calendar events for fasting from the Greek Orthodox Archdiocese of America's [calendar](https://www.goarch.org/chapel/calendar) and creates a new calendar ICS file with only those events.

## Usage

You can retrieve the calendar ICS file from: https://www.goarch.org/chapel/planner.
This tool is only designed to work with the English ICS file.

Run the tool with:

```bash
python main.py <arg>
```

or:

```bash
uv run main.py <arg>
```

A calendar ICS file must be provided using one of the two args below.

### Args

- `--url`: The URL for the ICS file to retrieve and then process.

- `--cal`: The path to the downloaded ICS file to process.

