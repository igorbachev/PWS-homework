"""
веб-сервис, веб-приложения для ведения базы музыкальных альбомов.
требования к приложению:

1. принимает GET-запросы по адресу /albums/<artist> и выводит на экран сообщение с количеством альбомов
исполнителя artist и списком названий этих альбомов.
2. принимает POST-запросы по адресу /albums/ и сохраняет переданные пользователем данные об альбоме.
Данные передаются в формате веб-формы. Если пользователь пытается передать данные об альбоме, который уже есть в базе
данных, обработчик запроса отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение.

Допустим, мы запустили сервер по адресу http://localhost:8080. Тогда запросы будут выглядеть так:

http -f POST http://localhost:8080/albums artist="New Artist" genre="Rock" album="Super"

Дополните список передаваемых параметров, если потребуется.

3. Набор полей в передаваемых данных полностью соответствует схеме таблицы album базы данных.

4. В качестве исходной базы данных использовать файл albums.sqlite3.

5. До попытки сохранить переданные пользователем данные, нужно провалидировать их. Проверить, например, что
в поле "год выпуска" передан действительно год.

NB для метода POST не поддерживается передача символов кирилической кодировки
например: "альбоме 'ÐÐ¾Ð¼Ð±Ð°ÑÐ´Ð¸ÑÐ¾Ð²ÑÐ¸ÐºÐ¸' исполнителя 'Ð§Ð¸Ð¶' в жанре 'Rock' от 1997 года, сохранен
в базу данных"

Руководство по Python Bottle (Перевод) Часть 2 - Hello World
https://kbss.ru/blog/python/311.html
"""

# импортируем модули из библиотеки bottle для работы веб сервера
# запуск сервера
from bottle import run
# маршрутизация страниц
from bottle import route
# получение переданных запросов со страницы
from bottle import request
from bottle import post
# обработка и вывод ошибок
from bottle import HTTPError

# импортируем модули из библиотеки для работы с базами данных
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base
# use and_()
from sqlalchemy import and_
import urllib.parse

"""
ВНИМАНИЕ в системе должны быть установлены библиотеки
pip install bottle
pip install sqlalchemy
установка утилиты http, предназначенной для тестирования веб приложений
python -m pip install httpie
"""

# константа, указывающая способ соединения  с базой данных
DB_PATH = "sqlite:///albums.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет, и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH, encoding='utf-8')
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    return session()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    # указываем имя таблицы
    __tablename__ = "album"
    # Задаем колонки в формате
    # название_колонки = sa.Column(ТИП_КОЛОНКИ)

    # идентификатор строки
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def find_album(artist, album=None, genre=None, year=None):
    """
    получаем из БД информацию по альбомам указанного артиста
    :param artist: артист
    :param album название альбома
    :param genre жанж
    :param year год выхода
    :return: список альбомов исполнителя
    """
    # получили список строк таблицы альбомов по указанному испольнитеклю
    session = connect_db()
    # проверяем переданные параметры
    if album is None or genre is None or year is None:
        album_lst = session.query(Album).filter(Album.artist == artist).all()
        album_lst = [alb.album for alb in album_lst]
    else:
        album_lst = session.query(Album).filter(and_(Album.artist == artist,
                                                     Album.album == album,
                                                     Album.genre == genre.capitalize(),
                                                     Album.year == year)).first()
    return album_lst


def add_album(album):
    """
    сохраняе данные альбома в БД
    :param album: кортеж для записи в БД
    :return:
    """
    session = connect_db()
    session.add(album)
    session.commit()
    print("данные сохранены в базе данных")


# тестирование: страница с ошибкой
# http://localhost:8080/albums/met
# тестирование: страница с данными
# http://localhost:8080/albums/Beatles


