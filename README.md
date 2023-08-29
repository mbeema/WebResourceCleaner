

# Web Crawler for Identifying Unused JavaScript and CSS

## Overview

This project aims to crawl a website to identify unused JavaScript functions and CSS classes. It uses Selenium for web scraping and BeautifulSoup for HTML parsing.

## Author

- Madhukar Beema, DevOps Consultant

## Prerequisites

- Python 3.x
- Selenium
- BeautifulSoup
- ChromeDriver

## Installation

1. **Clone the Repository**

    ```
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. **Navigate to the Directory**

    ```
    cd yourrepository
    ```

3. **Install Required Python Packages**

    ```
    pip install -r requirements.txt
    ```

4. **Download ChromeDriver**

    Download the appropriate version of ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in a directory that's in your system's PATH.

## Usage

### Command Line Arguments

- `--url`: The URL of the website to crawl. (Required)
- `--exclude`: List of URLs to exclude from crawling. (Optional)

### Run the Script

```
python web_crawler.py --url https://example.com --exclude https://example.com/account https://example.com/checkout
```

### Jenkins Setup

1. Create a new Jenkins job.
2. In the "Build" section, add a shell or Python script build step.
3. Add the script or command to run your web crawler.
4. Optionally, set the `DISPLAY` environment variable if running on a Linux machine without a display (`export DISPLAY=:0`).

## Output

The script will generate a report listing all unused JavaScript functions and CSS classes.

## Troubleshooting

If you encounter issues with ChromeDriver, make sure that its version is compatible with the installed Chrome version. Also, ensure that you have set the `DISPLAY` environment variable if running on a Linux machine without a display.
