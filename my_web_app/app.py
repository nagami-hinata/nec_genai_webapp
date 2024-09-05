from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import uuid
import bcrypt
import PyPDF2
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('chat_app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user-name']
        email = request.form['e-mail']
        password = request.form['password']
        group_unique_ids = request.form['group-id']

        # パスワードをハッシュ化
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # ユニークIDの生成
        unique_id = str(uuid.uuid4())

        # データベース接続
        conn = get_db_connection()
        cur = conn.cursor()

        # Group_tableにgroup_unique_idが存在するか確認
        cur.execute("SELECT COUNT(*) FROM Group_table WHERE unique_id = ?", (group_unique_ids,))
        if cur.fetchone()[0] == 0:
            conn.close()
            flash("入力されたグループIDは存在しません。")
            return redirect(url_for('register'))

        # Userテーブルにデータを挿入
        cur.execute('''
            INSERT INTO User (name, password, unique_id, e_mail, last_page, group_unique_ids, tag)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_name, hashed_password, unique_id, email, None, group_unique_ids, None))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['e-mail']
        password = request.form['password']

        # データベース接続
        conn = get_db_connection()
        cur = conn.cursor()

        # Userテーブルからメールアドレスでユーザー情報を取得
        cur.execute("SELECT * FROM User WHERE e_mail = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if user is None:
            flash('メールアドレスが見つかりません。')
            return redirect(url_for('login'))

        # パスワードの照合
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # 認証成功時にセッション情報を保持
            # session['user_id'] = user['unique_id']
            return redirect(url_for('chatpage'))
        else:
            flash('パスワードが間違っています。')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/author_register', methods=['GET', 'POST'])
def author_register():
    if request.method == 'POST':
        company_name = request.form['user-name']
        email = request.form['e-mail']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Generate a unique ID
        unique_id = str(uuid.uuid4())

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the Group_table
        cur.execute('''
            INSERT INTO Group_table (name, e_mail, password, unique_id, leader_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (company_name, email, hashed_password, unique_id, None))

        conn.commit()
        conn.close()

        return redirect(url_for('author_login'))

    return render_template('author_register.html')

@app.route('/author_login', methods=['GET', 'POST'])
def author_login():
    if request.method == 'POST':
        email = request.form['e-mail']
        password = request.form['password']

        # データベース接続
        conn = get_db_connection()
        cur = conn.cursor()

        # Group_tableからメールアドレスでグループ情報を取得
        cur.execute("SELECT * FROM Group_table WHERE e_mail = ?", (email,))
        group = cur.fetchone()
        conn.close()

        if group is None:
            flash('メールアドレスが見つかりません。')
            return redirect(url_for('author_login'))

        # パスワードの照合
        if bcrypt.checkpw(password.encode('utf-8'), group['password']):
            # 認証成功時にセッション情報を保持
            # session['group_id'] = group['unique_id']
            return redirect(url_for('chatpage'))
        else:
            flash('パスワードが間違っています。')
            return redirect(url_for('author_login'))

    return render_template('author_login.html')

@app.route('/chatpage')
def chatpage():
    return render_template('chatpage.html')

@app.route('/data_reference')
def data_reference():
    conn = get_db_connection()
    cur = conn.cursor()

    # pageが1のファイルのみを取得
    cur.execute('SELECT * FROM Data WHERE page = 1')
    data_files = cur.fetchall()
    conn.close()

    return render_template('data_reference.html', data_files=data_files)

@app.route('/tag_edit', methods=['GET', 'POST'])
def tag_edit():
    if request.method == 'POST':
        # アップロードされたファイルを取得
        if 'file' not in request.files:
            flash('ファイルが選択されていません。')
            return redirect(url_for('tag_edit'))

        uploaded_file = request.files['file']
        
        if uploaded_file.filename == '':
            flash('ファイルが選択されていません。')
            return redirect(url_for('tag_edit'))

        if not uploaded_file.filename.endswith('.pdf'):
            flash('PDFファイルのみが許可されています。')
            return redirect(url_for('tag_edit'))

        # PDFファイルを読み込み
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            # データベース接続を確立
            conn = get_db_connection()
            cur = conn.cursor()

            # 各ページからテキストを抽出し、データベースに保存
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text = page.extract_text()

                # 空白2つ以上と改行2つ以上をそれぞれ1つに置き換える
                if extracted_text:  # extracted_text が None ではないことを確認
                    extracted_text = re.sub(r'\s{2,}', ' ', extracted_text)  # 空白2つ以上を1つに
                    extracted_text = re.sub(r'\n{2,}', '\n', extracted_text)  # 改行2つ以上を1つに

                # データベースに保存 (page番号も保存)
                cur.execute('''
                    INSERT INTO Data (content, group_unique_id, folder_unique_id, page, file_name)
                    VALUES (?, NULL, NULL, ?, ?)
                ''', (extracted_text, page_num + 1, uploaded_file.filename))

            # コミットして接続を閉じる
            conn.commit()
            conn.close()

        except Exception as e:
            flash('PDFからテキストを抽出できませんでした。')
            return redirect(url_for('tag_edit'))

        flash('PDFからテキストが抽出され、保存されました。')
        return redirect(url_for('tag_edit'))

    return render_template('tag_edit.html')


@app.route('/user_edit')
def user_edit():
    return render_template('user_edit.html')

@app.route('/data_deleted')
def data_deleted():
    return render_template('data_deleted.html')

@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.form['message']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (?)", (message,))
    conn.commit()
    conn.close()
    return 'Message added successfully'

if __name__ == '__main__':
    app.run(debug=True)
