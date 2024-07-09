import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Função para inicializar a conexão com o MongoDB
def get_mongo_client():
    username = "lennonmms7"
    password = "7d5b6r77"
    cluster_address = "teste.baoswin.mongodb.net"
    dbname = "teste" 
    # Certifique-se de que a senha está URL-encoded se contiver caracteres especiais
    DATABASE_URL = f"mongodb+srv://{username}:{password}@{cluster_address}/?retryWrites=true&w=majority&appName=teste"
    client = MongoClient(DATABASE_URL)
    return client

# Inicializar a conexão com o MongoDB
client = get_mongo_client()
db = client['teste']  
equipamentos_collection = db['equipamentos']

# Título da página
st.title('Adicionar Equipamento')

# Formulário para adicionar equipamentos
with st.form(key='add_equipamento'):
    nome = st.text_input('Motorista')
    quantidade = st.number_input('Quantidade Viagens', min_value=0, step=1)
    equipamento = st.text_input('Nome Equipamento')
    submit_button = st.form_submit_button(label='Adicionar')

    if submit_button:
        equipamentos_collection.insert_one({
            'nome': nome,
            'quantidade': quantidade,
            'equipamento': equipamento
        })
        st.success('Equipamento adicionado com sucesso!')

# Botão para excluir todos os dados
if st.button('Excluir Todos os Dados'):
    equipamentos_collection.delete_many({})
    st.warning('Todos os dados foram excluídos!')

# Exibir lista de equipamentos
equipamentos = list(equipamentos_collection.find())

if equipamentos:
    df = pd.DataFrame(equipamentos, columns=['_id', 'nome', 'quantidade', 'equipamento'])
    st.table(df)

    # Criar gráfico usando Plotly
    fig = px.bar(df, x='equipamento', y='quantidade', color='nome', title='Quantidade de Equipamentos por Nome')
    st.plotly_chart(fig)
else:
    st.write('Nenhum equipamento adicionado.')

# Botão para exportar dados para Excel
if st.button('Exportar para Excel'):
    df = pd.DataFrame(equipamentos)
    file_path = 'equipamentos.xlsx'
    df.to_excel(file_path, index=False)

    with open(file_path, 'rb') as file:
        st.download_button(label='Download Excel', data=file, file_name='equipamentos.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
