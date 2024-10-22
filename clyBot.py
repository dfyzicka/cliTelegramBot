import logging
import subprocess
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALIASES_FILE = 'aliases.txt'

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

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Введи алиас для выполнения команды на сервере.')

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    alias = update.message.text.strip()
    command = aliases.get(alias)

    if not command:
        await update.message.reply_text(f'Алиас "{alias}" не найден.')
        return

    try:
        # Выполнение команды
        output = subprocess.check_output(command, shell=True, text=True)
        await update.message.reply_text(f'Вывод:\n{output}')
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f'Ошибка:\n{e.output}')

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
    main()
