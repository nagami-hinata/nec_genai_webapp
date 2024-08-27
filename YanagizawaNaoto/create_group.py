import sqlite3
import uuid
import re

def create_group():
    # データベースに接続
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # グループ名の入力
    while True:
        group_name = input("グループ名を入力してください: ")
        if group_name:
            break
        print("グループ名は空にできません。")

    # パスワードの入力
    while True:
        password = input("グループのパスワードを入力してください: ")
        if password:
            break
        print("パスワードは空にできません。")

    # ユニークIDの生成
    unique_id = str(uuid.uuid4())

    # メールアドレスのリストの作成
    email_list = []
    while True:
        email = input("メンバーのメールアドレスを入力してください（終了する場合は空白のまま Enter）: ")
        if not email:
            break
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_list.append(email)
        else:
            print("無効なメールアドレスです。もう一度試してください。")

    # メールアドレスをカンマ区切りの文字列に変換
    emails = ','.join(email_list)

    # グループをデータベースに挿入
    try:
        cursor.execute('''
        INSERT INTO Group_table (name, password, unique_id, e_mail)
        VALUES (?, ?, ?, ?)
        ''', (group_name, password, unique_id, emails))
        
        # グループ作成者を最高権限者として設定
        creator_email = input("グループ作成者のメールアドレスを入力してください: ")
        cursor.execute("SELECT unique_id FROM User WHERE e_mail = ?", (creator_email,))
        creator_id = cursor.fetchone()
        
        if creator_id:
            cursor.execute('''
            INSERT INTO UserGroupRole (user_id, group_id, role)
            VALUES (?, ?, ?)
            ''', (creator_id[0], unique_id, 'owner'))
        else:
            print("警告: 指定されたメールアドレスのユーザーが見つかりません。")
        
        conn.commit()
        print(f"グループ '{group_name}' が正常に作成されました。ユニークID: {unique_id}")
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# 関数を実行
create_group()