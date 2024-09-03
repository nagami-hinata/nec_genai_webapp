import sqlite3
import uuid
import re

def get_user_id_by_name(cursor, username):
    cursor.execute('SELECT unique_id FROM User WHERE name = ?', (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def create_group():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
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

        # 責任者の名前を入力（任意）
        leader_id = None
        while True:
            leader_name = input("グループ責任者のユーザー名を入力してください（スキップする場合は空白のまま Enter）: ")
            if not leader_name:
                print("責任者の指定をスキップします。")
                break
            leader_id = get_user_id_by_name(cursor, leader_name)
            if leader_id:
                print(f"責任者として {leader_name} (ID: {leader_id}) が設定されました。")
                break
            print("指定されたユーザーが見つかりません。正しいユーザー名を入力するか、スキップしてください。")

        # グループをデータベースに挿入
        cursor.execute('''
        INSERT INTO Group_table (name, password, unique_id, e_mail, leader_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (group_name, password, unique_id, emails, leader_id))

        # 責任者が指定された場合、そのユーザーのgroup_unique_idsを更新
        if leader_id:
            cursor.execute('''
            UPDATE User 
            SET group_unique_ids = CASE 
                WHEN group_unique_ids IS NULL OR group_unique_ids = '' THEN ? 
                ELSE group_unique_ids || ',' || ? 
            END
            WHERE unique_id = ?
            ''', (unique_id, unique_id, leader_id))

        conn.commit()
        print(f"グループ '{group_name}' が正常に作成されました。ユニークID: {unique_id}")
        if leader_id:
            print(f"責任者: {leader_name} (ID: {leader_id})")
        else:
            print("責任者は指定されていません。")

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# 使用例
if __name__ == "__main__":
    create_group()