# Website Scraper and Resource Downloader

## Description

This Python script is a powerful website scraper that not only downloads the HTML content of a given webpage but also fetches all associated resources such as images, stylesheets, scripts, and other linked files. It's designed to create a local copy of a website, making it useful for archiving, offline viewing, or analysis purposes.

## Features

- Downloads the main HTML content of a specified URL
- Recursively downloads all linked resources (images, CSS, JavaScript, etc.)
- Updates HTML links to point to local resources
- Handles various HTML tags and attributes (a, img, script, link, etc.)
- Processes inline styles and `<style>` tags to download referenced resources
- Organizes downloaded files into subfolders based on their type
- Uses content hashing to avoid duplicate downloads
- Provides a progress bar for better user experience
- Handles relative and absolute URLs

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4
  - tqdm

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/website-scraper.git
   cd website-scraper
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line, providing the URL of the website you want to scrape:

```
python website_scraper.py https://example.com
```

Replace `https://example.com` with the URL of the website you wish