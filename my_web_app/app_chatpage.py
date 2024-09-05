from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import uuid
import bcrypt
import requests
import os


app = Flask(__name__)


# Cotomi APIの設定
COTOMI_API_URL = "https://api.cotomi.com/v1/chat/completions"
COTOMI_API_KEY = os.environ.get('COTOMI_API_KEY')  # 環境変数に設定してるものをとってきてる
GROUP_ID = os.environ.get('GROUP_ID')
TENANT_ID = os.environ.get('TENANT_ID')

key = "Bearer " + COTOMI_API_KEY

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data['message']

    # Cotomiとのやり取り
    try:
        # Cotomi APIを呼び出す
        headers = {
            "Content-Type": "application/json",
            "Authorization": key}
        payload = {
            "messages": [
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 150
        }
        
        response = requests.post(COTOMI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # エラーがあれば例外を発生させる
        
        cotomi_response = response.json()
        ai_response = cotomi_response['choices'][0]['message']['content'].strip()
        
        return jsonify({"response": ai_response})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": "Unexpected response format from Cotomi API"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# データベースへの追加を以下に書く




if __name__ == '__main__':
    app.run(debug=True)