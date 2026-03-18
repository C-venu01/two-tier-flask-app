import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'admin')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'mydb')

mysql = MySQL(app)

# Create table on first request
@app.before_request
def create_table():
    # Only create once
    if not getattr(app, '_table_created', False):
        cur = mysql.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message VARCHAR(255) NOT NULL
            )
        ''')
        mysql.connection.commit()
        cur.close()
        app._table_created = True

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM messages')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=data)

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success', 'message': message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
