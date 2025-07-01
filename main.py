import requests

TELEGRAM_TOKEN = '7315146387:AAEBInz6R-3P69zgw5vLF2U2pCIyoGjSM44'
CHAT_ID = '860219273'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

send_telegram_message("🚨 Teste de mensagem do bot")
