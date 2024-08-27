import sqlite3

def add_user_to_group():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # ユーザー認証
    username = input("ユーザー名を入力してください: ")
    password = input("パスワードを入力してください: ")

    try:
        cursor.execute('''
        SELECT unique_id, e_mail FROM User 
        WHERE name = ? AND password = ?
        ''', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user_id, user_email = user_data

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
                    # ユーザーが既にグループに所属しているか確認
                    cursor.execute('''
                    SELECT role FROM UserGroupRole 
                    WHERE user_id = ? AND group_id = ?
                    ''', (user_id, new_group_id))
                    existing_role = cursor.fetchone()

                    if existing_role:
                        print(f"ユーザーはすでにグループ '{group_name}' に所属しています。役割: {existing_role[0]}")
                    else:
                        # ユーザーの役割を入力
                        role = input(f"{group_name} での役割を入力してください (member/admin): ")
                        
                        # ユーザーをグループに追加
                        cursor.execute('''
                        INSERT INTO UserGroupRole (user_id, group_id, role)
                        VALUES (?, ?, ?)
                        ''', (user_id, new_group_id, role))

                        conn.commit()
                        print(f"ユーザー '{username}' を グループ '{group_name}' に正常に追加しました。役割: {role}")
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
add_user_to_group()