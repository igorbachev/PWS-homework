"""модуль поиска ближайшего к пользователю атлета. Логика работы модуля такова:

*    запросить идентификатор пользователя;
*    если пользователь с таким идентификатором существует в таблице user, то вывести на экран двух атлетов: ближайшего
по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
*    если пользователя с таким идентификатором нет, вывести соответствующее сообщение.

Все данные о пользователях хранятся в таблице user базы данных sochi_athletes.sqlite3
"""

# подключаем внешнюю библиотеку SQLAlchemy и даем ей псевдоним sa
import sqlalchemy as sa
# библиотека SQLAlchemy должна быть установлена в системе
# установки внешней библиотеки. Запускаем команду pip install sqlalchemy:

from sqlalchemy.orm import sessionmaker
# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base
# подключаем модуль работы с датами
import datetime


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


class Athelete(Base):
    """
    Описывает структуру таблицы athelete, содержащую данные об атлетах
    """
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def request_data():
    """
    Запрашивает у пользователя данные
    """
    # выводим приветствие
    print("Привет! найдем ближайших атлетов для пользователя с ID")
    # запрашиваем у пользователя данные
    user_id = input("Введи идентификатор пользователя: ")
    return int(user_id)


def str2date(date_str):
    """
    Конвертирует строку с датой рождения, в формате ГГГГ-ММ-ДД, в объект datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def find_birthdate(user, session):
    """
    поиск атлета с самой маленькой разницей в возрасте
    :param user: идентификатор пользователя, с которым сверяемся
    :param session: сессия к БД
    :return: ID атлета, ближайшая дата рождения к ДР пользователя
    """
    # получили список строк таблицы атлетов
    athelete_lst = session.query(Athelete).all()
    athlete_dic = {}
    # преобразуем список в словарь
    for athelete in athelete_lst:
        birthdate = str2date(athelete.birthdate)
        athlete_dic[athelete.id] = birthdate
    user_birthdate = str2date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_birthdate = None
    # ищем минимальный срок между датами рождения
    for key, birthdate in athlete_dic.items():
        dist = abs(user_birthdate - birthdate)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = key
            athlete_birthdate = birthdate
    return athlete_id, athlete_birthdate


def find_height(user, session):
    """
    поиск атлета с самой маленькой разницей в росте
    :param user: идентификатор пользователя, с которым сверяемся
    :param session: сессия к БД
    :return: ID атлета, ближайший рост атлета
    """
    # получили список строк таблицы атлетов
    # рост некоторых атлетов не указан в БД т.е. поле имеет значение None, отфильтруем их
    athletes_lst = session.query(Athelete).filter(Athelete.height != None).all()
    # преобразуем список в словарь
    athlete_dic = {athlete.id: athlete.height for athlete in athletes_lst}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for key, height in athlete_dic.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = key
            athlete_height = height

    return athlete_id, athlete_height


def main():
    """
    Основной блок программы
    """
    session = connect_db()
    user_id = request_data()
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром user_id
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя нет в базе")
    else:
        # получаем: ID атлета с ближайшей датой рождения, дату рождения
        id_birthdate, birthdate = find_birthdate(user, session)
        print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(id_birthdate, birthdate))
        id_height, height = find_height(user, session)
        print("Ближайший по росту атлет: {}, его рост: {}".format(id_height, height))

if __name__ == '__main__':
    # пример работы программы
    main()
    # date_str = str2date('1099-12-01')
    # print(date_str, type(date_str))
