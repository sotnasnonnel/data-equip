import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

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

# Inicializar o banco de dados
init_db()

# Título da página
st.title('Adicionar Equipamento')

# Formulário para adicionar equipamentos
with st.form(key='add_equipamento'):
    nome = st.text_input('Motorista')
    quantidade = st.number_input('Quantidade Viagens', min_value=0, step=1)
    equipamento = st.text_input('Nome Equipamento')
    submit_button = st.form_submit_button(label='Adicionar')

    if submit_button:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO equipamentos (nome, quantidade, equipamento)
            VALUES (?, ?, ?)
        ''', (nome, quantidade, equipamento))
        conn.commit()
        conn.close()
        st.success('Equipamento adicionado com sucesso!')

# Botão para excluir todos os dados
if st.button('Excluir Todos os Dados'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipamentos')
    conn.commit()
    conn.close()
    st.warning('Todos os dados foram excluídos!')

# Exibir lista de equipamentos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM equipamentos')
equipamentos = cursor.fetchall()
conn.close()

if equipamentos:
    df = pd.DataFrame(equipamentos, columns=['ID', 'Nome', 'Quantidade', 'Equipamento'])
    st.table(df)

    # Criar gráfico usando Plotly
    fig = px.bar(df, x='Equipamento', y='Quantidade', color='Nome', title='Quantidade de Equipamentos por Nome')
    st.plotly_chart(fig)
else:
    st.write('Nenhum equipamento adicionado.')

# Botão para exportar dados para Excel
if st.button('Exportar para Excel'):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query('SELECT * FROM equipamentos', conn)
    conn.close()
    
    file_path = 'equipamentos.xlsx'
    df.to_excel(file_path, index=False)
    
    with open(file_path, 'rb') as file:
        st.download_button(label='Download Excel', data=file, file_name='equipamentos.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
