import openai
import base64
import streamlit as st
#import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components
import json
import pickle
import re

from senha import API_KEY
from itertools import zip_longest
#from pandasai import PandasAI
#from pandasai.llm.openai import OpenAI
from st_aggrid import AgGrid


#video https://www.youtube.com/watch?v=vw0I8i7QJRk

# Configurar a API do OpenAI
openai.api_key = st.secrets["auth_token"]





#configurações do background de fundo//////////////////////////////////////////////////////////////////////////////////
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("bad.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://wallpapers.com/images/featured/dexter-fe9qbtzm9bbv0xxj.jpg");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:bad/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
#st.title("It's summer!")
#st.sidebar.header("Configuration")



#/////////////////////////////////////////////////////////////////////////////////////////////

#---------------------------aqui começa a cofiguração da api-------------------------------------------




df = pd.DataFrame()
Resposta = pd.DataFrame()
# Texto fixo para concatenação
texto_fixo = "crie um codigo python usando a biblioteca pandas para criar um df  com 9 recomendações similares de series, quero no df as seguintes colunas ,nome:,Nota média IMDB:"
# Função para fazer a requisição à API
def obter_resposta(texto):
    input_text = texto_fixo + texto
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        max_tokens=500,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15,
    )
    return response.choices[0].text.strip()

# Configuração do Streamlit
st.title("Quer recomendações de series?")
user_input = st.text_input("Digite o nome da serie que deseja")

# Concatenar o texto do usuário com o texto fixo
texto_completo = texto_fixo + user_input

# Fazer a requisição à API e obter a resposta
if user_input:
    resposta_api = obter_resposta(texto_completo)

    # Exibir a resposta em um DataFrame
    data = {
        'Resposta': [resposta_api]
    }
    df = pd.DataFrame(data)
    

# Executar o código existente e criar um novo DataFrame
namespace = {}
exec(df['Resposta'][0], namespace)
new_df = namespace['df']

# Exibir o novo DataFrame na tela
#st.write("Novo DataFrame:")
#st.dataframe(new_df)

df2 = new_df

df3 = pd.read_excel('dados_series.xlsx')
#df3

#------------------------------------------------------------------
# Fazendo o join entre df2 e df3 na coluna 'Nome' e selecionando as colunas desejadas
colunas_desejadas = ['Nome', 'Nota média IMDB', 'imagem_url','sinopse']
novo_df = df2.merge(df3, left_on='Nome', right_on='nome')[colunas_desejadas]
#exibir o df na tela
#novo_df

#----------------------------------------------------------------------
#plotanto o grafico
# Plotando o gráfico de barras

#------------------------descomentar---------------------------------------------------------------
#fig = px.bar(novo_df, x='Nota média IMDB', y='Nome', orientation='h', text='Nota média IMDB')

# Configurações do layout do gráfico
#fig.update_layout(
#    title='Notas Médias IMDB por Nome',
#   xaxis_title='Nota Média IMDB',
#    yaxis_title='Nome',
#    yaxis_categoryorder='total ascending',
#    showlegend=False
#)

# Exibindo o gráfico no Streamlit
#st.plotly_chart(fig)
#---------------aqui é feito os filtros dos dados a serem exibidos------------------------------
# Função para obter nome ou retornar 0 se a linha não existir
def obter_nome (novo_df, indice):
    try:
        return novo_df.loc[indice, 'Nome']
    except KeyError:
        return 'Fim'
#nomes
nome_serie = obter_nome(novo_df, 0)
nome_serie1 = obter_nome(novo_df, 1)
nome_serie2 = obter_nome(novo_df, 2)
nome_serie3 = obter_nome(novo_df, 3)
nome_serie4 = obter_nome(novo_df, 4)
nome_serie5 = obter_nome(novo_df, 5)
nome_serie6 = obter_nome(novo_df, 6)
nome_serie7 = obter_nome(novo_df, 7)
nome_serie8 = obter_nome(novo_df, 8)



#imdb
# Função para obter a média IMDB ou retornar 0 se a linha não existir
def obter_media_imdb(novo_df, indice):
    try:
        return novo_df.loc[indice, 'Nota média IMDB']
    except KeyError:
        return 0
    
media_imdb = obter_media_imdb(novo_df, 0)
media_imdb_1 = obter_media_imdb(novo_df, 1)
media_imdb_2 = obter_media_imdb(novo_df, 2)
media_imdb_3 = obter_media_imdb(novo_df, 3)
media_imdb_4 = obter_media_imdb(novo_df, 4)
media_imdb_5 = obter_media_imdb(novo_df, 5)
media_imdb_6 = obter_media_imdb(novo_df, 6)
media_imdb_7 = obter_media_imdb(novo_df, 7)
media_imdb_8 = obter_media_imdb(novo_df, 8)

#imagem
# Função para obter a média IMDB ou retornar 0 se a linha não existir
def obter_imagem(novo_df, indice):
    try:
        return novo_df.loc[indice, 'imagem_url']
    except KeyError:
        return 'https://preview.redd.it/que-obra-do-entretenimento-te-deixou-meme-do-pablo-escobar-v0-m7fdtabj98la1.jpg?auto=webp&s=811797a6a6cbb0ae9d6995bfa05da149d03ca383'
    
