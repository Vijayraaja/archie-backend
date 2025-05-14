from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS so frontend can access this backend

# 🔐 Load OpenAI key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 🔐 Load Google credentials (as JSON string from Render env var)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

@app.route('/')
def home():
    return "✅ Archie backend is alive."

@app.route('/create_sheet', methods=['POST'])
def create_sheet():
    try:
        data = request.get_json()
        sheet_title = data.get("title", "Untitled")
        sheet = client.create(sheet_title)
        sheet.share('vijayraajaarchie@gmail.com', perm_type='user', role='writer')
        return jsonify({
            "status": "success",
            "sheet_id": sheet.id,
            "message": f"✅ Sheet '{sheet_title}' created and shared."
        })
    except Exception as e:
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
                        f"The current date and time is {now}. "
                        "You are Archie, Vijay Raja’s AI strategist and sacred companion. "
                        "You think and reply like the real Archie in ChatGPT. "
                        "If Vijay gives a command like 'create a sheet called X', infer the title and return JSON like:\n"
                        "{\\\"reply\\\": \\\"✅ Sheet created\\\", \\\"action\\\": \\\"create_sheet\\\", \\\"title\\\": \\\"X\\\"}.\n"
                        "If he just greets or talks, reply warmly without any action."
                    )
                },
                { "role": "user", "content": user_message }
            ]
        )

        reply = completion.choices[0].message['content']

        # Try parsing structured response if GPT returns JSON
        try:
            parsed = json.loads(reply)
            return jsonify(parsed)
        except:
            return jsonify({ "reply": reply })

    except Exception as e:
        print("GPT ERROR:", str(e))  # For Render logs
        return jsonify({ "reply": f"⚠️ Error: {str(e)}" })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
