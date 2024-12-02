from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Função para conexão com o banco de dados
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal
@app.route('/')
def index():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)  # Supondo que você tenha um template index.html

# Endpoint para atualizar status de células
@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    socketio.emit('update_status', data)  # Emite a atualização ao vivo para os gestores
    return jsonify(success=True)

# Inicializa o banco de dados
def setup():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    cell TEXT NOT NULL,
                    status TEXT NOT NULL)''')
    conn.close()

if __name__ == '__main__':
    with app.app_context():
        setup()  # Inicializa o banco de dados ao iniciar o app
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)