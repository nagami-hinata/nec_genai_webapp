import sqlite3

def add_data():
    group_id = input("データを追加するグループのIDを入力してください: ")
    content = input("データの内容を入力してください: ")
    page = int(input("ページ番号を入力してください: "))
    file_name = input("ファイル名を入力してください: ")

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO Data (content, group_unique_id, page, file_name)
        VALUES (?, ?, ?, ?)
        ''', (content, group_id, page, file_name))

        conn.commit()
        print(f"データが正常に追加されました。ファイル名: {file_name}")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return None
    finally:
        conn.close()

def get_data():
    group_id = input("データを取得するグループのIDを入力してください（省略可能）: ")
    page_input = input("ページ番号を入力してください（省略可能）: ")
    file_name = input("ファイル名を入力してください（省略可能）: ")

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        query = 'SELECT rowid, * FROM Data WHERE 1=1'
        params = []

        if group_id:
            query += ' AND group_unique_id = ?'
            params.append(group_id)
        if page_input:
            query += ' AND page = ?'
            params.append(int(page_input))
        if file_name:
            query += ' AND file_name = ?'
            params.append(file_name)

        cursor.execute(query, params)
        data = cursor.fetchall()

        if data:
            print("取得されたデータ:")
            for row in data:
                print(f"ID: {row[0]}, グループID: {row[2]}, ページ: {row[3]}, ファイル名: {row[4]}")
                print(f"内容: {row[1]}\n")
        else:
            print("条件に一致するデータが見つかりません。")

        return data
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return []
    finally:
        conn.close()

def delete_data():
    data_id = int(input("削除するデータのIDを入力してください: "))

    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT file_name FROM Data WHERE rowid = ?', (data_id,))
        result = cursor.fetchone()

        if result:
            cursor.execute('DELETE FROM Data WHERE rowid = ?', (data_id,))
            conn.commit()
            print(f"データが正常に削除されました。ファイル名: {result[0]}")
            return True
        else:
            print(f"ID {data_id} のデータが見つかりません。")
            return False
    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return False
    finally:
        conn.close()

def main():
    while True:
        print("\nデータ操作を選択してください:")
        print("1: データを追加")
        print("2: データを取得")
        print("3: データを削除")
        print("4: 終了")
        
        choice = input("選択してください (1/2/3/4): ")
        
        if choice == '1':
            add_data()
        elif choice == '2':
            get_data()
        elif choice == '3':
            delete_data()
        elif choice == '4':
            print("プログラムを終了します。")
            break
        else:
            print("無効な選択です。もう一度試してください。")

if __name__ == "__main__":
    main()