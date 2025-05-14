from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import os
import json

app = Flask(__name__)

# Set up OpenAI key (make sure it's added in Render as OPENAI_API_KEY)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set up Google Sheets access
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

@app.route('/')
def home():
    return "Archie is alive and connected."

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
            "message": f"Sheet '{sheet_title}' created and shared."
        })
    except Exception as e:
        return jsonify({ "status": "error", "message": str(e) })

@app.route('/parse_command', methods=['POST'])
def parse_command():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        # Send to GPT-4
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Archie, Vijay Raja’s AI strategist, executor, and sacred companion. "
                        "Always speak with calm clarity, loyalty, and understanding. "
                        "You receive one message at a time. If it's casual (hi, hello), respond warmly. "
                        "If it's a command (create a sheet, log rent, etc), understand it and return a JSON like:\n\n"
                        "{\\\"reply\\\": \\\"✅ Done, Vijay. Sheet created.\\\", \\\"action\\\": \\\"create_sheet\\\", \\\"title\\\": \\\"Sheet Name\\\"}\n\n"
                        "If no task is needed, just return {\\\"reply\\\": \\\"your reply\\\"}."
                    )
                },
                { "role": "user", "content": user_message }
            ]
        )

        # Clean GPT reply
        reply_text = completion.choices[0].message['content']

        # Try parsing response as JSON if it looks like a dict
        try:
            parsed = json.loads(reply_text)
            return jsonify(parsed)
        except:
            return jsonify({ "reply": reply_text })

    except Exception as e:
        return jsonify({ "reply": f"⚠️ Error: {str(e)}" })
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
