import requests
import time
from datetime import datetime
import base64
from keep_alive import keep_alive

# Configurações
USERNAME = 'danilocarreira05@gmail.com'
PASSWORD = 'PN11pn12'
TELEGRAM_TOKEN = '7315146387:AAEBInz6R-3P69zgw5vLF2U2pCIyoGjSM44'
CHAT_ID = '860219273'
DROP_THRESHOLD = 0.10  # 10% de queda
CHECK_INTERVAL = 60  # a cada 60 segundos

API_URL = 'https://api.pinnacle.com/v1/odds?sportId=29'  # Exemplo: Esports FIFA

def get_auth_header():
    creds = f"{USERNAME}:{PASSWORD}"
    b64 = base64.b64encode(creds.encode()).decode()
    return {'Authorization': f'Basic {b64}'}

previous_odds = {}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data=data)

keep_alive()

while True:
    try:
        headers = get_auth_header()
        response = requests.get(API_URL, headers=headers)
        data = response.json()

        for league in data.get('leagues', []):
            for event in league.get('events', []):
                event_id = event['id']
                home = event['home']
                away = event['away']

                for period in event.get('periods', []):
                    if 'moneyline' in period:
                        for team in ['home', 'away']:
                            key = f"{event_id}_{team}"
                            current_odd = period['moneyline'][team]

                            if key in previous_odds:
                                old_odd = previous_odds[key]
                                if old_odd and current_odd:
                                    drop = (old_odd - current_odd) / old_odd
                                    if drop >= DROP_THRESHOLD:
                                        msg = (
                                            f"📉 *Drop de Odds Detectado!*\n\n"

                                            f"🏆 {home} vs {away}\n"

                                            f"🎯 Time: {team.upper()}\n"

                                            f"💸 Odd caiu de {old_odd:.2f} para {current_odd:.2f} (-{drop*100:.1f}%)\n"

                                            f"🕒 {datetime.now().strftime('%H:%M:%S')}"
                                        )
                                        send_telegram_message(msg)

                            previous_odds[key] = current_odd
                            send_telegram_message("🚨 Bot ativo e alerta de teste funcionando.")

    except Exception as e:
        print("Erro:", e)

    time.sleep(CHECK_INTERVAL)
