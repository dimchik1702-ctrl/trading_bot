import requests
import time

# ТВОИ ДАННЫЕ
TOKEN = '8751950645:AAHfSB-tBuzm3JJbocqclZEdD3Nlbf1b9EI'
CHAT_ID = '406362799'

def send_signal(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'})
    except:
        print("Ошибка отправки в TG")

def get_fast_signals():
    # Ищем монеты с резким падением на MEXC
    try:
        res = requests.get("https://api.mexc.com/api/v3/ticker/24hr").json()
        for coin in res:
            symbol = coin['symbol']
            if not symbol.endswith('USDT'): continue
            
            change = float(coin['priceChangePercent'])
            volume = float(coin['quoteVolume'])
            
            # Условие: Слив > 15% при объеме > $500k
            if change < -15 and volume > 500000:
                price = coin['lastPrice']
                msg = (
                    f"🚨 **ОТСКОК (LONG): #{symbol}**\n"
                    f"Падение: `{change}%` (Дно?)\n"
                    f"Цена: `{price}`\n"
                    f"----------\n"
                    f"💰 **План для $8:**\n"
                    f"Вход на $1.5 (Изолированная 20x)\n"
                    f"Тейк: +1% цены (+20% к сделке)\n"
                    f"Стоп: -1% цены"
                )
                send_signal(msg)
                time.sleep(300) 
    except:
        print("Ошибка получения данных")

print("Снайпер запущен...")
while True:
    get_fast_signals()
    time.sleep(30)
