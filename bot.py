import os
import subprocess
import telebot

# 1. Получаем токен из переменных окружения Railway
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# 2. Автоматическое создание флага при запуске
FLAG_PATH = "flag.txt"
if not os.path.exists(FLAG_PATH):
    with open(FLAG_PATH, "w") as f:
        f.write("CTF{RAILWAY_COMMAND_INJECTION_SUCCESS_2026}")

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "<b>Remote Diagnostic Tool v1.2.2</b>\n\n"
        "Система активна. Модуль ECHO готов.\n"
        "Используйте: /check_host [IP/Domain]"
    )
    bot.reply_to(message, welcome, parse_mode="HTML")

@bot.message_handler(commands=['check_host'])
def check_host(message):
    try:
        # Извлекаем аргумент после команды
        msg_parts = message.text.split(maxsplit=1)
        if len(msg_parts) < 2:
            bot.reply_to(message, "Ошибка: не указана цель. Пример: /check_host 8.8.8.8")
            return
        
        target = msg_parts[1]
        
        # --- УЯЗВИМОСТЬ: OS Command Injection ---
        # Мы убрали кавычки вокруг {target}. 
        # Теперь команда ; cat flag.txt сработает напрямую.
        command = f"echo Testing connection to: {target}"
        
        # Выполняем в shell
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        output = stdout.decode('utf-8', errors='ignore')
        error_output = stderr.decode('utf-8', errors='ignore')
        
        final_output = output if output else error_output
        
        bot.send_message(
            message.chat.id, 
            f"Результат:\n<pre>{final_output[:4000]}</pre>", 
            parse_mode="HTML"
        )

    except Exception as e:
        bot.reply_to(message, f"Системный сбой: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен. Ожидание инъекций...")
    bot.polling(none_stop=True)
