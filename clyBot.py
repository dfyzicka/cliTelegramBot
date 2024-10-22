import logging
import subprocess
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена и пароля из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PASSWORD = os.getenv('BOT_PASSWORD')
PASSWORD_INTERVAL = int(os.getenv('PASSWORD_INTERVAL', 0))  # Интервал запроса пароля
MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', 0))  # Максимальное количество попыток
LOCKOUT_TIME = int(os.getenv('LOCKOUT_TIME', 0))  # Время блокировки

ALIASES_FILE = 'aliases.txt'
aliases = {}

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для загрузки алиасов из файла
def load_aliases(file_path):
    aliases = {}
    if not os.path.exists(file_path):
        logger.warning(f'Файл {file_path} не найден. Используются пустые алиасы.')
        return aliases
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                alias, command = line.split('=', 1)
                aliases[alias.strip()] = command.strip()
    return aliases

# Загрузка алиасов
aliases = load_aliases(ALIASES_FILE)

# Хранит состояние авторизации пользователя
user_authenticated = {}
user_attempts = {}
user_lockout_until = {}
pending_commands = {}  # Хранит ожидающие команды

# Настройка блокировки пользователя
def is_user_locked(user_id):
    return user_id in user_lockout_until and time.time() < user_lockout_until[user_id]

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Введи алиас для выполнения команды на сервере.')

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # Проверка блокировки пользователя
    if is_user_locked(user_id):
        remaining_time = user_lockout_until[user_id] - time.time()
        await update.message.reply_text(f'Ты заблокирован. Попробуй снова через {int(remaining_time)} секунд.')
        return

    # Проверяем, есть ли в тексте алиас
    if text in aliases:
        pending_commands[user_id] = text  # Сохраняем алиас для выполнения
        await update.message.reply_text('Введите пароль для выполнения команды.')
    elif user_id in pending_commands:
        # Если пользователь вводит пароль
        if text == PASSWORD:
            command = pending_commands.pop(user_id)  # Извлекаем алиас
            try:
                output = subprocess.check_output(aliases[command], shell=True, text=True)
                await update.message.reply_text(f'Вывод:\n{output}')
            except subprocess.CalledProcessError as e:
                await update.message.reply_text(f'Ошибка:\n{e.output}')
        else:
            # Увеличиваем количество попыток
            user_attempts[user_id] = user_attempts.get(user_id, 0) + 1
            if MAX_ATTEMPTS > 0 and user_attempts[user_id] >= MAX_ATTEMPTS:
                # Блокировка пользователя
                user_lockout_until[user_id] = time.time() + LOCKOUT_TIME
                await update.message.reply_text(f'Ты превысил количество попыток. Заблокирован на {LOCKOUT_TIME} секунд.')
            else:
                await update.message.reply_text('Неверный пароль. Попробуй еще раз.')
    else:
        await update.message.reply_text('Алиас не найден. Попробуй еще раз.')

# Основная функция
def main() -> None:
    if not TOKEN:
        logger.error('Токен не найден. Пожалуйста, добавьте его в .env файл.')
        return

    global aliases
    aliases = load_aliases(ALIASES_FILE)

    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
