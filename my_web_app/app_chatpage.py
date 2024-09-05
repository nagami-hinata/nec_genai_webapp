import os
import sys
import base64
import requests
import json
import time
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import uuid
import bcrypt


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
    












HTTP_HEADER_REQUEST_ID = 'x-nec-cotomi-request-id'
HTTP_HEADER_TANANT_ID = "x-nec-cotomi-tenant-id"

# 成功時と失敗時(デフォルト)の返すコードをグローバル変数として定義
SUCCESS_CODE = 0
FAILURE_CODE = 1

def encode_file_to_base64(file_path):
    """
    ファイルをBase64エンコードします。

    Args:
        file_path (str): エンコードするファイルのパス。

    Returns:
        str: Base64エンコードされたファイルの文字列。
    """
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("ascii")
    return encoded_string

def generate_file_url(base_url, file_path, root_dir):
    """
    ファイルのURLを生成します。

    Args:
        base_url (str): ベースURL。
        file_path (str): ファイルのパス。
        root_dir (str): ルートディレクトリのパス。

    Returns:
        str: 生成されたファイルのURL。
    """
    relative_path = os.path.relpath(file_path, root_dir)
    return os.path.join(base_url, relative_path).replace("\\", "/")


def process_file(
    api_url, auth_token, tenantId, vector_index, file_path,
    url=None, overwrite=True, custom_metadata=None, kwargs=None
    ):
    """
    ファイルを処理し、APIに送信します。

    Args:
        api_url (str): APIのURL。
        auth_token (str): 認証トークン。
        tenantId (str): テナントID。
        vector_index (str): ベクターインデックス。
        file_path (str): ファイルのパス。
        url (str, optional): ファイルのURL。デフォルトはNone。
        overwrite (bool, optional): 上書きフラグ。デフォルトはTrue。
        custom_metadata (dict, optional): カスタムメタデータ。デフォルトはNone。
        kwargs (dict, optional): 追加のキーワード引数。デフォルトはNone。

    Returns:
        int: 成功時は0、失敗時はエラーステータスコードまたは1を返します。
    """
    encoded_file = encode_file_to_base64(file_path)
    filename = os.path.basename(file_path)

    if kwargs is None:
        kwargs = {"split_chunk_size": "512", "split_overlap_size": "128"}

    if custom_metadata is None:
        custom_metadata = {}

    payload = {
        "vectorIndex": vector_index,
        "file": encoded_file,
        "filepath": filename,
        "url": url,
        "overWrite": overwrite,
        "kwargs": kwargs,
        "customMetadata": custom_metadata
    }

    headers = {
        "Content-Type": "application/json",
        "x-nec-cotomi-tenant-id": f"{tenantId}",
        "Authorization": f"Bearer {auth_token}",
    }

    start_time = time.time()

    try:
        response = requests.post(api_url, headers=headers, json=payload, verify=True)
        request_id = response.headers.get(HTTP_HEADER_REQUEST_ID)
        now = datetime.now(ZoneInfo("Asia/Tokyo"))

        print(f"Processed {filename} at {now}: {response.status_code} {response.text}")

        if response.status_code != 200:
            try:
                data = response.json()
                print("Response Data:", data)
            except json.JSONDecodeError:
                print("Response is not in JSON format")
                print("Response text:", response.text)
            return response.status_code  # エラーステータスコードを返す

        return SUCCESS_CODE  # 成功時

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        print(f"[add_document] Error adding document: {e}")
        print(f"Error occurred at: {now}")
        return FAILURE_CODE  # 失敗時のデフォルトエラーステータスコード

