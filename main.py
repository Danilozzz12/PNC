import requests
import time
from datetime import datetime
import base64
import threading
from keep_alive import keep_alive

# Configurações
USERNAME = 'danilocarreira05@gmail.com'
PASSWORD = 'PN11pn12'
TELEGRAM_TOKEN = '7315146387:AAEBInz6R-3P69zgw5vLF2U2pCIyoGjSM44'
CHAT_ID = '860219273'
DROP_THRESHOLD = 0.10
CHECK_INTERVAL = 30

API_URL = 'https://api.pinnacle.com/v1/odds?sportId=29'

def get_auth_header():
    creds = f"{USERNAME}:{PASSWORD}"
    b64 = base64.b64encode(creds.encode()).decode()
    return {'Authorization': f'Basic {b64}'}

previous_odds = {}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data=data)

# Iniciar o servidor Flask numa thread separada
threading.Thread(target=keep_alive).start()

# Mensagem inicial
send_telegram_message("✅ Bot de odds ativo com sucesso.")

while True:
    print(f"[{datetime.now()}] 🔄 Início do ciclo de verificação")
    try:
        print(f"[{datetime.now()}] Verificando odds da Pinnacle...")

        headers = get_auth_header()
        response = requests.get(API_URL, headers=headers)
        data = response.json()

        print(f"[{datetime.now()}] ✅ Dados recebidos com sucesso.")

        for league in data.get('leagues', []):
            for event in league.get('events', []):
                event_id = event['id']
                home = event['home']
                away = event['away']

                for period in event.get('periods', []):
                    if 'moneyline' in period:
                        for team in ['home', 'away']:
                            key = f"{event_id}_{team}"
                            current_odd = period['moneyline'].get(team)
                            if current_odd is None:
                                continue

                            if key in previous_odds:
                                old_odd = previous_odds[key]
                                if old_odd:
                                    drop = (old_odd - current_odd) / old_odd
                                    if drop >= DROP_THRESHOLD:
                                        msg = (
                                            f"📉 *Drop de Odds Detectado!*\n\n"
                                            f"🏆 {home} vs {away}\n"
                                            f"🎯 Time: {team.upper()}\n"
                                            f"💸 Odd caiu de {old_odd:.2f} para {current_odd:.2f} (-{drop*100:.1f}%)\n"
                                            f"🕒 {datetime.now().strftime('%H:%M:%S')}"
                                        )
                                        print(f"[{datetime.now()}] 🚨 ALERTA ENVIADO: {msg}")
                                        send_telegram_message(msg)

                            previous_odds[key] = current_odd

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erro: {e}")

    print(f"[{datetime.now()}] ⏳ A dormir {CHECK_INTERVAL}s até à próxima verificação...\n")
    time.sleep(CHECK_INTERVAL)
