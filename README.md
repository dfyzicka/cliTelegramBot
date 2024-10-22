# Telegram CLI Bot

Telegram CLI Bot - это Telegram-бот, который позволяет выполнять команды на сервере через интерфейс Telegram. Он поддерживает алиасы для упрощения команд, а также имеет систему авторизации для повышения безопасности.

## Описание

Этот бот предназначен для пользователей, которые хотят управлять своим сервером через Telegram, используя простые алиасы для сложных команд. Он позволяет выполнять команды и получать результаты прямо в чате, что делает его удобным инструментом для администрирования и мониторинга.

## Функциональные возможности

- **Исполнение команд**: Выполняет команды на сервере, используя алиасы.
- **Алиасы**: Поддержка алиасов для сокращения ввода команд.
- **Авторизация**: Защита команд паролем с возможностью настройки интервалов запросов пароля.
- **Блокировка**: Блокировка пользователя после нескольких неправильных попыток ввода пароля.

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/dfyzicka/cliTelegramBot.git
2. **Сделайте файл бота исполняемым**:   
   ```bash
   cd cliTelegramBot/ &&  chmod +x clyBot.py
3. **Установите необходимые библиотеки**:
   ```bash
   pip install --upgrade --no-cache-dir -r requirements.txt
4. **Переименуйте файл ex.env в .env** 
   ```bash
   mv ex.env .env
5. **Добавьте необходимые переменные**
   ```bash
   nano .env

**Переменные окружения**
- TELEGRAM_BOT_TOKEN=ваш_токен_бота
- BOT_PASSWORD=ваш_пароль
- PASSWORD_INTERVAL=0  # Интервал запроса пароля (0: нет, -1: каждый раз, >0: через заданный интервал в секундах)
- MAX_ATTEMPTS=0       # Максимальное количество попыток ввода пароля (0: не ограничено)
- LOCKOUT_TIME=0       # Время блокировки в секундах после превышения попыток (0: без блокировки)

6. **Заполните список алиасов**
   ```bash
   nano aliases.txt
   
7. **Запустите бота**
   ```bash
   python3 clyBot.py

# Telegram CLI Bot

The Telegram CLI Bot allows users to execute commands on a server through a Telegram interface. It supports aliases for simplifying commands and includes an authorization system for enhanced security.

## Description

This bot is designed for users who want to manage their server via Telegram, using simple aliases for complex commands. It enables command execution and returns results directly in the chat, making it a convenient tool for administration and monitoring.

## Features

- **Command Execution:** Executes server commands using aliases.
- **Aliases:** Supports aliases for reduced command input.
- **Authorization:** Protects commands with a password and allows for configurable password request intervals.
- **Lockout:** Locks the user out after several incorrect password attempts.

## Installation

1. **Clone the repository:**:
   ```bash
   git clone https://github.com/dfyzicka/cliTelegramBot.git
2. **Make the bot file executable:**:   
   ```bash
   cd cliTelegramBot/ &&  chmod +x clyBot.py
3. **Install required libraries:**:
   ```bash
   pip install --upgrade --no-cache-dir -r requirements.txt
4. **Rename the ex.env file to .env:** 
   ```bash
   mv ex.env .env
5. **Add required variables:**
   ```bash
   nano .env

**Environment Variables**
- TELEGRAM_BOT_TOKEN=ваш_токен_бота
- BOT_PASSWORD=ваш_пароль
- PASSWORD_INTERVAL=0  # Password request interval (0: none, -1: every time, >0: after specified seconds)
- MAX_ATTEMPTS=0       # Maximum password attempts (0: unlimited)
- LOCKOUT_TIME=0       # Lockout time in seconds after exceeding attempts (0: no lockout)

6. **Fill in the aliases list:**
   ```bash
   nano aliases.txt
   
7. **Run the bot:**
   ```bash
   python3 clyBot.py




