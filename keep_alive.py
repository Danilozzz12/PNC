from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot está vivo!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

import threading
from main import start_bot_loop

threading.Thread(target=start_bot_loop).start()
