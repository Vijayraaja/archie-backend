import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define API scopes
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Path to your JSON key file (make sure to adjust the filename!)
creds = ServiceAccountCredentials.from_json_keyfile_name('archieai-458911-83ba95b8ed88.json', scope)

# Authorize client
client = gspread.authorize(creds)

# Open your Google Sheet by name
sheet = client.open("ArchieSheet").sheet1

# Add a test row
sheet.append_row(["Hello Vijay", "Archie is alive!", "Let's build this."])

print("✅ Test row added to Google Sheet!")