imagem_url = obter_imagem(novo_df, 0)
imagem_url_1 = obter_imagem(novo_df, 1)
imagem_url_2 = obter_imagem(novo_df, 2)
imagem_url_3 = obter_imagem(novo_df, 3)
imagem_url_4 = obter_imagem(novo_df, 4)
imagem_url_5 = obter_imagem(novo_df, 5)
imagem_url_6 = obter_imagem(novo_df, 6)
imagem_url_7 = obter_imagem(novo_df, 7)
imagem_url_8 = obter_imagem(novo_df, 8)

#sinopse
def obter_sinopse(novo_df, indice):
    try:
        return novo_df.loc[indice, 'sinopse']
    except KeyError:
        return ''
    
sinopse   = obter_sinopse(novo_df, 0)
sinopse_1 = obter_sinopse(novo_df, 1)
sinopse_2 = obter_sinopse(novo_df, 2)
sinopse_3 = obter_sinopse(novo_df, 3)
sinopse_4 = obter_sinopse(novo_df, 4)
sinopse_5 = obter_sinopse(novo_df, 5)
sinopse_6 = obter_sinopse(novo_df, 6)
sinopse_7 = obter_sinopse(novo_df, 7)
sinopse_8 = obter_sinopse(novo_df, 8)



#----------------------------nessa parte está as configurações das colunas----------------------------------
#primeira parte das colunas
col1,col2,col3 = st.columns(3)
#coluna1
col1.subheader(nome_serie) #nome
col1.image(imagem_url) #imagem
col1.text('Nota média IMDB: ' + str(media_imdb))  #imdb
col1.text('Número de episodios:')
col1.text('Duração episodios:')  
col1.text('Data inico:')  #
col1.text('Data fim:')  
col1.text('Sinopse: '+ str(sinopse))  #sinopse


#coluna2
col2.subheader(nome_serie1) #nome
col2.image(imagem_url_1) #imagem
col2.text('Nota média IMDB: ' + str(media_imdb_1))  #imdb
col2.text('Número de episodios:')
col2.text('Duração episodios:')  
col2.text('Data inico:')  #
col2.text('Data fim:')   
col2.text('Sinopse: '+ str(sinopse_1))  #sinopse

#coluna3
col3.subheader(nome_serie2) #nome
col3.image(imagem_url_2) #imagem
col3.text('Nota média IMDB: ' + str(media_imdb_2))  #imdb
col3.text('Número de episodios:')
col3.text('Duração episodios:')  
col3.text('Data inico:')  #
col3.text('Data fim:')  
col3.text('Sinopse: '+ str(sinopse_2))  #sinopse

#segunda parte das colunas-------------------------------------------------------------------------
col4,col5,col6 = st.columns(3)
#coluna4
col4.subheader(nome_serie3) #nome
col4.image(imagem_url_3) #imagem
col4.text('Nota média IMDB: ' + str(media_imdb_3))  #imdb
col4.text('Número de episodios:')
col4.text('Duração episodios:')  
col4.text('Data inico:')  #
col4.text('Data fim:')  
col4.text('Sinopse: '+ str(sinopse_3))  #sinopse
#col1.text('IMDB: ' + str(IMDB_1))  #imdb
#col1.text('Data Inicio: ' +str(dt_inicio_1))  #inicio
#col1.text('Data Fim: '+ str(dt_fim_1))  #fim

#coluna5
col5.subheader(nome_serie4) #nome
col5.image(imagem_url_4) #imagem
col5.text('Nota média IMDB: ' + str(media_imdb_4))  #imdb
col5.text('Número de episodios:')
col5.text('Duração episodios:')  
col5.text('Data inico:')  #
col5.text('Data fim:')  
col5.text('Sinopse: '+ str(sinopse_4))  #sinopse

#coluna6
col6.subheader(nome_serie5) #nome
col6.image(imagem_url_5) #imagem
col6.text('Nota média IMDB: ' + str(media_imdb_5))  #imdb
col6.text('Número de episodios:')
col6.text('Duração episodios:')  
col6.text('Data inico:')  #
col6.text('Data fim:')  
col6.text('Sinopse: '+ str(sinopse_5))  #sinopse

#terceira parte das colunas-------------------------------------------------------------------------
col7,col8,col9 = st.columns(3)
#coluna7
col7.subheader(nome_serie6) #nome
col7.image(imagem_url_6) #imagem
col7.text('Nota média IMDB: ' + str(media_imdb_6))  #imdb
col7.text('Número de episodios:')
col7.text('Duração episodios:')  
col7.text('Data inico:')  #
col7.text('Data fim:')  
col7.text('Sinopse: '+ str(sinopse_6))  #sinopse
#col1.text('IMDB: ' + str(IMDB_1))  #imdb
#col1.text('Data Inicio: ' +str(dt_inicio_1))  #inicio
#col1.text('Data Fim: '+ str(dt_fim_1))  #fim

#coluna8
col8.subheader(nome_serie7) #nome
col8.image(imagem_url_7) #imagem
col8.text('Nota média IMDB: ' + str(media_imdb_7))  #imdb
col8.text('Número de episodios:')
col8.text('Duração episodios:')  
col8.text('Data inico:')  #
col8.text('Data fim:')  
col8.text('Sinopse: '+ str(sinopse_7))  #sinopse

#coluna9
col9.subheader(nome_serie8) #nome
col9.image(imagem_url_8) #imagem
col9.text('Nota média IMDB: ' + str(media_imdb_8))  #imdb
col9.text('Número de episodios:')
col9.text('Duração episodios:')  
col9.text('Data inico:')  #
col9.text('Data fim:')  
col9.text('Sinopse: '+ str(sinopse_8))  #sinopse

