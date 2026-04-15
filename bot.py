import os
import subprocess
import telebot

# Получаем токен из настроек Railway (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Создаем файл с флагом при запуске, если его нет
FLAG_PATH = "flag.txt"
if not os.path.exists(FLAG_PATH):
    with open(FLAG_PATH, "w") as f:
        f.write("CTF{Wh0_1s_Tyr3ll_W3ll1k}")

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "<b>Remote Network Diagnostic Tool v1.2</b>\n\n"
        "Система готова к работе.\n"
        "Используйте: /check_host [IP/Domain]"
    )
    bot.reply_to(message, welcome, parse_mode="HTML")

@bot.message_handler(commands=['check_host'])
def check_host(message):
    try:
        msg_parts = message.text.split(maxsplit=1)
        if len(msg_parts) < 2:
            bot.reply_to(message, "Ошибка: укажите цель. Пример: /check_host google.com")
            return
        
        target = msg_parts[1]
        
        # УЯЗВИМОСТЬ: Специально оставлена для CTF
        command = f"ping -c 1 {target}"
        
        # Выполнение команды в системе Railway
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
        bot.reply_to(message, f"Ошибка сервера: {str(e)}")

if __name__ == "__main__":
    print("Бот запущен на Railway...")
    bot.polling(none_stop=True)
