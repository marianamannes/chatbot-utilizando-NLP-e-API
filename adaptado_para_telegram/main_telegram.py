import telepot
from main_adaptado import Chatbot
import random
from telepot.loop import MessageLoop
from inserir_tokens import token_telegram

telegram = telepot.Bot(token_telegram)

saidas = ["sair", "tchau", "cancelar", "adeus", "não", "até mais", "fim", "quit", "exit", "bye", "nop", "nao", "nope"]

Jorge = Chatbot()

step = 1

def handle(msg):
   global step
   global chatID
   chatID = msg["chat"]["id"]
   global nome
   nome = msg["chat"]["first_name"]
   global mensagem
   mensagem = msg["text"]
   if step == 1 and mensagem == '/start':
       telegram.sendMessage(chatID, f"Olá, {nome}! Meu nome é Jorge, e estou aqui para te ajudar!")
       mensagem = random.choice(["Me pergunte sobre o tempo lá fora.",
                                       "O que você gostaria de saber sobre previsão de tempo?",
                                       "Me faça qualquer pergunta sobre previsão de tempo!",
                                       "Adoro falar sobre previsões do tempo, me faça uma pergunta sobre isso."])
       telegram.sendMessage(chatID, mensagem)
       step += 1
   elif step == 2 :   
       telegram.sendMessage(chatID, Jorge.responder(mensagem, chatID, nome))
              
def condicao():
    for saida in saidas:
        if saida in mensagem:
            return True

MessageLoop(telegram, handle).run_as_thread()

while True:
    pass