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

# KEY = "Bearer " + COTOMI_API_KEY

KEY = COTOMI_API_KEY



# 新規インデックスを作成.
# インデックス名は半角アルファベット、数字、ハイフンのみで構成される必要がある
def create_index(index):
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/index/createIndex/"
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分.
    # テナントIDを指定.
    headers = { "content-type": "application/json",
                "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key
            }
    # HTTPリクエストのボディ部分.
    # 新規作成するインデックス名を指定.
    # グループIDを指定
    payload = { "vectorIndex" : index,
                "groupId": GROUP_ID
                }
    
    # HTTPリクエストを送信.
    # ResponseオブジェクトはHTTPレスポンスが入ってくる.
    response = requests.post(url, headers=headers, json=payload)
    # Responseオブジェクトを返り値として返す.
    return response

# インデックス一覧を取得する関数.
def get_index_list():
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/index/listIndex/"
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key,
                }
    
    # HTTPリクエストを送信
    response = requests.get(url, headers=headers)
    return response

# 指定したインデックスを削除する関数
def delete_index(index):
    # APIエンドポイントURL.
    # index: 削除したいインデックス名
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/index/deleteIndex?vectorIndex=" + index
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key }
    
    # HTTPリクエストを送信
    response = requests.delete(url, headers=headers)
    return response

# 指定したインデックスに登録されている文書一覧を取得する関数
def get_document_list(index):
    # APIエンドポイントのURL.
    # index: 指定するインデックス名
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/document/listDocument?vectorIndex=" + index
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key
            }
    
    # HTTPリクエストを送信
    response = requests.get(url, headers=headers)
    return response

# 指定したインデックスに登録されている文書ファイルを削除する関数
def delete_document(index, file_path):
    # APIエンドポイントURL.
    # index: 削除したいファイルが登録されているインデックス名
    # file_path: 削除したいファイルのパス
    url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/document/deleteDocument?vectorIndex=" + index + "&filePath=" + file_path
    
    # APIキー. "Bearer"を忘れないこと. エラーになる.
    key = "Bearer " + KEY
    
    # HTTPリクエストのヘッダ部分
    # テナントIDを指定
    headers = { "x-nec-cotomi-tenant-id": TENANT_ID,
                "Authorization": key }
    # HTTPリクエストを送信
    response = requests.delete(url, headers=headers)
    return response


if __name__ == "__main__":
    import json
    # インデックスの作成
    create_index("<インデックス名>")
    # インデックスリストの表示
    print(json.dumps(get_index_list().json(), indent=2, ensure_ascii=False))
    # インデックスの削除
    delete_index("<インデックス名>")
    # 登録文書リストの表示
    print(json.dumps(get_document_list("<インデックス名>").json(), indent=2, ensure_ascii=False))
    # 登録文書の削除
    delete_document("<インデックス名>", "<ファイル名>")
    




























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