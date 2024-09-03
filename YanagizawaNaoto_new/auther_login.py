import sqlite3
import uuid
import re

def admin_login():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    username = input("管理者名を入力してください: ")
    password = input("パスワードを入力してください: ")

    try:
        cursor.execute('''
        SELECT * FROM User 
        WHERE name = ? AND password = ?
        ''', (username, password))
        
        user_data = cursor.fetchone()
        
        if user_data:
            print("ログイン成功！")
            admin_menu(user_data, cursor, conn)
        else:
            print("ログイン失敗。ユーザー名またはパスワードが間違っています。")
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

def admin_menu(user_data, cursor, conn):
    user_id = user_data[2]  # unique_id
    cursor.execute("SELECT * FROM Group_table WHERE leader_id = ?", (user_id,))
    admin_groups = cursor.fetchall()

    if admin_groups:
        print("\n管理しているグループ:")
        for group in admin_groups:
            print(f"- {group[0]} (ID: {group[2]})")
        
        display_user_info(user_data, cursor)
    else:
        print("\nあなたは現在どのグループの管理者でもありません。")
        create_new_group = input("新しいグループを作成しますか？ (y/n): ")
        if create_new_group.lower() == 'y':
            create_group(user_id, cursor, conn)

def display_user_info(user_data, cursor):
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

def create_group(user_id, cursor, conn):
    group_name = input("新しいグループ名を入力してください: ")
    password = input("グループのパスワードを入力してください: ")
    unique_id = str(uuid.uuid4())

    email_list = []
    while True:
        email = input("メンバーのメールアドレスを入力してください（終了する場合は空白のまま Enter）: ")
        if not email:
            break
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_list.append(email)
        else:
            print("無効なメールアドレスです。もう一度試してください。")

    emails = ','.join(email_list)

    try:
        cursor.execute('''
        INSERT INTO Group_table (name, password, unique_id, e_mail, leader_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (group_name, password, unique_id, emails, user_id))

        cursor.execute('''
        UPDATE User 
        SET group_unique_ids = CASE 
            WHEN group_unique_ids IS NULL OR group_unique_ids = '' THEN ? 
            ELSE group_unique_ids || ',' || ? 
        END
        WHERE unique_id = ?
        ''', (unique_id, unique_id, user_id))

        conn.commit()
        print(f"グループ '{group_name}' が正常に作成されました。ユニークID: {unique_id}")
    except sqlite3.Error as e:
        print(f"グループ作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    admin_login()