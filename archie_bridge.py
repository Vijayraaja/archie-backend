from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Load credentials from Render environment variable
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

@app.route('/')
def home():
    return "Archie is alive and connected to Google Sheets!", 200

@app.route('/create_sheet', methods=['POST'])
def create_sheet():
    try:
        data = request.get_json()
        sheet_title = data.get("title", "Untitled")

        sheet = client.create(sheet_title)
        return jsonify({
            "status": "success",
            "sheet_id": sheet.id
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
