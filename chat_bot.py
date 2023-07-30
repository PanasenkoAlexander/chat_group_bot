import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import random
from datetime import datetime, timedelta
import threading


TOKEN = 'token'
bot = telebot.TeleBot(TOKEN)

# Идентификатор (chat_id) группы, куда нужно отправлять сообщения
group_id = 'chat_id'
# отправка в сразу несколько групп
# group_ids = ['chat_id', 'chat_id']


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я бот разработчика @shurik_python 👨🏼‍💻')


# Обработчик команды /get_group_id
@bot.message_handler(commands=['get_group_id'])
def get_group_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"The group chat_id is: {chat_id}")


# Функция для публикации поста с текстом в группе
def publish_post():
    greeting_variations = ["Приветствую", "Добрый день", "Здравствуйте", "Всем привет", "Привет народ", "Привет"]
    # Выбираем случайное приветствие
    random_greeting = random.choice(greeting_variations)
    post_text = f"{random_greeting}! Я разработчик ботов 🤖 на 🐍, по вопросам сотрудничества обращайтесь к @shurik_python 👨🏼‍💻 либо пишите в бота"
    # Отправляем сообщение в группу
    bot.send_message(group_id, post_text)
    # отправка в сразу несколько групп
    # for group_id in group_ids:
    #     bot.send_message(group_id, post_text)


# Функция для определения времени следующей публикации (в разное время каждый день)
def get_next_publish_time():
    # Получаем текущее время
    now = datetime.now()
    # Генерируем случайное время для следующей публикации (от 08:00 до 17:00)
    next_publish_time = now.replace(hour=random.randint(8, 17), minute=random.randint(0, 59))

    # Если текущее время позже сгенерированного, публикация будет на следующий день
    if now > next_publish_time:
        next_publish_time += timedelta(days=1)
    return next_publish_time


# Функция для запуска планировщика задач
def run_scheduler():
    # Выполнить первую публикацию сразу после запуска
    publish_post()

    scheduler = BackgroundScheduler()
    scheduler.add_job(publish_post, 'interval', days=1, start_date=get_next_publish_time())
    scheduler.start()


# Запуск планировщика задач в отдельном потоке
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

# Запускаем бота
print("\nБот запущен")
bot.polling()
