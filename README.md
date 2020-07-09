# chatbot-utilizando-NLP-e-API
Chatbot que pode ser acessado pelo Telegram ou terminal, com o objetivo de retornar a previsão do tempo.

## Pré requisitos
- Python 3
- Bibliotecas em <b>requirements.txt</b>
- Token para API do [OpenWeatherMap](https://openweathermap.org/api)
- Para versão do Telegram: Gerar token pelo [BotFather](https://web.telegram.org/#/im?p=@BotFather)

## Iniciando o programa
Basta rodar o arquivo <b>main.py</b> para a versão por terminal, ou <b>main_telegram.py</b> para a versão do Telegram.<br>
Não esqueça de, antes disso, inserir os tokens necessários no arquivo <b>inserir_tokens.py</b>, existente em ambas versões.

## Quais as diferenças da versão adaptada ao Telegram?
- Para aguardar uma resposta do usuário com a biblioteca Telepot é necessário criar condicionais - no código, indicadas por "step", ao invés de utilizar o input ([referência do desenvolvedor](https://github.com/nickoala/telepot/issues/209)).
- Algumas opções a mais que fazem sentido em aplicativos de mensagem de texto.

## Exemplos do chatbot funcionando
<img src="https://i.imgur.com/TBP0Vhs.jpg" height="450" width="260"> <img src="https://i.imgur.com/kcnxPQo.jpg" height="450" width="260"> <img src="https://i.imgur.com/sMH0sCJ.jpg" height="450" width="260">
