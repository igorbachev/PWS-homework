# Репозиторий проекта проверки Домашнего Задания

## директория B4.12

модуль users.py, регистрирует новых пользователей. Скрипт запрашивать следующие данные:

    имя
    фамилию
    пол
    адрес электронной почты
    дату рождения
    рост

Все данные о пользователях сохранены в таблице user базы данных sochi_athletes.sqlite3.

модуль find_athlete.py поиск ближайшего к пользователю атлета. Логика работы модуля такова:

    запросить идентификатор пользователя;
    если пользователь с таким идентификатором существует в таблице user, то вывести на экран двух атлетов: ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
    если пользователя с таким идентификатором нет, вывести соответствующее сообщение.

## директория B5.9

пример описания декоратор для логики, которая измеряет скорость работы функций. Как-то так:

```python
@time_this(num_runs=10)
def f():
    for j in range(1000000):
        pass
```
Примечания:

    в данном случае внутри вложенной функции (где-то в декораторе) стоит выводить среднее время выполнения;
    можно либо зафиксировать число запусков, либо передавать как параметр.

Опционально: вы можете выполнить несколько дополнительных требований и получить за них баллы:

    задание с одной звездочкой: написать декоратор в качестве объекта класса-секундомера;
    задание с двумя звездочками: написать декоратор в качестве объекта класса-секундомера, который можно использовать как контекстный менеджер.

## директория B6.13

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