#импорт библиотек
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
#определение текущей директории
path=str(os.path.abspath(os.path.dirname(__file__)))
os.chdir(path)

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)



#Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

#Находит все альбомы в базе данных по заданному артисту
def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

# функция создания нового альбома
def create_album(user_data):
    album = Album(
        year=user_data["year"],
        artist=user_data["artist"],
        genre=user_data["genre"],
        album=user_data["album"])
    #возвращаем созданный альбом
    return album


#Записывает пользовательские данные в БД
def rec(album):
    session = connect_db()
    # добавляем новый альбом в сессию
    session.add(album)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")

#секция исключений
#Используется для идентификации некорректных данных запроса
class InvalidData(Exception):
    pass

#Класс для проверки года
class InvalidArgumentType(InvalidData):
    pass

#Функция проверки года на число
def valid_year(year):
    if not year.isdigit():
        raise InvalidArgumentType("Некорректный тип, ожидается цифра года")