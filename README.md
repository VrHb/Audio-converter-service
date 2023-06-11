# Сервис для конвертирования аудиозаписей 

## Установка проекта

1. Скопируйте репозиторий

```
git clone https://github.com/VrHb/Audio-converter-service.git
```

2. Активируйте виртуальное окружение

```
python -m venv <название окружения>
```

3. Установите необходимые библиотеки

```
pip install -r requirements.txt
```

#### Переменные окружения

1. Создайте .env файл

```
touch .env
```

2. Добавьте пароль и порт для postgresql в файл

```
echo "PSQL_PASSWORD=<ваш пароль к бд>" >> .env";
echo "PSQL_PORT=<порт>" >> .env
```

#### Создание контейнера с postgresql

1. Запустите сборку контейнера

```
docker-compose up -d
```

## Запуск сервиса

```
uvicorn main:app --reload
```

#### Пример запросов


##### Добавление пользователя

```
curl -X 'POST' \
  'http://127.0.0.1:8800/add_user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "имя пользователя"
}'
```

##### Добавление аудиофайла

```
curl -X 'POST' \
  'http://127.0.0.1:8800/convert_audio/?user_uuid=<uuid пользователя>&user_token=<токен пользователя>' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'audiofile=@ewrwer.wav;type=audio/wav'
```

*Документации по API методам проекта находится в `/docs`*
