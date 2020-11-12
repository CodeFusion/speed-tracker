# Speed Tracker
Check and save the results of a speed test

## Dependencies
- speedtest-cli
- aiohttp
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- python-dotenv

Run `setup.py` to install all dependencies

## Setup
- Create a Google Sheet 
  - Columns are Date, Latency, Download, Upload
  - Copy the ID in the URL
- Create a new project with the Google Sheets API