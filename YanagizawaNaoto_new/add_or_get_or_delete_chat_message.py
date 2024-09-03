import sqlite3
from datetime import datetime

def add_chat_message():
    content = input("メッセージ内容を入力してください: ")
    user_id = input("あなたのユーザーIDを入力してください: ")
    group_id = input("グループIDを入力してください: ")
    is_user = True  # ユーザーからの入力なので常にTrue
    thread_number = int(input("スレッド番号を入力してください: "))

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO Chat (content, time_stamp, user_unique_id, is_user, group_unique_id, thread_number)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (content, timestamp, user_id, is_user, group_id, thread_number))
        conn.commit()
        print("チャットメッセージが正常に追加されました。")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return None
    finally:
        conn.close()

def get_chat_messages():
    group_id = input("メッセージを取得するグループIDを入力してください: ")
    thread_input = input("スレッド番号を入力してください（省略する場合は Enter）: ")
    thread_number = int(thread_input) if thread_input else None

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    try:
        query = '''
        SELECT Chat.rowid, Chat.content, Chat.time_stamp, Chat.user_unique_id, 
               Chat.is_user, Chat.group_unique_id, Chat.thread_number, User.name 
        FROM Chat 
        LEFT JOIN User ON Chat.user_unique_id = User.unique_id 
        WHERE Chat.group_unique_id = ?
        '''
        params = [group_id]
        if thread_number is not None:
            query += ' AND Chat.thread_number = ?'
            params.append(thread_number)
        query += ' ORDER BY Chat.time_stamp ASC'
        cursor.execute(query, params)
        messages = cursor.fetchall()
        if messages:
            print("取得されたチャットメッセージ:")
            for msg in messages:
                print(f"ID: {msg[0]}, 内容: {msg[1]}, 時間: {msg[2]}, "
                      f"ユーザーID: {msg[3]}, スレッド番号: {msg[6]}, "
                      f"ユーザー名: {msg[7] if msg[7] else '不明'}")
                print("-" * 50)
        else:
            print("条件に一致するチャットメッセージが見つかりません。")
        return messages
    except sqlite3.Error as e:
        print(f"データベースエラーが発生しました: {e}")
        return []
    finally:
        conn.close()

def delete_chat_message():
    message_id = int(input("削除するメッセージのIDを入力してください: "))
    user_id = input("あなたのユーザーIDを入力してください: ")

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT user_unique_id FROM Chat 
        WHERE rowid = ?
        ''', (message_id,))
        result = cursor.fetchone()
        
        if result and result[0] == user_id:
            cursor.execute('DELETE FROM Chat WHERE rowid = ?', (message_id,))
            conn.commit()
            print(f"メッセージ（ID: {message_id}）が正常に削除されました。")
            return True
        elif result:
            print("このメッセージを削除する権限がありません。")
            return False
        else:
            print(f"ID {message_id} のメッセージが見つかりません。")
            return False
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return False
    finally:
        conn.close()

def main():
    while True:
        print("\nチャット操作を選択してください:")
        print("1: メッセージを追加")
        print("2: メッセージを取得")
        print("3: メッセージを削除")
        print("4: 終了")
        
        choice = input("選択してください (1/2/3/4): ")
        
        if choice == '1':
            add_chat_message()
        elif choice == '2':
            get_chat_messages()
        elif choice == '3':
            delete_chat_message()
        elif choice == '4':
            print("プログラムを終了します。")
            break
        else:
            print("無効な選択です。もう一度試してください。")

if __name__ == "__main__":
    main()