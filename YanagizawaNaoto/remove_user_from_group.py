import sqlite3

def remove_user_from_group():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # ユーザー認証
    username = input("ユーザー名を入力してください: ")
    password = input("パスワードを入力してください: ")

    try:
        cursor.execute('''
        SELECT unique_id FROM User 
        WHERE name = ? AND password = ?
        ''', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user_id = user_data[0]

            # ユーザーが所属しているグループを取得
            cursor.execute('''
            SELECT g.unique_id, g.name, ugr.role
            FROM UserGroupRole ugr
            JOIN Group_table g ON ugr.group_id = g.unique_id
            WHERE ugr.user_id = ?
            ''', (user_id,))
            groups = cursor.fetchall()

            if not groups:
                print("現在所属しているグループはありません。")
                return

            print("現在所属しているグループ:")
            for i, (group_id, group_name, role) in enumerate(groups, 1):
                print(f"{i}. {group_name} (役割: {role})")

            # 削除するグループの選択
            while True:
                try:
                    choice = int(input("削除するグループの番号を入力してください（0で中止）: "))
                    if choice == 0:
                        print("グループ削除を中止しました。")
                        return
                    if 1 <= choice <= len(groups):
                        break
                    print("無効な選択です。もう一度試してください。")
                except ValueError:
                    print("数字を入力してください。")

            # 選択されたグループからユーザーを削除
            removed_group_id, removed_group_name, _ = groups[choice - 1]

            cursor.execute('''
            DELETE FROM UserGroupRole
            WHERE user_id = ? AND group_id = ?
            ''', (user_id, removed_group_id))

            conn.commit()
            print(f"ユーザー '{username}' を グループ '{removed_group_name}' から正常に削除しました。")
        else:
            print("ユーザー名またはパスワードが正しくありません。")

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# 関数を実行
remove_user_from_group()