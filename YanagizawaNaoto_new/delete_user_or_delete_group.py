import sqlite3

def remove_user_from_group():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # ユーザー認証
    username = input("ユーザー名を入力してください: ")
    password = input("パスワードを入力してください: ")

    try:
        cursor.execute('''
        SELECT unique_id, group_unique_ids FROM User 
        WHERE name = ? AND password = ?
        ''', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user_id, current_groups = user_data
            current_group_list = current_groups.split(',') if current_groups else []

            if not current_group_list:
                print("現在所属しているグループはありません。")
                return

            print("現在所属しているグループ:")
            for i, group_id in enumerate(current_group_list, 1):
                cursor.execute("SELECT name, leader_id FROM Group_table WHERE unique_id = ?", (group_id,))
                group_info = cursor.fetchone()
                if group_info:
                    group_name, leader_id = group_info
                    leader_status = "（責任者）" if leader_id == user_id else ""
                    print(f"{i}. {group_name} {leader_status}")
                else:
                    print(f"{i}. 不明なグループ")

            # 削除するグループの選択
            while True:
                try:
                    choice = int(input("削除するグループの番号を入力してください（0で中止）: "))
                    if choice == 0:
                        print("グループ削除を中止しました。")
                        return
                    if 1 <= choice <= len(current_group_list):
                        break
                    print("無効な選択です。もう一度試してください。")
                except ValueError:
                    print("数字を入力してください。")

            # 選択されたグループを削除
            removed_group_id = current_group_list[choice - 1]

            # グループの責任者かどうかを確認
            cursor.execute("SELECT leader_id FROM Group_table WHERE unique_id = ?", (removed_group_id,))
            leader_id = cursor.fetchone()[0]

            if leader_id == user_id:
                print("あなたはこのグループの責任者です。グループを離れる前に新しい責任者を指名する必要があります。")
                new_leader_name = input("新しい責任者のユーザー名を入力してください: ")
                cursor.execute("SELECT unique_id FROM User WHERE name = ?", (new_leader_name,))
                new_leader_id = cursor.fetchone()

                if new_leader_id:
                    cursor.execute("UPDATE Group_table SET leader_id = ? WHERE unique_id = ?", (new_leader_id[0], removed_group_id))
                    print(f"グループの責任者を {new_leader_name} に変更しました。")
                else:
                    print("指定されたユーザーが見つかりません。グループから削除できません。")
                    return

            current_group_list.remove(removed_group_id)
            updated_groups = ','.join(current_group_list)

            # ユーザーの所属グループを更新
            cursor.execute('''
            UPDATE User SET group_unique_ids = ? WHERE unique_id = ?
            ''', (updated_groups, user_id))

            # 削除されたグループの名前を取得
            cursor.execute("SELECT name FROM Group_table WHERE unique_id = ?", (removed_group_id,))
            removed_group_name = cursor.fetchone()[0]

            conn.commit()
            print(f"ユーザー '{username}' を グループ '{removed_group_name}' から正常に削除しました。")
        else:
            print("ユーザー名またはパスワードが正しくありません。")
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# 関数を実行
if __name__ == "__main__":
    remove_user_from_group()