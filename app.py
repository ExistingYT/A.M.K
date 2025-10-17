from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  author TEXT NOT NULL,
                  content TEXT NOT NULL,
                  date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Home route: Show posts and form
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT author, content, date FROM posts ORDER BY date DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=[{'author': p[0], 'content': p[1], 'date': p[2]} for p in posts])

# Submit route: Handle new posts
@app.route('/submit', methods=['POST'])
def submit():
    author = request.form['author'].strip()
    content = request.form['content'].strip()
    
    # Basic validation
    if not author or not content or len(author) > 50 or len(content) > 500:
        return "Invalid input. Name and post must not be empty and must be under 50 and 500 characters, respectively.", 400
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (author, content, date) VALUES (?, ?, ?)', (author, content, date))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)