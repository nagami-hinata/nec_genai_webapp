from flask import Flask, session, render_template, request, redirect, url_for, flash, render_template, jsonify
import sqlite3
import uuid
import bcrypt
import PyPDF2
import re
import os
import json
import requests
from werkzeug.utils import secure_filename
from add_or_get_or_delete_data import data_bp
from datetime import timedelta
import sys
import base64
import time
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import uuid
import bcrypt





app = Flask(__name__)
app.secret_key = 'session_key'  # セッションを暗号化するための秘密鍵
app.permanent_session_lifetime = timedelta(minutes=30)  # セッションの有効期限を設定




# Cotomi APIの設定
COTOMI_API_URL = "https://api.cotomi.com/v1/chat/completions"
COTOMI_API_KEY = os.environ.get('COTOMI_API_KEY')  # 環境変数に設定してるものをとってきてる
GROUP_ID = os.environ.get('GROUP_ID')
TENANT_ID = os.environ.get('TENANT_ID')

# KEY = "Bearer " + COTOMI_API_KEY

KEY = COTOMI_API_KEY





def get_db_connection():
    conn = sqlite3.connect('chat_app.db')
    conn.row_factory = sqlite3.Row
    return conn


# ラグ用の関数
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


# ファイルをインデックスに登録する関数
def register_file_to_index(file_path, index, api_url):
    key = f"Bearer {KEY}"
    headers = {
        "content-type": "application/json",
        "x-nec-cotomi-tenant-id": TENANT_ID,
        "Authorization": key
    }
    payload = {
        "vectorIndex": index,
        "file": file_path,
        "groupId": GROUP_ID
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.status_code == 200





# 検索対話用

# 使用するモデル名.
MODEL = "cotomi-core-pro-v1.0-awq"

# 検索対話を行う関数. ストリーミングはオフ.
def search_chat(
    user_content, # ユーザプロンプト.       # 実質的な引数
    vector_index, # インデックス名.         # 実質的な引数
    system_content="あなたはAIアシスタントです", # システムプロンプト.
    client_id="DEFAULT", # クライアントID.
    history_id="new", # 会話履歴ID.
    temperature=1,  # LLMのランダム性パラメータ.
    search_option={"searchType": "hybrid", "chunkSize": 16, "topK": 4}, # 検索オプション.
    is_oneshot=False, # 単発の会話にするかどうか.
    max_tokens=8096 # LLMトークンの最大値.
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







@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user-name']
        email = request.form['e-mail']
        password = request.form['password']
        group_unique_ids = request.form['group-id']

        # パスワードをハッシュ化
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # ユニークIDの生成
        unique_id = str(uuid.uuid4())

        # データベース接続
        conn = get_db_connection()
        cur = conn.cursor()

        # Group_tableにgroup_unique_idが存在するか確認
        cur.execute("SELECT COUNT(*) FROM Group_table WHERE unique_id = ?", (group_unique_ids,))
        if cur.fetchone()[0] == 0:
            conn.close()
            flash("入力されたグループIDは存在しません。")
            return redirect(url_for('register'))

        # Userテーブルにデータを挿入
        cur.execute('''
            INSERT INTO User (name, password, unique_id, e_mail, last_page, group_unique_ids, tag)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_name, hashed_password, unique_id, email, None, group_unique_ids, None))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['e-mail']
        password = request.form['password']

        # データベース接続
        conn = get_db_connection()
        cur = conn.cursor()

        # Userテーブルからメールアドレスでユーザー情報を取得
        cur.execute("SELECT * FROM User WHERE e_mail = ?", (email,))
        user = cur.fetchone()
        
        
        # セッション変数に格納する処理
        cur.execute("SELECT unique_id FROM Group_table WHERE e_mail = ?", (email,))
        result = cur.fetchone()  # メールに対応するunique_idを取得
        
        if result:
            unique_id = result[0]
            session['unique_id_session'] = unique_id  # session変数に格納
        
        
        conn.close()

        if user is None:
            flash('メールアドレスが見つかりません。')
            return redirect(url_for('login'))

        # パスワードの照合
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # 認証成功時にセッション情報を保持
            # session['user_id'] = user['unique_id']
            return redirect(url_for('chatpage'))
        else:
            flash('パスワードが間違っています。')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/author_register', methods=['GET', 'POST'])
def author_register():
    if request.method == 'POST':
        company_name = request.form['user-name']
        email = request.form['e-mail']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Generate a unique ID
        unique_id = str(uuid.uuid4())

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the Group_table
        cur.execute('''
            INSERT INTO Group_table (name, e_mail, password, unique_id, leader_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (company_name, email, hashed_password, unique_id, None))

        conn.commit()
        conn.close()

        return redirect(url_for('author_login'))

    return render_template('author_register.html')

@app.route('/author_login', methods=['GET', 'POST'])
def author_login():
    if request.method == 'POST':
        email = request.form['e-mail']
        password = request.form['password']

        # データベース接続
        conn = get_db_connection()
        cur = conn.cursor()

        # Group_tableからメールアドレスでグループ情報を取得
        cur.execute("SELECT * FROM Group_table WHERE e_mail = ?", (email,))
        group = cur.fetchone()
        
        
        # セッション変数に格納する処理
        cur.execute("SELECT unique_id FROM Group_table WHERE e_mail = ?", (email,))
        result = cur.fetchone()  # メールに対応するunique_idを取得
        
        if result:
            unique_id = result[0]
            session['unique_id_session'] = unique_id  # session変数に格納
        
        
        conn.close()

        if group is None:
            flash('メールアドレスが見つかりません。')
            return redirect(url_for('author_login'))

        # パスワードの照合
        if bcrypt.checkpw(password.encode('utf-8'), group['password']):
            # 認証成功時にセッション情報を保持
            # session['group_id'] = group['unique_id']
            return redirect(url_for('chatpage'))
        else:
            flash('パスワードが間違っています。')
            return redirect(url_for('author_login'))

    return render_template('author_login.html')



@app.route('/chatpage')
def chatpage():
    # データベースに接続
    conn = get_db_connection()
    cur = conn.cursor()
    
    # タグを取得
    cur.execute("SELECT tag FROM Tag")
    results = cur.fetchall()   # 全てのタグを取得
    tags = list(dict.fromkeys([results[0] for result in results]))  
    
    
    # 会話内容を取得
    current_login_user_unique_id = session['unique_id_session']  # 現在ログインしているユーザーのユニークID取得
    cur.execute("SELECT * FROM Chat WHERE user_unique_id = ?", (current_login_user_unique_id,))
    chats = cur.fetchall()
    
    # Threadテーブルからuser_unique_idが同じものを取得
    cur.execute("SELECT * FROM Thread WHERE user_unique_id = ?", (current_login_user_unique_id,))
    threads = cur.fetchall()  # そのユーザーが持つすべてのスレッド
        
    # 結果を辞書のリストに変換
    columns = [column[0] for column in cur.description]
    chats = []
    for row in chats:
        chats.append(dict(zip(columns, row)))  # オブジェクトの配列
    
    
    if tags == []:
        conn.close()
        return render_template('chatpage.html', tags=tags, chats=chats, threads=threads)
    else: 
        conn.close()
    
        # 取得したタグ一覧を配列として送ってレンダリング
        return render_template('chatpage.html', tags=tags, chats=chats, threads=threads)        

    

thread_number = 1
current_thread_number = 1
# 文章登録用

HTTP_HEADER_REQUEST_ID = 'x-nec-cotomi-request-id'
HTTP_HEADER_TANANT_ID = "x-nec-cotomi-tenant-id"

# 成功時と失敗時(デフォルト)の返すコードをグローバル変数として定義
SUCCESS_CODE = 0
FAILURE_CODE = 1
    
# chatpageでタグを選択したときの処理
@app.route('/tag_select', methods=['POST'])
def tag_select():
    global thread_number  # thread_numberをグローバル変数として利用
    global current_thread_number
    
    # 選択されたタグをすべて取得
    selected_tag = request.form.get('tag')  # 配列として取得
    
    current_login_user_unique_id = session['unique_id_session']  # 現在ログインしているユーザーのユニークID取得
    
    
    # データベースに接続
    conn = get_db_connection()
    cur = conn.cursor()
    
    files = []
    cur.execute("SELECT file_name FROM Data WHERE tag = ?", (selected_tag,))  # タグに対応したファイルを取得
    files = [row[0] for row in cur.fetchall()]  # ファイル名を要素に持つ配列
    
    files = list(set([row[0] for row in cur.fetchall()]))  # 重複の削除  

    # Threadテーブルに入れる
    cur.execute("INSERT INTO Thread (thread, tag, user_unique_id) VALUES (?, ?, ?)", (thread_number, selected_tag, current_login_user_unique_id))

    
    # Threadテーブルからuser_unique_idが同じものを取得
    cur.execute("SELECT * FROM Thread WHERE user_unique_id = ?", (current_login_user_unique_id,))
    threads = cur.fetchall()
    
    # 会話履歴を取得
    cur.execute("SELECT * FROM Chat WHERE user_unique_id = ?", (current_login_user_unique_id,))
    chats = cur.fetchall()
    
    # タグを取得
    cur.execute("SELECT tag FROM Data")
    tags = cur.fetchall()
    
    
    
    conn.commit()  # データベースに変更をコミット
    conn.close()  # データベースとの接続を切る
    
    

    index = f"index_{thread_number}"  # インデックスの名前をつける
    
    current_thread_number = thread_number  # スレッドを作ったときの番号を現在のスレッド変数に代入
    
    thread_number += 1  # スレッドナンバーを更新
    
    
    # 新規インデックスを作成
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
    
    add_document_url = "https://api.cotomi.nec-cloud.com/cotomi-search-api/document/addDocument/"
    # 作ったインデックスに選択されたタグ属性を持つファイルをアップ
    for file in files:
        success = register_file_to_index(file, index, add_document_url)
        
    return render_template('chatpage.html', tags=tags, chats=chats, threads=threads)

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



current_index = 1

# チャット用のエンドポイント
@app.route('/send_message', methods=['POST'])
def send_message():
    global current_index
    global current_thread_number
    
    current_index = current_thread_number
    
    data = request.json
    user_message = data['message']
    # index = Data.query.filter_by(folder_unique_id=folder.folder_unique_id).all()

    
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    
    
    # Cotomiとのやり取り
    try:
        index = f"index_{current_index}"

        ai_response = search_chat(user_message, index).text
        
        # response = requests.post(COTOMI_API_URL, headers=headers, json=payload)
        # response.raise_for_status()  # エラーがあれば例外を発生させる
        
        # cotomi_response = response.json()
        # ai_response = cotomi_response['choices'][0]['message']['content'].strip()
        
        return jsonify({"response": ai_response})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": "Unexpected response format from Cotomi API"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/data_reference', methods=['GET', 'POST'])
def data_reference():
    group_unique_id = session.get('unique_id_session')
    
    app.logger.info(f"Accessed data_reference. group_unique_id: {group_unique_id}")

    if group_unique_id is None:
        app.logger.warning("User not logged in, redirecting to login page")
        flash('ログインが必要です。', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            action = request.form.get('action')
            file_name = request.form.get('file_name')

            app.logger.info(f"Received POST request: action={action}, file_name={file_name}")

            if not file_name:
                raise ValueError('ファイル名が指定されていません。')

            if action == 'rename':
                new_name = request.form.get('new_name')
                if not new_name:
                    raise ValueError('新しいファイル名が指定されていません。')

                app.logger.info(f"Renaming file: {file_name} to {new_name}")

                # ファイルの存在確認
                cur.execute('SELECT * FROM Data WHERE file_name = ? AND group_unique_id = ?', (file_name, group_unique_id))
                result = cur.fetchone()
                if result is None:
                    app.logger.warning(f"File not found: file_name={file_name}, group_unique_id={group_unique_id}")
                    raise ValueError('指定されたファイルが見つかりません。')

                app.logger.info(f"File found: {result}")

                cur.execute('''
                    UPDATE Data 
                    SET file_name = ? 
                    WHERE file_name = ? AND group_unique_id = ?
                ''', (new_name, file_name, group_unique_id))
                
                conn.commit()
                app.logger.info(f"File renamed successfully: {file_name} to {new_name}")
                return jsonify({"success": True, "message": "ファイル名が変更されました"})

            elif action == 'delete':
                app.logger.info(f"Deleting file: {file_name}")

                # ファイルの存在確認
                cur.execute('SELECT * FROM Data WHERE file_name = ? AND group_unique_id = ?', (file_name, group_unique_id))
                result = cur.fetchone()
                if result is None:
                    app.logger.warning(f"File not found for deletion: file_name={file_name}, group_unique_id={group_unique_id}")
                    raise ValueError('削除するファイルが見つかりません。')

                app.logger.info(f"File found for deletion: {result}")

                cur.execute('''
                    DELETE FROM Data 
                    WHERE file_name = ? AND group_unique_id = ?
                ''', (file_name, group_unique_id))
                
                conn.commit()
                app.logger.info(f"File deleted successfully: {file_name}")
                return jsonify({"success": True, "message": "ファイルが削除されました"})

            else:
                app.logger.warning(f"Invalid action received: {action}")
                raise ValueError('無効なアクションです。')

        except ValueError as e:
            app.logger.error(f"ValueError: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return jsonify({"error": "サーバーエラーが発生しました"}), 500
        finally:
            cur.close()
            conn.close()

    # GETリクエストの処理
    try:
        app.logger.info(f"Fetching files for group_unique_id: {group_unique_id}")
        cur.execute('''
            SELECT file_name, content, page
            FROM Data
            WHERE group_unique_id = ? AND page = 1
            ORDER BY file_name
        ''', (group_unique_id,))
        
        data_files = cur.fetchall()
        app.logger.info(f"Retrieved {len(data_files)} files for group_unique_id={group_unique_id}")
        return render_template('data_reference.html', data_files=data_files)
    except Exception as e:
        app.logger.error(f"Error fetching data: {str(e)}", exc_info=True)
        flash('データの取得中にエラーが発生しました。', 'error')
        return redirect(url_for('error_page'))
    finally:
        cur.close()
        conn.close()

# アップロードされたファイルを保存するフォルダー
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# アップロードを許可するファイル拡張子
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/tag_edit', methods=['GET', 'POST'])
# def tag_edit():
#     # セッションからgroup_unique_idを取得（新しく追加）
#     group_unique_id = session.get('unique_id_session')
    
#     if group_unique_id is None:
#         flash('ログインが必要です。')
#         return redirect(url_for('login'))

#     tags = []
#     error_message = None
#     if request.method == 'POST':
#         # アップロードされたファイルを取得
#         if 'file' not in request.files:
#             flash('ファイルが選択されていません。')
#             return redirect(url_for('tag_edit'))

#         uploaded_file = request.files['file']
        
#         if uploaded_file.filename == '':
#             flash('ファイルが選択されていません。')
#             return redirect(url_for('tag_edit'))

#         if not uploaded_file.filename.endswith('.pdf'):
#             flash('PDFファイルのみが許可されています。')
#             return redirect(url_for('tag_edit'))

#         # PDFファイルを読み込み
#         try:
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)

#             # データベース接続を確立
#             conn = get_db_connection()
#             conn.row_factory = sqlite3.Row
#             cur = conn.cursor()

#             # 各ページからテキストを抽出し、データベースに保存
#             for page_num in range(len(pdf_reader.pages)):
#                 page = pdf_reader.pages[page_num]
#                 extracted_text = page.extract_text()

#                 # 空白2つ以上と改行2つ以上をそれぞれ1つに置き換える
#                 if extracted_text:  # extracted_text が None ではないことを確認
#                     extracted_text = re.sub(r'\s{2,}', ' ', extracted_text)  # 空白2つ以上を1つに
#                     extracted_text = re.sub(r'\n{2,}', '\n', extracted_text)  # 改行2つ以上を1つに

#                 # データベースに保存 (group_unique_idを含める)
#                 cur.execute('''
#                     INSERT INTO Data (content, group_unique_id, folder_unique_id, page, file_name, thread_number, tag, genre, color)
#                     VALUES (?, ?, NULL, ?, ?, NULL, NULL, NULL, NULL)
#                 ''', (extracted_text, group_unique_id, page_num + 1, uploaded_file.filename))

#             # ジャンルとタグ、色をデータベースからとってきて変数に格納
#             cur.execute("SELECT * FROM Tag")
            
#             rows = cur.fetchall()
            
#             # 各行をオブジェクトに変換しリストに追加
#             tags = [dict(row) for row in rows]
            
#             # コミットして接続を閉じる
#             conn.commit()
#             conn.close()
            
#             # ファイルが要求に含まれているか確認
#             if 'file' not in request.files:
#                 return jsonify({"error": "No file part in the request"}), 400
#             file = request.files['file']
    
#             # ファイル名が空でないか確認
#             if file.filename == '':
#                 return jsonify({"error": "No file selected for uploading"}), 400
    
#             # ファイルが許可された拡張子を持っているか、安全なファイル名か確認
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 # アップロードフォルダーが存在しない場合は作成
#                 if not os.path.exists(app.config['UPLOAD_FOLDER']):
#                     os.makedirs(app.config['UPLOAD_FOLDER'])
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             else:
#                 return jsonify({"error": "Allowed file types are txt, pdf, png, jpg, jpeg, gif"}), 400

#             flash('PDFからテキストが抽出され、保存されました。')
#             return redirect(url_for('tag_edit'))

#         except Exception as e:
#             flash('PDFからテキストを抽出できませんでした。')
#             return redirect(url_for('tag_edit'))

#     return render_template('tag_edit.html', tags=tags)


@app.route('/tag_edit', methods=['GET', 'POST'])
def tag_edit():
    # セッションからgroup_unique_idを取得（新しく追加）
    group_unique_id = session.get('unique_id_session')
    
    if group_unique_id is None:
        flash('ログインが必要です。')
        return redirect(url_for('login'))
    
    # データベース接続を確立
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # ジャンルとタグ、色をデータベースからとってきて変数に格納
    # 後でunique_idが同じものだけ取ってくるようにする
    cur.execute("SELECT * FROM Tag")
            
    rows = cur.fetchall()
            
    # 各行をオブジェクトに変換しリストに追加
    tags = [dict(row) for row in rows]
            
    # コミットして接続を閉じる
    conn.commit()
    conn.close()
    
    return render_template('tag_edit.html', tags=tags)

 


# fileをアップロードしたときのエンドポイント
@app.route('/file_up', methods=['POST'])
def file_up():
    tags = []
    error_message = None
    # セッションからgroup_unique_idを取得（新しく追加）
    group_unique_id = session.get('unique_id_session')
    
    # アップロードされたファイルを取得
    if 'file' not in request.files:
        flash('ファイルが選択されていません。')
        return redirect(url_for('tag_edit'))

    uploaded_file = request.files['file']
            
    if uploaded_file.filename == '':
        flash('ファイルが選択されていません。')
        return redirect(url_for('tag_edit'))

    if not uploaded_file.filename.endswith('.pdf'):
        flash('PDFファイルのみが許可されています。')
        return redirect(url_for('tag_edit'))


    # PDFファイルを読み込み
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        # データベース接続を確立
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # 各ページからテキストを抽出し、データベースに保存
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text = page.extract_text()

            # 空白2つ以上と改行2つ以上をそれぞれ1つに置き換える
            if extracted_text:  # extracted_text が None ではないことを確認
                extracted_text = re.sub(r'\s{2,}', ' ', extracted_text)  # 空白2つ以上を1つに
                extracted_text = re.sub(r'\n{2,}', '\n', extracted_text)  # 改行2つ以上を1つに

            # データベースに保存 (group_unique_idを含める)
            cur.execute('''
                INSERT INTO Data (content, group_unique_id, folder_unique_id, page, file_name, thread_number, tag, genre, color)
                VALUES (?, ?, NULL, ?, ?, NULL, NULL, NULL, NULL)
            ''', (extracted_text, group_unique_id, page_num + 1, uploaded_file.filename))

        file = request.files['file']
           
        # # ファイルが要求に含まれているか確認
        # if 'file' not in request.files:
        #     return jsonify({"error": "No file part in the request"}), 400
        
        # # ファイル名が空でないか確認
        # if file.filename == '':
        #     return jsonify({"error": "No file selected for uploading"}), 400
        
        # ファイルが許可された拡張子を持っているか、安全なファイル名か確認
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # アップロードフォルダーが存在しない場合は作成
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # else:
            # return jsonify({"error": "Allowed file types are txt, pdf, png, jpg, jpeg, gif"}), 400

        flash('PDFからテキストが抽出され、保存されました。')
        # return render_template('tag_edit.html', tags=tags)
        return redirect(url_for('tag_edit'))

    except Exception as e:
        flash('PDFからテキストを抽出できませんでした。')
        # return render_template('tag_edit.html', tags=tags)
        return redirect(url_for('tag_edit'))



# ジャンルとタグを新規作成したときのエンドポイント
# @app.route('/create_tag', methods=['POST'])
# def create_tag():
#     try:
#         tags = []
#         data = request.json
    
#         genre = data['genre']
#         tag = data['tag']
#         color = data['color']

    
#         # データベース接続を確立
#         conn = get_db_connection()
#         cur = conn.cursor()
    
#         conn.execute("INSERT INTO Tag (genre, tag, color) VALUES (?, ?, ?)", (genre, tag, color))
#         conn.commit()
    
#         # ジャンルとタグ、色をデータベースからとってきて変数に格納
#         cur.execute("SELECT * FROM Tag")
            
#         rows = cur.fetchall()
            
#         # 各行をオブジェクトに変換しリストに追加
#         tags = [dict(row) for row in rows]
            
#         return render_template('tag_edit.html', tags=tags)
#     except sqlite3.Error as e:
#         conn.rollback()
#         return jsonify({'error': str(e)}), 500
#     finally:
#         conn.close()
#         return render_template('tag_edit.html', tags=tags)


@app.route('/create_tag', methods=['POST'])
def create_tag():
    try:
        data = request.json
        
        genre = data['genre']
        tag = data['tag']
        color = data['color']
        
        # データベース接続を確立
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("INSERT INTO Tag (genre, tag, color) VALUES (?, ?, ?)", (genre, tag, color))
        conn.commit()
        
        # 新しく追加したタグの情報を返す
        return jsonify({
            'success': True,
            'tag': {
                'genre': genre,
                'tag': tag,
                'color': color
            }
        }), 200
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    


@app.route('/user_edit')
def user_edit():
    return render_template('user_edit.html')

@app.route('/data_deleted')
def data_deleted():
    return render_template('data_deleted.html')

@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.form['message']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (?)", (message,))
    conn.commit()
    conn.close()
    return 'Message added successfully'

if __name__ == '__main__':
    app.run(debug=True)
