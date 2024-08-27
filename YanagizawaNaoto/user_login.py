import sqlite3

def user_login():
    # データベースに接続
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # ユーザー名とパスワードの入力
    username = input("ユーザー名を入力してください: ")
    password = input("パスワードを入力してください: ")

    try:
        # ユーザーの認証
        cursor.execute('''
        SELECT * FROM User 
        WHERE name = ? AND password = ?
        ''', (username, password))
        
        user_data = cursor.fetchone()
        
        if user_data:
            print("ログイン成功！")
            display_user_info(user_data, cursor)
        else:
            print("ログイン失敗。ユーザー名またはパスワードが間違っています。")

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

def display_user_info(user_data, cursor):
    # カラム名を取得
    cursor.execute("PRAGMA table_info(User)")
    columns = [column[1] for column in cursor.fetchall()]

    print("\nユーザー情報:")
    for column, value in zip(columns, user_data):
        if column == 'password':
            print(f"{column}: *****")  # パスワードは表示しない
        else:
            print(f"{column}: {value}")
    
    # ユーザーの所属グループと役割を表示
    user_id = user_data[2]  # unique_idのインデックス
    cursor.execute('''
    SELECT g.name, ugr.role
    FROM UserGroupRole ugr
    JOIN Group_table g ON ugr.group_id = g.unique_id
    WHERE ugr.user_id = ?
    ''', (user_id,))
    group_roles = cursor.fetchall()

    print("\n所属グループと役割:")
    for group_name, role in group_roles:
        print(f"  - {group_name}: {role}")

# 関数を実行
user_login()