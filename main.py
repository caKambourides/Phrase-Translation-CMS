from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)

def init_db():
    #initialize the database
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            wordFirstLang TEXT NOT NULL,
            sentenceFirstLang TEXT NOT NULL,
            wordSecondLang TEXT NOT NULL,                   
            sentenceSecondLang TEXT NOT NULL
        )
    ''')
    conn.commit()
    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM entries")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        #load and insert json data
        with open('data.json', encoding="utf8") as f:
            data = json.load(f)
        for entry in data:
            cursor.execute('''
                INSERT INTO entries (id, wordFirstLang, sentenceFirstLang, wordSecondLang, sentenceSecondLang)
                VALUES (?, ?, ?, ?, ?)
            ''', (entry['id'], entry['wordFirstLang'], entry['sentenceFirstLang'], entry['wordSecondLang'], entry['sentenceSecondLang']))
    
    conn.commit()
    conn.close()



@app.route('/')
def index():
    #Display all entries
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    query = request.args.get('query')
    if not query:
        query = ""
    cursor.execute('SELECT id, wordFirstLang, wordSecondLang, sentenceFirstLang, sentenceSecondLang FROM entries WHERE wordFirstLang LIKE ? OR wordSecondLang LIKE ?', ('%' + query + '%', '%' + query + '%'))
    entries = cursor.fetchall()
    conn.close()
    page = request.args.get('page', 1, type=int)
    perPage = 10
    start = (page - 1) * perPage
    end = start + perPage
    totalPages = (len(entries) + perPage - 1) // perPage

    entries_to_display = entries[start:end]
    return render_template('index.html', entries=entries_to_display, page=page, totalPages=totalPages)


@app.route('/edit/<int:content_id>', methods=['GET', 'POST'])
def edit(content_id):
    #Edit an entry
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        wordFirstLang = request.form['wordFirstLang']
        wordSecondLang = request.form['wordSecondLang']
        sentenceFirstLang = request.form['sentenceFirstLang']
        sentenceSecondLang = request.form['sentenceSecondLang']

        cursor.execute('UPDATE entries SET wordFirstLang = ?, wordSecondLang = ?, sentenceFirstLang = ?, sentenceSecondLang = ? WHERE id = ?', (wordFirstLang, wordSecondLang, sentenceFirstLang, sentenceSecondLang, content_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT id, wordFirstLang, wordSecondLang, sentenceFirstLang, sentenceSecondLang FROM entries WHERE id = ?', (content_id,))
    entry = cursor.fetchone()
    conn.close()
    return render_template('edit.html', entry=entry, content_id=content_id)

@app.route('/add', methods=['GET', 'POST'])
def add():
    #Add a new entry
    if request.method == 'POST':
        wordFirstLang = request.form['wordFirstLang']
        wordSecondLang = request.form['wordSecondLang']
        sentenceFirstLang = request.form['sentenceFirstLang']
        sentenceSecondLang = request.form['sentenceSecondLang']

        conn = sqlite3.connect('cms.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (wordFirstLang, wordSecondLang, sentenceFirstLang, sentenceSecondLang) VALUES (?, ?, ?, ?)', (wordFirstLang, wordSecondLang, sentenceFirstLang, sentenceSecondLang))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:content_id>', methods=['GET', 'POST'])
def delete(content_id):
    #Delete a content entry.
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = ?', (content_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run()
