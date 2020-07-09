import random
from collections import Counter
from funcoes import pegar_nome, pegar_cidade, pegar_tempo_agora, pegar_tempo_futuro, resposta_a, resposta_b, resposta_c, respostas, preprocessar, comparar, palavras, sentimento, afirmacoes, horas

class Chatbot:
    def __init__(self):
        self.saidas = ["sair", "tchau", "cancelar", "adeus", "não", "até mais", 
                  "fim", "quit", "exit", "bye", "nop", "nao", "nope"]
        
    def conversar(self):
        mensagem = input("Olá! Meu nome é Jorge, e estou aqui para te ajudar! Qual o seu nome?\n")
        global nome 
        nome = pegar_nome(mensagem)
        mensagem = input(random.choice([f"Certo! Me pergunte sobre o tempo lá fora, {nome}.\n",
                                       f"Ok, {nome}! O que você gostaria de saber sobre previsão de tempo?\n",
                                       f"Legal conversar com você, {nome}. Me faça qualquer pergunta sobre previsão de tempo!\n",
                                       f"Legal, {nome}! Adoro falar sobre previsões do tempo, me faça uma pergunta sobre isso.\n"]))  
        while not self.sair(mensagem):
            mensagem = self.responder(mensagem)
                  
    def sair(self, mensagem):
        for saida in self.saidas:
            if saida in mensagem.lower():
                print(random.choice([f"Ok! Até mais, {nome} :)", f"Okay! Tchau, {nome}", 
                       f"Tudo bem! Abraços, {nome}", 
                       f"Tchau, {nome}! Tenha uma boa semana!"]))
                return True
            
    def responder(self, mensagem):   
        for h in horas:
            if h in mensagem.lower():
                return input("Ah, infelizmente ainda não consigo prever o tempo de acordo com cada horário, nem te retornar exatamente quando um fenômeno vai ocorrer. Para isso, recomendo que me pergunte sobre o resto dessa semana!")
        for palavra in palavras:
            if palavra in mensagem.lower():
                mensagem = self.analisar(palavra, mensagem)
                return input(mensagem)
        for palavra in sentimento:
            if palavra in mensagem.lower():
                return input("Estou muito bem, obrigada :) Como posso ajudar?\n")
        for palavra in afirmacoes:
            if palavra in mensagem.lower():
                return input(random.choice([f"Certo! Me pergunte sobre o tempo lá fora, {nome}.\n",
                                       f"Ok, {nome}! O que você gostaria de saber sobre previsão de tempo?\n",
                                       f"Legal conversar com você, {nome}. Me faça qualquer pergunta sobre previsão de tempo!\n",
                                       f"Legal, {nome}! Adoro falar sobre previsões do tempo, me faça uma pergunta sobre isso.\n"]))       
        return input(random.choice(["Hmmmm, parece que isso não é sobre previsão de tempo. Me pergunte algo sobre o dia lá fora!\n", 
                                    "Não consegui entender! Você poderia perguntar de outra forma?\n",
                                    "Parece que com isso não vou conseguir te ajudar. Me pergunte sobre a previsão do tempo!\n",
                                    "Não entendi muito bem, mas olha só essa curiosidade: Tempo refere-se a um estado momentâneo das condições atmosféricas. Já clima é duradouro, tratando-se de uma sucessão habitual de tempos. Legal, né?\n"]))
                    
    def pegar_melhor_resp(self, respostas, mensagem):
      contagem_perg = Counter(preprocessar(mensagem))
      resps_preprocessadas = [Counter(preprocessar(resposta)) for resposta in respostas]
      similaridade = [comparar(resposta, contagem_perg) for resposta in resps_preprocessadas]
      index_respostas = similaridade.index(max(similaridade))
      return respostas[index_respostas]
  
    def analisar(self, palavra, mensagem):
        global cidade
        global responder
        responder = ""
        cidade = pegar_cidade(mensagem)
        melhor_resposta = self.pegar_melhor_resp(respostas, mensagem)
        if melhor_resposta == resposta_a:
            responder = resposta_a.format(cidade.title(), pegar_tempo_agora(cidade)[0], pegar_tempo_agora(cidade)[1], pegar_tempo_futuro("próximo", cidade)[0], pegar_tempo_agora(cidade)[2], pegar_tempo_futuro("próximo", cidade)[2])
            print(responder)
        if melhor_resposta == resposta_b:
            responder = resposta_b.format(pegar_tempo_futuro("amanhã", cidade)[0], pegar_tempo_futuro("amanhã", cidade)[2], cidade.title())
            print(responder)
        if "chuva" in responder:
            print(random.choice(["Cuidado para não se molhar por aí!", "Se for sair, lembre-se de levar guarda-chuva :D"]))
        if "sol" in responder:
            print(random.choice(["Dia bonito, né?", "Bom pra pegar um solzinho."]))            
        if melhor_resposta == resposta_c:
            pegar_tempo_futuro("semana", cidade)
        return random.choice(["Posso ajudar em mais alguma coisa?\n", "Tem mais algo que posso ajudar?\n", "Você gostaria de fazer mais alguma pergunta?\n"])        
                               
Jorge = Chatbot()
Jorge.conversar()