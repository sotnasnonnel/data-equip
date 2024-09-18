import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient, errors
import requests

# Função para obter o IP público do servidor
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException:
        return None

# Função para inicializar a conexão com o MongoDB
def get_mongo_client():
    username = "lennonmms7"
    password = "7d5b6r77"
    cluster_address = "teste.baoswin.mongodb.net"
    dbname = "teste"
    DATABASE_URL = f"mongodb+srv://{username}:{password}@{cluster_address}/?retryWrites=true&w=majority&appName=teste"
    client = MongoClient(DATABASE_URL, serverSelectionTimeoutMS=5000)  # 5 segundos de timeout
    try:
        client.server_info()  # Forçar uma tentativa de conexão para capturar erros
        return client
    except errors.ServerSelectionTimeoutError as err:
        st.error(f"Erro ao conectar ao MongoDB: {err}")
        return None

# Obter o IP público do servidor e exibi-lo
public_ip = get_public_ip()
if public_ip:
    st.info(f"IP público do servidor: {public_ip}")
else:
    st.warning("Não foi possível obter o IP público do servidor.")

# Inicializar a conexão com o MongoDB
client = get_mongo_client()
if client:
    db = client['teste']  
    equipamentos_collection = db['equipamentos']

    # Título da página
    st.write('Essa página é um exemplo para adicionar equipamentos em uma base de dados SQL, e instantaneamente criado um gráfico, e é adicionada as informações em uma tabela.')
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
else:
    st.write("Não foi possível conectar ao MongoDB. Verifique suas credenciais e configurações.")
