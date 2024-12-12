# Greek Orthodox Fast Calendar

This tools extracts the calendar events for fasting from the Greek Orthodox Archdiocese of America's [calendar](https://www.goarch.org/chapel/calendar) and creates a new calendar ICS file with only those events.

## Usage

You can retrieve the calendar ICS file from: https://www.goarch.org/chapel/planner.
This tool is only designed to work with the English ICS file.

### Args

A calendar ICS file must be provided using one of the two args below.

- `--url`: The URL for the ICS file to retrieve and then process.

- `--cal`: The path to the downloaded ICS file to process.

### Setup

You can run the program using either `uv` or `pip`.

#### uv

Run the program:

```bash
uv run main.py <arg>
```

#### pip

First, create a virtual environment:

```bash
python -m venv venv
```

Next, activate the virtual environment, and install the dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Finally, run the program:

```bash
python main.py <arg>
```

