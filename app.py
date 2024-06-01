from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            equipamento TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM equipamentos')
    equipamentos = cursor.fetchall()
    conn.close()

    # Criar DataFrame para o gráfico
    df = pd.DataFrame(equipamentos, columns=['ID', 'Nome', 'Quantidade', 'Equipamento'])

    # Criar gráfico usando Plotly
    if not df.empty:
        fig = px.bar(df, x='Equipamento', y='Quantidade', color='Nome', title='Quantidade de Equipamentos por Nome')
        graph_html = pio.to_html(fig, full_html=False)
    else:
        graph_html = ''

    return render_template('index.html', equipamentos=equipamentos, graph_html=graph_html)

@app.route('/add', methods=['POST'])
def add_equipamento():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    equipamento = request.form['equipamento']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO equipamentos (nome, quantidade, equipamento)
        VALUES (?, ?, ?)
    ''', (nome, quantidade, equipamento))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_equipamentos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipamentos')
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/export')
def export():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query('SELECT * FROM equipamentos', conn)
    conn.close()
    
    file_path = 'equipamentos.xlsx'
    df.to_excel(file_path, index=False)
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
