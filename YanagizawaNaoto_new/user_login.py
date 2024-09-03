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
        elif column == 'group_unique_ids':
            group_ids = value.split(',') if value else []
            print(f"{column}:")
            for group_id in group_ids:
                group_name, is_leader = get_group_info(group_id, user_data[2], cursor)
                leader_status = "（責任者）" if is_leader else ""
                print(f"  - {group_name} (ID: {group_id}) {leader_status}")
        else:
            print(f"{column}: {value}")

def get_group_info(group_id, user_id, cursor):
    cursor.execute("SELECT name, leader_id FROM Group_table WHERE unique_id = ?", (group_id,))
    result = cursor.fetchone()
    if result:
        return result[0], result[1] == user_id
    return "不明なグループ", False

# 関数を実行
user_login()