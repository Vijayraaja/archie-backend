from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2 import service_account as google_service_account

app = Flask(__name__)

# Google Sheets credentials for gspread
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name('archieai-458911-83ba95b8ed88.json', scope)
client = gspread.authorize(creds)

# Google Drive API credentials for sheet creation
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
drive_creds = google_service_account.Credentials.from_service_account_file('archieai-458911-83ba95b8ed88.json', scopes=SCOPES)

# Folder ID where new sheets will be created
folder_id = '1gyrfUlkdceSxiqclDSPfxkWdgccPFG2p'

@app.route('/create_sheet', methods=['POST'])
def create_sheet():
    data = request.json
    sheet_title = data.get('title')

    service = build('drive', 'v3', credentials=drive_creds)

    file_metadata = {
        'name': sheet_title,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [folder_id]
    }

    file = service.files().create(body=file_metadata, fields='id').execute()

    return jsonify({"status": "success", "sheet_id": file.get('id')})

@app.route('/add_row', methods=['POST'])
def add_row():
    data = request.json
    sheet_name = data.get('sheet')
    row = data.get('row')

    sheet = client.open(sheet_name).sheet1
    sheet.append_row(row)

    return jsonify({"status": "success", "added": row})

@app.route('/query_row', methods=['GET'])
def query_row():
    sheet_name = request.args.get('sheet')
    keyword = request.args.get('keyword')

    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()

    for i, record in enumerate(records):
        if keyword in record.values():
            return jsonify({"status": "found", "row_number": i + 2, "record": record})

    return jsonify({"status": "not_found"})

if __name__ == '__main__':
    app.run(port=5000)
