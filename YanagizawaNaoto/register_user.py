import sqlite3
import uuid
import re

def get_group_id(cursor, group_name, group_password):
    cursor.execute('''
    SELECT unique_id FROM Group_table 
    WHERE name = ? AND password = ?
    ''', (group_name, group_password))
    result = cursor.fetchone()
    return result[0] if result else None

def register_user():
    # データベースに接続
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # ユーザー名の入力
    while True:
        user_name = input("ユーザー名を入力してください: ")
        if user_name:
            break
        print("ユーザー名は空にできません。")

    # パスワードの入力
    while True:
        password = input("パスワードを入力してください: ")
        if password:
            break
        print("パスワードは空にできません。")

    # ユニークIDの生成
    unique_id = str(uuid.uuid4())

    # メールアドレスの入力
    while True:
        email = input("メールアドレスを入力してください: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        print("無効なメールアドレスです。もう一度試してください。")

    # 初期のlast_pageを空文字列に設定
    last_page = ''

    # ユーザーをデータベースに挿入
    try:
        cursor.execute('''
        INSERT INTO User (name, password, unique_id, e_mail, last_page)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_name, password, unique_id, email, last_page))
        
        # 所属グループの入力
        while True:
            group_name = input("所属するグループの名前を入力してください（終了する場合は空白のまま Enter）: ")
            if not group_name:
                break
            group_password = input(f"{group_name} のパスワードを入力してください: ")
            
            group_id = get_group_id(cursor, group_name, group_password)
            if group_id:
                role = input(f"{group_name} での役割を入力してください (member/admin/owner): ")
                cursor.execute('''
                INSERT INTO UserGroupRole (user_id, group_id, role)
                VALUES (?, ?, ?)
                ''', (unique_id, group_id, role))
                print(f"{group_name} に正常に所属しました。")
            else:
                print("グループ名またはパスワードが正しくありません。")
        
        conn.commit()
        print(f"ユーザー '{user_name}' が正常に登録されました。ユニークID: {unique_id}")
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# 関数を実行
register_user()