запуск сервера:
bd_album_server.py

тест строка для проверки get запроса:
http://localhost:8080/albums/Beatles

тест строка для проверки post запроса:
http -f POST http://localhost:8080/albums artist="New Artist" genre="Rock" album="Super" year="2020"