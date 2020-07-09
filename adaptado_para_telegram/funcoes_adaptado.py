import spacy
import requests
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import datetime as dt
import telepot
from inserir_tokens import token_telegram, token_openweathermap

telegram = telepot.Bot(token_telegram)

stop_words = set(stopwords.words("portuguese"))
nlp = spacy.load("pt_core_news_sm")

resposta_a = "Em {}, a temperatura de agora está de {}°C, com sensação térmica de {}°C. Mais tarde, chegaremos a {}°C! O tempo está marcado como: {}, e, para o resto do dia, a previsão é: {}."
resposta_b = "Para amanhã, a previsão do tempo é de {}°C e {} em {}."
resposta_c = "Segue a previsão do tempo para os próximos cinco dias nessa semana: {}."

respostas = [resposta_a, resposta_b, resposta_c]

palavras = ["tempo", "calor", "frio", "chuva", "sol", "vento", "graus", "chover",
            "ventar", "temperatura", "hoje", "amanhã", "semana", "nublado", 
            "clima", "nevar", "neve", "previsão", "chovendo", "agora",
            "ventando", "temporal", "umidade", "abafado", "calorzinho",
            "abafado", "dia", "quente"]

sentimento = ["tudo bem", "como você está", "como você tá", "tudo certo"]

afirmacoes = ["sim", "claro", "pode", "yes", "yep"]

horas = ["horas", "horário", "quando"]

agradecimento = ["obrigada", "obrigado", "agradeço", "valeu"]

def pegar_tempo_agora(cidade):
    url_agora = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&lang=pt_br&units=metric".format(cidade, token_openweathermap)
    res = requests.get(url_agora)
    data = res.json()
    temperatura = int(data["main"]["temp"])
    sensacao = int(data["main"]["feels_like"])
    situacao = data["weather"][0]["description"]
    return temperatura, sensacao, situacao

def pegar_tempo_futuro(date, cidade, chatID):
    url_futuro = "http://api.openweathermap.org/data/2.5/forecast?q={}&APPID={}&lang=pt_br&units=metric".format(cidade, token_openweathermap)
    res = requests.get(url_futuro)
    data = res.json()
    amanha_dt = dt.datetime.now() + dt.timedelta(days=1)
    amanha_str = str(amanha_dt)[0:10] + str(" 12:00:00")
    if date == "próximo":
        temperatura = int(data["list"][0]["main"]["temp"])
        sensacao = int(data["list"][0]["main"]["feels_like"])
        situacao = (data["list"][0]["weather"][0]["description"])
        return temperatura, sensacao, situacao        
    if date == "amanhã":
        for i in range(0,40):
            if data["list"][i]["dt_txt"] == amanha_str:
                        temperatura = int(data["list"][i]["main"]["temp"])
                        sensacao = int(data["list"][i]["main"]["feels_like"])
                        situacao = (data["list"][i]["weather"][0]["description"])
                        return temperatura, sensacao, situacao
    if date == "semana":
        for i in range(0,40):
            if data["list"][i]["dt_txt"] == amanha_str:
                        temperatura = int(data["list"][i]["main"]["temp"])
                        sensacao = int(data["list"][i]["main"]["feels_like"])
                        situacao = (data["list"][i]["weather"][0]["description"])
                        p = (f"Dia: {str(amanha_str)[8:10]} | Temperatura: {temperatura}°C | Tempo: {situacao}.")
                        telegram.sendMessage(chatID, p)
                        amanha_dt = amanha_dt + dt.timedelta(days=1)
                        amanha_str = str(amanha_dt)[0:10] + str(" 12:00:00")
        return "Todas as temperaturas e tempos são previsões para o horário do meio-dia."
    
def preprocessar(frase):
    frase = frase.lower()
    frase = re.sub(r'[^\w\s]','',frase)
    tokens = word_tokenize(frase)
    frase = [i for i in tokens if not i in stop_words]
    return(frase)

def comparar(mensagem, respostas):
    similares = 0
    for token in mensagem:
        if token in respostas:
              similares += 1
    return similares