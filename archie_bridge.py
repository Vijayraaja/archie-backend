from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

@app.route('/')
def home():
    return "Archie is alive and connected!", 200

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

# === BIND TO 0.0.0.0 FOR RENDER ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
