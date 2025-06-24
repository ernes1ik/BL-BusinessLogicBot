from script.classes import BotLogic
from script.db import init_db
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    # Инициализация базы данных
    init_db()

    # Создание экземпляра бизнес-логики
    bot_logic = BotLogic()

    logger.info("Бизнес-логика бота инициализирована")
    print(bot_logic.get_help_message())


if __name__ == '__main__':
    main()