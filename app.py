import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Configurações do banco de dados
db_config = {
    'user': 'root',
    'password': 'UvsLRfnxzfIHdIZVdXkoiDEeKxwRxPgE',
    'host': 'containers-us-west-94.railway.app',
    'port': 29533,
    'database': 'railway'
}

# Função para inicializar o banco de dados
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            quantidade INT NOT NULL,
            equipamento VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
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
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO equipamentos (nome, quantidade, equipamento)
            VALUES (%s, %s, %s)
        ''', (nome, quantidade, equipamento))
        conn.commit()
        cursor.close()
        conn.close()
        st.success('Equipamento adicionado com sucesso!')

# Botão para excluir todos os dados
if st.button('Excluir Todos os Dados'):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM equipamentos')
    conn.commit()
    cursor.close()
    conn.close()
    st.warning('Todos os dados foram excluídos!')

# Exibir lista de equipamentos
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor.execute('SELECT * FROM equipamentos')
equipamentos = cursor.fetchall()
cursor.close()
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
    conn = mysql.connector.connect(**db_config)
    df = pd.read_sql('SELECT * FROM equipamentos', conn)
    conn.close()
    
    file_path = 'equipamentos.xlsx'
    df.to_excel(file_path, index=False)
    
    with open(file_path, 'rb') as file:
        st.download_button(label='Download Excel', data=file, file_name='equipamentos.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
