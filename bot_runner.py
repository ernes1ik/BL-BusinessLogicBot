from script.classes import BotLogic
from telegram.ext import Updater, CommandHandler
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def start(update, context):
    user = update.effective_user
    bot_logic.register_user(user.id, user.username, user.first_name, user.last_name)
    update.message.reply_text(bot_logic.get_welcome_message(user.id))


def help_command(update, context):
    update.message.reply_text(bot_logic.get_help_message())


def add_note(update, context):
    user_id = update.effective_user.id
    text = ' '.join(context.args)
    if not text:
        update.message.reply_text("Пожалуйста, укажите текст заметки")
        return

    note_id = bot_logic.add_note(user_id, text)
    update.message.reply_text(f"Заметка #{note_id} добавлена!")


def list_notes(update, context):
    user_id = update.effective_user.id
    notes = bot_logic.get_user_notes(user_id)
    if not notes:
        update.message.reply_text("У вас пока нет заметок")
        return

    response = "Ваши заметки:\n" + "\n".join(
        f"#{note['id']}: {note['text']} ({note['created_at']})"
        for note in notes
    )
    update.message.reply_text(response)


if __name__ == '__main__':
    # Инициализация бизнес-логики
    bot_logic = BotLogic()

    # Получение токена бота
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("Не задан BOT_TOKEN в переменных окружения!")
        exit(1)

    # Создание и настройка бота
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add_note", add_note))
    dp.add_handler(CommandHandler("notes", list_notes))

    # Запуск бота
    logger.info("Бот запущен и ожидает сообщений...")
    updater.start_polling()
    updater.idle()