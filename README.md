# NBA Stats Scraper

This Python script scrapes player statlines from the ESPN website using Selenium and writes the data to an Excel file.

## Setup Instructions

1. **Clone this repository** or download the files.

2. **Create a virtual environment**:

    ``` python3 -m venv venv```

3. **Activate the environment**:

    - On Windows:
      ```venv\Scripts\activate```
    - On macOS/Linux:
      ```source venv/bin/activate```

4. **Install dependencies**:

    ```pip install -r requirements.txt```

5. **Run the script**:

    ```python3 NBA_Stats_Scraper.py```

6. **Exit the virtual environment**:

    ```deactivate```

## Requirements

- Python 3.11+
- Google Chrome (for Selenium)
- ChromeDriver

## Notes

- Make sure you download the correct version of [ChromeDriver](https://sites.google.com/chromium.org/driver/) that matches your installed Chrome browser.
- You may need to adjust the target URL or parsing logic based on the website's structure.
