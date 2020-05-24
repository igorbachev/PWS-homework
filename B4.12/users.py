"""модуль users.py, регистрирует новых пользователей. Скрипт должен запрашивать следующие данные:
    имя
    фамилию
    пол
    адрес электронной почты
    дату рождения
    рост

Все данные о пользователях сохраните в таблице user нашей базы данных sochi_athletes.sqlite3."""
# подключаем внешнюю библиотеку SQLAlchemy и даем ей псевдоним sa
# библиотека SQLAlchemy должна быть установлена в системе
# установки внешней библиотеки. Запускаем команду pip install sqlalchemy:
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения  с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет, и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    return session()


class User(Base):
    """
    Описывает структуру таблицы user для хранения записей музыкальной библиотеки
    """
    # указываем имя таблицы
    __tablename__ = "user"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)

    # идентификатор строки
    id = sa.Column(sa.INTEGER, primary_key=True)
    # Имя
    first_name = sa.Column(sa.TEXT)
    # фамилию
    last_name = sa.Column(sa.TEXT)
    # пол
    gender = sa.Column(sa.TEXT)
    # адрес электронной почты
    email = sa.Column(sa.TEXT)
    # дата рождения
    birthdate = sa.Column(sa.TEXT)
    # рост
    height = sa.Column(sa.FLOAT)


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Какого ты пола? (варианты: Male, Female) ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    # дата рождения
    birthdate = input("Укажи дату своего рождения в формате ГГГГ-ММ-ДД. Например, 1999-01-01: ")
    height = input("Укажи свой рост, для разделения целой и десятичной части используй точку. Например, 1.65: ")
    # создаем кортеж с параметрами пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def main():
    """
    Основной блок программы
    """
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Твои данные сохранены в базе данных. Спасибо!")


if __name__ == '__main__':
    # пример работы программы
    main()
