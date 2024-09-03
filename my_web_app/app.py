from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chat_app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')
"""
@app.route('/user_sign_up')
def other_page():
    return render_template('user_sign_up.html')

@app.route('/user_login')
def other_page():
    return render_template('user_login.html')

@app.route('/admin_sign_up')
def other_page():
    return render_template('admin_sign_up.html')

@app.route('/admin_login')
def other_page():
    return render_template('admin_login.html')

@app.route('/admin_sign_up')
def other_page():
    return render_template('admin_sign_up.html')
"""
@app.route('/chatpage')
def chatpage():
    return render_template('chatpage.html')
"""
@app.route('/admin_sign_up')
def other_page():
    return render_template('admin_sign_up.html')
"""

@app.route('/data_reference')
def data_reference():
    return render_template('data_reference.html')

@app.route('/tag_edit')
def tag_edit():
    return render_template('tag_edit.html')

@app.route('/data_deleted')
def data_deleted():
    return render_template('data_deleted.html')

# データベース操作の例
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