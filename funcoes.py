import spacy
import requests
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import datetime as dt
from inserir_tokens import token_openweathermap

stop_words = set(stopwords.words("portuguese"))
nlp = spacy.load("pt_core_news_sm")

resposta_a = "Em {}, a temperatura de agora está de {}°C, com sensação térmica de {}°C. Mais tarde, chegaremos a {}°C! O tempo está marcado como: {}, e, ainda hoje, a previsão também é: {}.\n"
resposta_b = "Para amanhã, a previsão do tempo é de {}°C e {} em {}.\n"
resposta_c = "Segue a previsão do tempo para os próximos cinco dias nessa semana: {}.\n"

respostas = [resposta_a, resposta_b, resposta_c]

horas = ["horas", "horário", "quando"]

palavras = ["tempo", "calor", "frio", "chuva", "sol", "vento", "graus", "chover",
            "ventar", "temperatura", "hoje", "amanhã", "semana", "nublado", 
            "clima", "nevar", "neve", "previsão", "chovendo", "agora",
            "ventando", "temporal", "umidade", "abafado", "calorzinho",
            "abafado", "dia"]

sentimento = ["tudo bem", "como você está", "como você tá", "tudo certo"]

afirmacoes = ["sim", "claro", "pode"]

def pegar_tempo_agora(cidade):
    url_agora = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&lang=pt_br&units=metric".format(cidade, token_openweathermap)
    res = requests.get(url_agora)
    data = res.json()
    temperatura = int(data["main"]["temp"])
    sensacao = int(data["main"]["feels_like"])
    situacao = data["weather"][0]["description"]
    return temperatura, sensacao, situacao

def pegar_tempo_futuro(date, cidade):
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
                        print(f"Dia: {str(amanha_str)[8:10]} | Temperatura: {temperatura}°C | Tempo: {situacao}.\n")
                        amanha_dt = amanha_dt + dt.timedelta(days=1)
                        amanha_str = str(amanha_dt)[0:10] + str(" 12:00:00")
        print("Todas as temperaturas são previsões para o horário do meio-dia")   
                     
def pegar_cidade(mensagem):
    city = ""
    frase = nlp(mensagem)
    global ent
    for ent in frase.ents:
        if ent.label_ == "LOC":
            try:
                pegar_tempo_agora(ent.text)
                city = "ok"
                return ent.text
            except KeyError:
                resp = input("Não consegui entender. Por favor, escreva o nome completo da cidade :D\n")
                return pegar_cidade(resp)
    if city == "":
        resp = input("Opa! Qual cidade?\n")
        return pegar_cidade(resp)


def pegar_nome(mensagem):
    nome = ""
    for token in nlp(mensagem):
        if token.pos_ == "PROPN":
            nome = token.text
    if nome == "":
        return nlp(mensagem)[-1].text.title()
    else:
        return nome.title()
    
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

