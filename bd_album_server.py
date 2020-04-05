import json

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import os
path=str(os.path.abspath(os.path.dirname(__file__)))
print(path)
os.chdir(path)
#импортируем файл bd_album.py
import bd_album

@route("/albums/<artist>")
def albums(artist):
    #импортируем функцию find из файла bd_album.py
    albums_list = bd_album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
         album_names = [album.album for album in albums_list]
         result = "Количество альбомов {}: {}<br>".format(artist,len(albums_list))
         result += "Список альбомов {}:<br>".format(artist)
         result += "<br>".join(album_names)
    return result

#Форма запроса http -f POST http://localhost:8080/albums artist="New Artist" genre="Rock" album="Super" year="1980"
#POST запрос на запись в БД

@route("/albums", method="POST")
def user():
    user_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year": request.forms.get("year"),
    }
    bd_album.valid_year(user_data["year"])
    #Ищем альбомы по данным введенного artist и формируем список записей Album
    albums_list = bd_album.find(user_data["artist"])
    #если список пуст, то артист новый - вносим запись
    if not albums_list:
       #создаем новый альбом по данным из POST запроса
       new_album = bd_album.create_album(user_data)
       #вносим запись в БД
       bd_album.rec(new_album)
       result = "Данные успешно сохранены в БД !"
    else:
       #формируем список альбомов введенного исполнителя
       album_names = [album.album for album in albums_list]
       #если альбом из запроса есть, в БД то выдаем ошибку
       if user_data["album"] in album_names:
          message = "Вносятся данные об альбоме {} исполнителя {}, который уже есть в БД".format(user_data["album"],user_data["artist"])
          result = HTTPError(409, message)
       else:
          #создаем новый альбом по данным из POST запроса
          new_album = bd_album.create_album(user_data)
          #вносим запись в БД
          bd_album.rec(new_album)
          result = "Данные успешно сохранены в БД !"
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
