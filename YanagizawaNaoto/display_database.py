import sqlite3
from prettytable import PrettyTable

def display_database_info():
    # データベースに接続
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # テーブル名のリストを取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\n--- {table_name} テーブル ---")

        # テーブルの列名を取得
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        # テーブルの内容を取得
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # PrettyTableを使用してテーブルを整形
        pt = PrettyTable()
        pt.field_names = columns
        for row in rows:
            pt.add_row(row)

        print(pt)

    conn.close()

# 関数を実行
display_database_info()