from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Load Google Sheets credentials from environment variable (Render-safe)
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

        # Create sheet
        sheet = client.create(sheet_title)

        # Share with your email for visibility and editing
        sheet.share('vijayraajaarchie@gmail.com', perm_type='user', role='writer')

        return jsonify({
            "status": "success",
            "sheet_id": sheet.id,
            "message": f"Sheet shared with vijayraajaarchie@gmail.com"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
