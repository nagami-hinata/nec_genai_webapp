import sqlite3

def delete_user():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    username = input("削除するユーザーの名前を入力してください: ")
    password = input("ユーザーのパスワードを入力してください: ")

    try:
        # ユーザーが存在するか、またパスワードが正しいか確認
        cursor.execute("SELECT unique_id, name FROM User WHERE name = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            user_id, user_name = user
            
            # 確認プロンプト
            confirm = input(f"ユーザー '{user_name}' を削除しますか？ この操作は取り消せません。(y/n): ")
            
            if confirm.lower() == 'y':
                # 関連するチャットメッセージを削除
                cursor.execute("DELETE FROM Chat WHERE user_unique_id = ?", (user_id,))
                
                # UserGroupRoleテーブルから削除
                cursor.execute("DELETE FROM UserGroupRole WHERE user_id = ?", (user_id,))
                
                # ユーザーを削除
                cursor.execute("DELETE FROM User WHERE unique_id = ?", (user_id,))
                
                conn.commit()
                print(f"ユーザー '{user_name}' とその関連データが正常に削除されました。")
            else:
                print("削除操作がキャンセルされました。")
        else:
            print("ユーザー名またはパスワードが正しくありません。")

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

def delete_group():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    group_id = input("削除するグループのユニークIDを入力してください: ")

    try:
        # グループが存在するか確認
        cursor.execute("SELECT name FROM Group_table WHERE unique_id = ?", (group_id,))
        group = cursor.fetchone()

        if group:
            # 関連するチャットメッセージを削除
            cursor.execute("DELETE FROM Chat WHERE group_unique_id = ?", (group_id,))
            
            # 関連するデータを削除
            cursor.execute("DELETE FROM Data WHERE group_unique_id = ?", (group_id,))
            
            # UserGroupRoleテーブルから削除
            cursor.execute("DELETE FROM UserGroupRole WHERE group_id = ?", (group_id,))
            
            # グループを削除
            cursor.execute("DELETE FROM Group_table WHERE unique_id = ?", (group_id,))
            
            conn.commit()
            print(f"グループ '{group[0]}' とその関連データが正常に削除されました。")
        else:
            print("指定されたIDのグループが見つかりません。")

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# メイン実行部分
while True:
    print("\n1: ユーザーを削除")
    print("2: グループを削除")
    print("3: 終了")
    choice = input("選択してください (1/2/3): ")

    if choice == '1':
        delete_user()
    elif choice == '2':
        delete_group()
    elif choice == '3':
        break
    else:
        print("無効な選択です。もう一度試してください。")

print("プログラムを終了します。")