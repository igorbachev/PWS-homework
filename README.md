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
