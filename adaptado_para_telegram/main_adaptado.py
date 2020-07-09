import random
from collections import Counter
from funcoes_adaptado import pegar_tempo_agora, pegar_tempo_futuro, resposta_a, resposta_b, resposta_c, respostas, preprocessar, comparar, palavras, sentimento, afirmacoes, horas, agradecimento
import telepot
import spacy
from inserir_tokens import token_telegram

telegram = telepot.Bot(token_telegram)

a = "Não consegui entender. Por favor, escreva o nome completo da cidade :D"

b = "Opa! Qual cidade?"

step = 0
class Chatbot:
    def __init__(self):
        self.saidas = ["sair", "tchau", "cancelar", "adeus", "não", "até mais", "fim", "quit", "exit", "bye", "nop", "nao", "nope"]
                              
    def responder(self, mensagem, chatID, nome):
        step = 1
        if step == 1:
            for h in horas:
                if h in mensagem.lower():
                    return "Ah, infelizmente ainda não consigo prever o tempo de acordo com cada horário, nem te retornar exatamente quando um fenômeno vai ocorrer. Para isso, recomendo que me pergunte sobre o resto dessa semana!"
        for palavra in palavras:
            if palavra in mensagem.lower():
                global msg
                msg = ""
                cidade = self.pegar_cidade(mensagem)        
                step = 2
                if step == 2:
                    if cidade == a:
                        msg = mensagem
                        return cidade
                    if cidade == b:
                        msg = mensagem
                        return cidade
                    melhor_resposta = self.analisar_melhor_resposta(mensagem, cidade, chatID)
                    telegram.sendMessage(chatID, melhor_resposta)
                    self.complemento(chatID, melhor_resposta)
                    return random.choice(["Posso ajudar em mais alguma coisa?", "Tem mais algo que posso ajudar?", "Você gostaria de fazer mais alguma pergunta?"])               
        if self.pegar_cidade(mensagem) != a and self.pegar_cidade(mensagem) != b and msg != "":
            telegram.sendMessage(chatID, "Certo! Só um momento.")
            cidade = self.pegar_cidade(mensagem)
            melhor_resposta = self.analisar_melhor_resposta(msg, cidade, chatID)
            telegram.sendMessage(chatID, melhor_resposta)
            self.complemento(chatID, melhor_resposta)
            msg = ""
            return random.choice(["Posso ajudar em mais alguma coisa?", "Tem mais algo que posso ajudar?", "Você gostaria de fazer mais alguma pergunta?"])               
        for palavra in sentimento:
            if palavra in mensagem.lower():
                step = 3
                if step == 3:
                    return "Estou muito bem, obrigado :) Como posso ajudar?"
        for palavra in afirmacoes:
            if palavra in mensagem.lower():
                step = 4
                if step == 4:
                    return random.choice([f"Certo! Me pergunte sobre o tempo lá fora, {nome}.",
                                           f"Ok, {nome}! O que você gostaria de saber sobre previsão de tempo?",
                                           f"Legal conversar com você, {nome}. Me faça qualquer pergunta sobre previsão de tempo!",
                                           f"Legal, {nome}! Adoro falar sobre previsões do tempo, me faça uma pergunta sobre isso."])
        step = 5
        if step == 5:
            for saida in self.saidas:
                if saida in mensagem.lower():
                    return random.choice([f"Ok! Até mais, {nome} :)", f"Okay! Tchau, {nome}", 
                           f"Tudo bem! Abraços, {nome}", 
                           f"Certo. Tchau, {nome}! Tenha uma boa semana!"])
        step = 6
        if step == 6:
            for agr in agradecimento:
                if agr in mensagem.lower():
                    return random.choice(["De nada, é um prazer falar com você!", "De nada, {nome}! Eu que agradeço por conversar comigo :)"])
        step = 7
        if step == 7:
            return random.choice(["Hmmmm, me parece que isso não é sobre previsão de tempo. Me pergunte algo sobre o dia lá fora!", 
                                        "Não consegui entender! Você poderia perguntar de outra forma?",
                                        "Parece que com isso não vou conseguir te ajudar. Me pergunte sobre a previsão do tempo!",
                                        "Não entendi muito bem, mas olha só essa curiosidade: Tempo refere-se a um estado momentâneo das condições atmosféricas. Já clima é duradouro, tratando-se de uma sucessão habitual de tempos. Legal, né?"])
                        
    def pegar_melhor_resp(self, respostas, mensagem):
      contagem_perg = Counter(preprocessar(mensagem))
      resps_preprocessadas = [Counter(preprocessar(resposta)) for resposta in respostas]
      similaridade = [comparar(resposta, contagem_perg) for resposta in resps_preprocessadas]
      index_respostas = similaridade.index(max(similaridade))
      return respostas[index_respostas]
    
    def pegar_cidade(self, mensagem):
        step = 8
        if step == 8:
            nlp = spacy.load("pt_core_news_sm")
            status = ""
            frase = nlp(mensagem)
            global ent
            for ent in frase.ents:
                if ent.label_ == "LOC":
                    try:
                        pegar_tempo_agora(ent.text)
                        city = ent.text
                        status = "ok"
                        return city
                    except KeyError:
                        return a
            if status == "":
                step = 9
                if step == 9:
                    return b
    
    def analisar_melhor_resposta(self, mensagem, cidade, chatID):
        melhor_resposta = self.pegar_melhor_resp(respostas, mensagem)
        step = 10
        if step == 10:
            if melhor_resposta == resposta_a:
                return resposta_a.format(cidade.title(), pegar_tempo_agora(cidade)[0], pegar_tempo_agora(cidade)[1], pegar_tempo_futuro("próximo", cidade, chatID)[0], pegar_tempo_agora(cidade)[2], pegar_tempo_futuro("próximo", cidade, chatID)[2])
            if melhor_resposta == resposta_b:
                return resposta_b.format(pegar_tempo_futuro("amanhã", cidade, chatID)[0], pegar_tempo_futuro("amanhã", cidade, chatID)[2], cidade.title())
            if melhor_resposta == resposta_c:
                return pegar_tempo_futuro("semana", cidade, chatID)                

    def complemento(self, chatID, responder):
        if "chuva" in responder:
            r = (random.choice(["Cuidado para não se molhar por aí!", "Se for sair, lembre-se de levar guarda-chuva :D"]))
            telegram.sendMessage(chatID, r)
        elif "sol" in responder:
            r = random.choice(["Dia bonito, né não?", "Tempo bom pra pegar um solzinho!"])
            telegram.sendMessage(chatID, r)
        elif "nublado" in responder:
            r = random.choice(["Segue uma curiosidade sobre dias nublados: Mesmo em um dia nublado, a radiação solar penetra nas nuvens. Não é à toa que, no verão, mesmo em dias de céu fechado, as pessoas podem ter queimação na pele. Pelo mesmo motivo, os painéis solares ainda produzem eletricidade em dias como esse. Interessante, né?", 
                                   "Poxa, parece que o sol não vai sair por enquanto!"])
            telegram.sendMessage(chatID, r)