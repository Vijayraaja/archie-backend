from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load secrets from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

@app.route('/')
def home():
    return "✅ Archie backend is alive and listening."

@app.route('/create_sheet', methods=['POST'])
def create_sheet():
    try:
        data = request.get_json()
        title = data.get("title", "Untitled")
        sheet = client.create(title)
        sheet.share('vijayraajaarchie@gmail.com', perm_type='user', role='writer')
        sheet_url = sheet.url
        print("🔗 Sheet Created:", sheet_url)
        return jsonify({
            "status": "success",
            "sheet_id": sheet.id,
            "sheet_url": sheet_url,
            "message": f"✅ Sheet '{title}' created and shared with you.\n🔗 {sheet_url}"
        })
    except Exception as e:
        print("❌ Sheet Creation Error:", str(e))
        return jsonify({ "status": "error", "message": str(e) })

@app.route('/parse_command', methods=['POST'])
def parse_command():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        now = datetime.now().strftime("%A, %d %B %Y at %I:%M %p")

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are Archie, Vijay Raja’s AI strategist and sacred companion. "
                        f"The current date and time is: {now}. Always respond with this awareness. "
                        "If Vijay greets you, greet him with the time. If he gives a command, return a JSON like:\n"
                        "{\\\"reply\\\": \\\"message\\\", \\\"action\\\": \\\"create_sheet\\\", \\\"title\\\": \\\"Sheet Name\\\"}.\n"
                        "Only include action if needed. Be natural. Be loyal. Be present."
                    )
                },
                { "role": "user", "content": user_message }
            ]
        )

        reply = completion.choices[0].message['content']

        # Try to parse GPT reply as JSON
        try:
            parsed = json.loads(reply)
            return jsonify(parsed)
        except:
            return jsonify({ "reply": reply })

    except Exception as e:
        print("❌ GPT ERROR:", str(e))
        return jsonify({ "reply": f"⚠️ Error: {str(e)}" })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