@route('/albums/<artist>')
def show_albums(artist):
    """
    обработка GET запроса
    :param artist: имя артиста
    :return: экран сообщение с количеством альбомов исполнителя artist и списком названий этих альбомов
    """
    artist_lst = find_album(artist)
    if not artist_lst:
        message = "Альбомов исполнителя '{}' не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        result = "для исполнителя '{}' найдено {} альбомов:<br>".format(artist, len(artist_lst))
        result += "<br>".join(artist_lst)
    return result


# http -f GET http://localhost:8080/albums_t artist=="New Artist" genre=="Rock" album=="Super" year=="2020"
# http -f GET http://localhost:8080/albums_t artist=="Кино" genre=="Rock" album=="Звезда по имени Солнце" year==1989
# http://localhost:8080/albums_t?artist=New Artist&genre=Rock&album=Super&year=2020
# http://localhost:8080/albums_t?artist=Жуки&genre=Rock&album=Батарейка&year=1999
# http://localhost:8080/albums_t?artist=Жукифф&genre=Rock&album=Батарейкаф&year=1998

@route("/albums_t")
def post_albums_t():
    """
    тестирование работы get запроса
    """
    try:
        # album_data = {
        #     "artist": request.query.get("artist"),
        #     "genre": request.query.get("genre"),
        #     "album": request.query.get("album"),
        #     "year":  int(request.query.get("year"))
        # }
        album = Album(
            artist=request.query.artist,
            genre=request.query.genre,
            album=request.query.album,
            year=int(request.query.year)
        )
    except ValueError:
        result = HTTPError(400, "Некорректные параметры")
    else:
        artist_lst = find_album(artist = album.artist, genre = album.genre, album = album.album, year = album.year)
        if artist_lst:
            message = "альбоме '{}' исполнителя '{}' в жанре '{}' от {} года, уже есть в базе данных".format(
                album.album,
                album.artist,
                album.genre,
                album.year
            )
            result = HTTPError(409, message)
        else:
            add_album(album)
            result = "альбоме '{}' исполнителя '{}' в жанре '{}' от {} года, сохранен в базу данных".format(
                album.album,
                album.artist,
                album.genre,
                album.year
            )
    return result


# http -f POST localhost:8080/albums artist="New Artist" genre="Rock" album="Super" year="2020"
# http -f POST localhost:8080/albums artist="Чичерина" genre="Rock" album="Сны" year="2000"

# http -f POST localhost:8080/albums artist="Чиж & Co" genre="Rock" album="Бомбардировщики" year="1997"

# http://localhost:8080/albums_t?artist=New Artist&genre=Rock&album=Super&year=2020
# http://localhost:8080/albums_t?artist=Жуки&genre=Rock&album=Батарейка&year=1999


# @route('/albums', metod='POST')
@post('/albums')
def post_album():
    # album_data = {
    #     "artist": request.forms.get("artist"),
    #     "genre": request.forms.get("genre"),
    #     "album": request.forms.get("album"),
    #     "year":  int(request.forms.get("year"))
    # }
    try:
        album = Album(
            artist=request.forms.get("artist"),
            genre=request.forms.get("genre"),
            album=request.forms.get("album"),
            year=int(request.forms.get("year"))
        )
        print("альбоме '{}' исполнителя '{}' в жанре '{}' от {} года, сохранен в базу данных".format(
                album.album,
                album.artist,
                album.genre,
                album.year
            ))
    except ValueError:
        result = HTTPError(400, "Некорректные параметры")
    else:
        artist_lst = find_album(artist = album.artist, genre = album.genre, album = album.album, year = album.year)
        if artist_lst:
            message = "альбоме '{}' исполнителя '{}' в жанре '{}' от {} года, уже есть в базе данных".format(
                album.album,
                album.artist,
                album.genre,
                album.year
            )
            result = HTTPError(409, message)
        else:
            add_album(album)
            result = "альбоме '{}' исполнителя '{}' в жанре '{}' от {} года, сохранен в базу данных".format(
                album.album,
                album.artist,
                album.genre,
                album.year
            )
    return result


if __name__ == '__main__':
    # запускаем локальный сервер в режиме отладки
    run(host="localhost", port=8080, debug=True)
