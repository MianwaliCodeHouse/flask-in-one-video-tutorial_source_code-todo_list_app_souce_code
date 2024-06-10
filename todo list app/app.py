from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY id DESC")
    todos = cursor.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    description = request.form['description']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("UPDATE todos SET title = ?, description = ? WHERE id = ?", (title, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM todos WHERE id = ?", (id,))
        todo = cursor.fetchone()
        conn.close()
        return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
