import spacy
import streamlit as st
from gnews import GNews
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pytz import timezone

nlp = spacy.load("pt_core_news_sm")

def processar_texto(texto, periodo):
    google_news = GNews(language='pt', country='BR', period=(periodo[0]+'d'))
    news = google_news.get_news(texto)
    return pd.DataFrame(news)

def gerar_wordcloud(data, texto):
    text = " ".join(" ".join(token.text for token in nlp(review) if token.pos_ in ['NOUN', 'ADV']) for review in data)
    wordcloud = WordCloud(background_color='white', stopwords=set([texto])).generate(text)
    
    st.divider()
    st.subheader("Nuvem de palavras das manchetes")

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    


def grafico_fontes(data):

    publisher = {}
    publisher["title"] = []

    for p in data['publisher']:
        publisher["title"].append(p["title"])

    publisher_df = pd.DataFrame(publisher)


    st.divider()
    st.subheader("Fontes encontradas na pesquisa")
    st.bar_chart(publisher_df.groupby('title').size(),x_label="Fontes",y_label="Quantidade")

def grafico_hora(data):

    # Converter as strings de data e hora para datetime
    data['published date'] = pd.to_datetime(data['published date'], format='%a, %d %b %Y %H:%M:%S GMT')
    data['published date'] = data['published date'].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')

    # Extrair a hora
    data['hour'] = data['published date'].dt.hour

    # Contar o número de publicações por hora
    hourly_counts = data['hour'].value_counts().sort_index()


    # Criar os gráficos
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))


    # Histograma
    ax[0].bar(hourly_counts.index, hourly_counts.values, color='blue', alpha=0.7)
    ax[0].set_title('Histograma de Publicações por Hora')
    ax[0].set_xlabel('Hora do Dia')
    ax[0].set_ylabel('Número de Publicações')

    # Gráfico de linha
    ax[1].plot(hourly_counts.index, hourly_counts.values, marker='o', linestyle='-', color='green')
    ax[1].set_title('Gráfico de Linha de Publicações por Hora')
    ax[1].set_xlabel('Hora do Dia')
    ax[1].set_ylabel('Número de Publicações')

    
    st.divider()
    st.subheader("Concentraçaõ de notícias hora a hora")
    st.pyplot(fig)




st.title("Observatório de pesquisas no Google News")
texto_usuario = st.text_input('Chave para a pesquisa:')

periodo = st.select_slider(
    "Faixa de busca",
    options=[
        "1 dia",
        "2 dias",
        "3 dias",
        "4 dias",
        "5 dias",
        "6 dias",
        "7 dias",
    ],
)

if st.button('Processar'):
    # A função é chamada com o texto inserido pelo usuário quando o botão é clicado.
    if len(texto_usuario) != 0:
        data = processar_texto(texto_usuario, periodo)
        grafico_fontes(data)
        gerar_wordcloud(data["title"], texto_usuario)
        grafico_hora(data)
    else:
        st.info("É preciso informar uma palavra")


    
    