def main(directory_or_file_path, api_url, vector_index, auth_token, tenantId, url=None, 
         overwrite=True, custom_metadata=None, kwargs=None
        ):
    """
    ディレクトリまたはファイルを処理します。

    Args:
        directory_or_file_path (str): ディレクトリまたはファイルのパス。
        api_url (str): APIのURL。
        vector_index (str): ベクターインデックス。
        auth_token (str): 認証トークン。
        tenantId (str): テナントID。
        url (str, optional): ベースURL。デフォルトはNone。
        overwrite (bool, optional): 上書きフラグ。デフォルトはTrue。
        custom_metadata (dict, optional): カスタムメタデータ。デフォルトはNone。
        kwargs (dict, optional): 追加のキーワード引数。デフォルトはNone。

    Returns:
        int: 成功時は0、失敗時はエラーステータスコードまたは1を返します。
    """
    print(f"Starting process for directory or file: {directory_or_file_path}")
    
    if os.path.isdir(directory_or_file_path):
        for root, _, files in os.walk(directory_or_file_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_url = generate_file_url(url, file_path, directory_or_file_path) if url else None
                print(f"Processing file: {file_path}")
                status_code = process_file(
                    api_url, auth_token, tenantId, vector_index, file_path,
                    url=file_url, overwrite=overwrite, custom_metadata=custom_metadata, kwargs=kwargs
                )
                if status_code != SUCCESS_CODE:
                    return status_code
    elif os.path.isfile(directory_or_file_path):
        print(f"Processing single file: {directory_or_file_path}")
        status_code = process_file(
            api_url, auth_token, tenantId, vector_index, directory_or_file_path, 
            url, overwrite, custom_metadata, kwargs
        )
        if status_code != SUCCESS_CODE:
            return status_code
    else:
        print(f"Error: {directory_or_file_path} is neither a file nor a directory")
        return FAILURE_CODE

    return SUCCESS_CODE  # 全て成功時

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('tenantId', type=str, help='Tenant ID')
    parser.add_argument('api_url', type=str, help='API URL')
    parser.add_argument('auth_token', type=str, help='Authentication token')
    parser.add_argument('directory_or_file_path', type=str, help='Path to the directory or file')
    parser.add_argument('vector_index', type=str, help='Vector index')
    parser.add_argument('--url', type=str, default=None, help='Base URL')
    parser.add_argument('--overwrite', type=bool, default=True, help='Overwrite flag')
    parser.add_argument('--custom_metadata', type=json.loads, default=None, help='Custom metadata in JSON format')
    parser.add_argument('--kwargs', type=json.loads, default=None, help='Additional keyword arguments in JSON format')

    args = parser.parse_args()

    exit_code = main(
        args.directory_or_file_path,
        args.api_url,
        args.vector_index,
        args.auth_token,
        args.tenantId,
        url=args.url,
        overwrite=args.overwrite,
        custom_metadata=args.custom_metadata,
        kwargs=args.kwargs
    )

    sys.exit(exit_code)




# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 検索対話を行う関数. ストリーミングはオフ.
def search_chat(
    user_content, # ユーザプロンプト.
    vector_index, # インデックス名.
    system_content="あなたはAIアシスタントです", # システムプロンプト.
    client_id="DEFAULT", # クライアントID.
    history_id="new", # 会話履歴ID.
    temperature=1,  # LLMのランダム性パラメータ.
    search_option={"searchType": "hybrid", "chunkSize": 16, "topK": 4}, # 検索オプション.
    is_oneshot=False, # 単発の会話にするかどうか.
    max_tokens=1024 # LLMトークンの最大値.
    ):
    
    # APIエンドポイントのURL.
    url = "https://api.cotomi.nec-cloud.com/cotomi-api/v1/searchchat"
    # 認証パラメータ.
    key = "Bearer " + KEY
    
    # リクエストボディのパラメータ指定.
    payload = { "userContent": user_content,
                "systemContent": system_content,
                "vectorIndex": vector_index,
                "historyId": history_id,
                "temperature": temperature,
                "model": MODEL,
                "searchOption": search_option,
                "onshot": is_oneshot,
                "maxTokens": max_tokens}
    
    # リクエストヘッダのパラメータ指定.
    headers = { "content-type": "application/json",
                "x-nec-cotomi-client-id": client_id,
                "Authorization": key }
    
    # POSTリクエスト送信、レスポンス受信.
    response = requests.post(url, json=payload, headers=headers)
    return response




# # 検索対話を行うジェネレータ関数. ストリーミングはオン.
# def search_chat_streaming(
#     user_content, # ユーザプロンプト.
#     vector_index, # インデックス名.
#     system_content="あなたはAIアシスタントです", # システムプロンプト.
#     client_id="DEFAULT", # クライアントID.
#     history_id="new", # 会話履歴ID.
#     temperature=1,  # LLMのランダム性パラメータ.
#     search_option={"searchType": "hybrid", "chunkSize": 16, "topK": 4}, # 検索オプション.
#     is_oneshot=False, # 単発の会話にするかどうか.
#     stream_num=10, # ストリーミング時に何文字単位で返すか.
#     max_tokens=1024 # LLMトークンの最大値.
#     ):
    
#     # APIエンドポイントのURL.
#     url = "https://api.cotomi.nec-cloud.com/cotomi-api/v1/searchchat"
#     # 認証パラメータ.
#     key = "Bearer " + KEY
    
#     # リクエストボディのパラメータ指定.
#     payload = { "userContent": user_content,
#                 "systemContent": system_content,
#                 "vectorIndex": vector_index,
#                 "historyId": history_id,
#                 "temperature": temperature,
#                 "model": MODEL,
#                 "searchOption": search_option,
#                 "onshot": is_oneshot,
#                 "stream": True,
#                 "streamNum": stream_num,
#                 "maxTokens": max_tokens}
    
#     # リクエストヘッダのパラメータ指定.
#     headers = { "content-type": "application/json",
#                 "x-nec-cotomi-client-id": client_id,
#                 "Authorization": key }
#     # ストリーム形式でPOSTリクエスト送信、レスポンスを逐次受信.
#     with requests.post(url, json=payload, headers=headers, stream=True) as response:
#         # HTTPのエラー.
#         if not response.status_code == 200 :
#             data = None
#             try :
#                 data = response.json() # エラーメッセージ.
#             except Exception as e:
#                 print(e)
#             finally:
#                 now = datetime.now(ZoneInfo("Asia/Tokyo"))
#                 # エラー内容を標準出力.
#                 print("ERROR,DATE,{},httpStatus,{},errorMsg,{}".format(now.time().isoformat(timespec="seconds"), str(response.status_code), data))
#                 raise TypeError()
#         try:
#             # サーバー送信イベント (SSE)のストリーミング. MDNのドキュメント参照のこと(https://developer.mozilla.org/ja/docs/Web/API/Server-sent_events/Using_server-sent_events).
#             for chunk in response.iter_lines(decode_unicode=True): # 分割されたレスポンスを1つずつ処理.
#                 if chunk is None: # 空のチャンクはスキップ.
#                     continue
#                 if chunk.startswith("event:done") : # ストリームの終端.
#                     break
#                 if not chunk.startswith("data:") : # イベントメッセージを読み捨てる(表示させたい場合はこの中で処理を記述してください).
#                     continue
                
#                 data = json.loads(chunk[6:]) # "data: "を切り捨て.
#                 if "answer" in data:
#                     yield data["answer"] # 細切れのレスポンスを返す.
#                 if "error" in data:
#                     yield data["error"] # 途中に発生したエラーメッセージを返す.
#         except Exception as e:
#             # 予期せぬエラーキャッチ
#             print(e)
#             now = datetime.now(ZoneInfo("Asia/Tokyo"))
#             print("ERROR,DATE,{},httpStatus,{},line,{}".format(now.time().isoformat(timespec="seconds"), str(response.status_code), chunk))
            
if __name__ == "__main__":
    # ストリーミング無しの検索対話の呼び出し
    print(search_chat("<prompt>", "<index name>").text)
    
    # # ストリーミングありの検索対話の呼び出し
    # for talk in search_chat_streaming("<prompt>", "<index name>"):
    #     print(talk, end="")




















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