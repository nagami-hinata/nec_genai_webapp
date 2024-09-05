import sqlite3
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
from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template
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


# 文章登録用
HTTP_HEADER_REQUEST_ID = 'x-nec-cotomi-request-id'
HTTP_HEADER_TANANT_ID = "x-nec-cotomi-tenant-id"

# 成功時と失敗時(デフォルト)の返すコードをグローバル変数として定義
SUCCESS_CODE = 0
FAILURE_CODE = 1

# エンコード関数
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

# URL作成関数
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

# ファイルを処理しAPIに送信
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
    encoded_file = encode_file_to_base64(file_path)     # 1個目の関数
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

# ファイルをAPIに送る
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
                file_url = generate_file_url(url, file_path, directory_or_file_path) if url else None       # 2個目の関数
                print(f"Processing file: {file_path}")
                status_code = process_file(                                                                 # 3個目の関数
                    api_url, auth_token, tenantId, vector_index, file_path,
                    url=file_url, overwrite=overwrite, custom_metadata=custom_metadata, kwargs=kwargs
                )
                if status_code != SUCCESS_CODE:
                    return status_code
    elif os.path.isfile(directory_or_file_path):
        print(f"Processing single file: {directory_or_file_path}")
        status_code = process_file(                                                                         # 3個目の関数
            api_url, auth_token, tenantId, vector_index, directory_or_file_path, 
            url, overwrite, custom_metadata, kwargs
        )
        if status_code != SUCCESS_CODE:
            return status_code
    else:
        print(f"Error: {directory_or_file_path} is neither a file nor a directory")
        return FAILURE_CODE

    return SUCCESS_CODE  # 全て成功時



def add_data():
    group_id = input("データを追加するグループのIDを入力してください: ")
    content = input("データの内容を入力してください: ")
    page = int(input("ページ番号を入力してください: "))
    file_name = input("ファイル名を入力してください: ")

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        # ファイルをデータベースへ登録
        cursor.execute('''
        INSERT INTO Data (content, group_unique_id, page, file_name)
        VALUES (?, ?, ?, ?)
        ''', (content, group_id, page, file_name))
              

        # ファイルをfilesフォルダーに追加 
        
        
        
        
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


        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        conn.commit()
        print(f"データが正常に追加されました。ファイル名: {file_name}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return None
    finally:
        conn.close()

def get_data():
    group_id = input("データを取得するグループのIDを入力してください（省略可能）: ")
    page_input = input("ページ番号を入力してください（省略可能）: ")
    file_name = input("ファイル名を入力してください（省略可能）: ")

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        query = 'SELECT rowid, * FROM Data WHERE 1=1'
        params = []

        if group_id:
            query += ' AND group_unique_id = ?'
            params.append(group_id)
        if page_input:
            query += ' AND page = ?'
            params.append(int(page_input))
        if file_name:
            query += ' AND file_name = ?'
            params.append(file_name)

        cursor.execute(query, params)
        data = cursor.fetchall()

        if data:
            print("取得されたデータ:")
            for row in data:
                print(f"ID: {row[0]}, グループID: {row[2]}, ページ: {row[3]}, ファイル名: {row[4]}")
                print(f"内容: {row[1]}\n")
        else:
            print("条件に一致するデータが見つかりません。")

        return data
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return []
    finally:
        conn.close()

def delete_data():
    data_id = int(input("削除するデータのIDを入力してください: "))

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT file_name FROM Data WHERE rowid = ?', (data_id,))
        result = cursor.fetchone()

        if result:
            cursor.execute('DELETE FROM Data WHERE rowid = ?', (data_id,))
            conn.commit()
            print(f"データが正常に削除されました。ファイル名: {result[0]}")
            return True
        else:
            print(f"ID {data_id} のデータが見つかりません。")
            return False
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return False
    finally:
        conn.close()

def main():
    while True:
        print("\nデータ操作を選択してください:")
        print("1: データを追加")
        print("2: データを取得")
        print("3: データを削除")
        print("4: 終了")
        
        choice = input("選択してください (1/2/3/4): ")
        
        if choice == '1':
            add_data()
        elif choice == '2':
            get_data()
        elif choice == '3':
            delete_data()
        elif choice == '4':
            print("プログラムを終了します。")
            break
        else:
            print("無効な選択です。もう一度試してください。")

if __name__ == "__main__":
    main()