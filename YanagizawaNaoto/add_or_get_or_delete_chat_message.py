import sqlite3

def add_data(group_id, content, page, file_name):
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        # データを挿入
        cursor.execute('''
        INSERT INTO Data (content, group_unique_id, page, file_name)
        VALUES (?, ?, ?, ?)
        ''', (content, group_id, page, file_name))

        conn.commit()
        print(f"データが正常に追加されました。ファイル名: {file_name}")
        return cursor.lastrowid  # 挿入されたデータのIDを返す

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        conn.close()

def delete_data(data_id):
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        # データが存在するか確認
        cursor.execute('SELECT file_name FROM Data WHERE rowid = ?', (data_id,))
        result = cursor.fetchone()

        if result:
            # データを削除
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

def get_data(group_id=None, page=None, file_name=None):
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    try:
        query = 'SELECT rowid, * FROM Data WHERE 1=1'
        params = []

        if group_id:
            query += ' AND group_unique_id = ?'
            params.append(group_id)
        if page:
            query += ' AND page = ?'
            params.append(page)
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

# 使用例
if __name__ == "__main__":
    # データを追加
    new_data_id = add_data('group123', 'これはテストデータです。', 1, 'test.txt')

    # データを取得
    get_data(group_id='group123')

    # データを削除
    if new_data_id:
        delete_data(new_data_id)

    # 削除後のデータを確認
    get_data(group_id='group123')