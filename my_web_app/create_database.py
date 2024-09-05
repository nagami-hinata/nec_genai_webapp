import sqlite3

def create_database():
    # データベースに接続（なければ作成される）
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()

    # Groupテーブルの作成（責任者の項目を含む）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Group_table (
        name TEXT,
        password TEXT,
        unique_id TEXT PRIMARY KEY,
        e_mail TEXT,
        leader_id TEXT,
        FOREIGN KEY (leader_id) REFERENCES User(unique_id)
    )
    ''')

    # Userテーブルの作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        name TEXT,
        password TEXT,
        unique_id TEXT PRIMARY KEY,
        e_mail TEXT,
        last_page TEXT,
        group_unique_ids TEXT,
        tag TEXT
    )
    ''')

    # Chatテーブルの作成（スレッド番号の項目を含む）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Chat (
        content TEXT,
        time_stamp TIMESTAMP,
        user_unique_id TEXT,
        is_user BOOLEAN,
        group_unique_id TEXT,
        thread_number INTEGER,
        FOREIGN KEY (user_unique_id) REFERENCES User(unique_id),
        FOREIGN KEY (group_unique_id) REFERENCES Group_table(unique_id)
    )
    ''')

    # Folderテーブルの構造（folder_nameを含む）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Folder (
        group_unique_id TEXT,
        folder_unique_id TEXT PRIMARY KEY,
        folder_name TEXT,
        FOREIGN KEY (group_unique_id) REFERENCES Group_table(unique_id)
    )
    ''')

    # Dataテーブルの作成（file_name、thread_number、tagを含む）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Data (
        content TEXT,
        group_unique_id TEXT,
        folder_unique_id TEXT,
        page INTEGER,
        file_name TEXT,
        thread_number INTEGER,
        tag TEXT,
        FOREIGN KEY (group_unique_id) REFERENCES Group_table(unique_id),
        FOREIGN KEY (folder_unique_id) REFERENCES Folder(folder_unique_id)
    )
    ''')

    # 変更を保存し、接続を閉じる
    conn.commit()
    conn.close()
    print("データベースとテーブルが正常に作成されました。")

if __name__ == "__main__":
    create_database()
