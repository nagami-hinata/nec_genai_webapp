import sqlite3

def add_user_to_group():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # ユーザー認証
    username = input("ユーザー名を入力してください: ")
    password = input("パスワードを入力してください: ")

    try:
        cursor.execute('''
        SELECT unique_id, group_unique_ids, e_mail FROM User 
        WHERE name = ? AND password = ?
        ''', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user_id, current_groups, user_email = user_data
            current_group_list = current_groups.split(',') if current_groups else []

            # 新しいグループの情報を入力
            group_name = input("参加するグループの名前を入力してください: ")
            group_password = input(f"{group_name} のパスワードを入力してください: ")

            # グループの存在確認と認証
            cursor.execute('''
            SELECT unique_id, e_mail FROM Group_table 
            WHERE name = ? AND password = ?
            ''', (group_name, group_password))
            group_data = cursor.fetchone()

            if group_data:
                new_group_id, group_emails = group_data
                group_email_list = group_emails.split(',') if group_emails else []

                if user_email in group_email_list:
                    if new_group_id not in current_group_list:
                        current_group_list.append(new_group_id)
                        updated_groups = ','.join(current_group_list)

                        # ユーザーの所属グループを更新
                        cursor.execute('''
                        UPDATE User SET group_unique_ids = ? WHERE unique_id = ?
                        ''', (updated_groups, user_id))
                        conn.commit()
                        print(f"ユーザー '{username}' を グループ '{group_name}' に正常に追加しました。")
                    else:
                        print(f"ユーザーはすでにグループ '{group_name}' に所属しています。")
                else:
                    print("ユーザーのメールアドレスがグループのメールアドレスリストに含まれていません。")
            else:
                print("グループ名またはパスワードが正しくありません。")
        else:
            print("ユーザー名またはパスワードが正しくありません。")
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        conn.close()

# 関数を実行
if __name__ == "__main__":
    add_user_to_group()