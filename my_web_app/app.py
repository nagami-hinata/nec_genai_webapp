from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid
import bcrypt

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chat_app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
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
        
        return redirect(url_for('login'))
    
    return render_template('author_register.html')

@app.route('/author_login')
def author_login():
    return render_template('author_login.html')

@app.route('/chatpage')
def chatpage():
    return render_template('chatpage.html')

@app.route('/data_reference')
def data_reference():
    return render_template('data_reference.html')

@app.route('/tag_edit')
def tag_edit():
    return render_template('tag_edit.html')

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
