# Low tides web scraper

## Description

A simple web scraper to pull low tide information at the following locations:
* Half Moon Bay, California
* Huntington Beach, California
* Providence, Rhode Island
* Wrightsville Beach, North Carolina
Only low tide instances between sunrise and sunset are pulled. For each location, the height and time of low tide are printed.

## Dependencies

The script is known to run on Python version 3.8.1. Two packages should be installed from PyPI. The `requests` module can be installed via
```bash
python -m pip install requests
```
The `Beautiful Soup` module can be installed via
```bash
python -m pip install beautifulsoup4
```

## Run Instructions

Running the script can be down by running `python` on the `tides.py` script via
```bash
python tides.py
```
