import sqlite3

# データベースに接続（なければ作成される）
conn = sqlite3.connect('chat_app.db')
cursor = conn.cursor()

# Groupテーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS Group_table (
    name TEXT,
    password TEXT,
    unique_id TEXT PRIMARY KEY,
    e_mail TEXT
)
''')

# Userテーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    name TEXT,
    password TEXT,
    unique_id TEXT PRIMARY KEY,
    e_mail TEXT,
    last_page TEXT
)
''')

# UserGroupRoleテーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserGroupRole (
    user_id TEXT,
    group_id TEXT,
    role TEXT,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES User(unique_id),
    FOREIGN KEY (group_id) REFERENCES Group_table(unique_id)
)
''')

# Chatテーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS Chat (
    content TEXT,
    time_stamp TIMESTAMP,
    user_unique_id TEXT,
    is_user BOOLEAN,
    group_unique_id TEXT,
    FOREIGN KEY (user_unique_id) REFERENCES User(unique_id),
    FOREIGN KEY (group_unique_id) REFERENCES Group_table(unique_id)
)
''')

# Dataテーブルの作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS Data (
    content TEXT,
    group_unique_id TEXT,
    page INTEGER,
    file_name TEXT,
    FOREIGN KEY (group_unique_id) REFERENCES Group_table(unique_id)
)
''')

# 変更を保存し、接続を閉じる
conn.commit()
conn.close()

print("データベースとテーブルが正常に作成されました。")