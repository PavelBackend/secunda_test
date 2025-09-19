Описание:
- Убрал .env из .gitignore для легкого запуска тестового
- Для авторизации в документации справа вверху кнопка authorize, туда вставляем CEj56fFn4gS9W8bST6484GYeRmPdYbHJfdA6z0IZs_8

Запуск:
# Клонируем репозиторий
git clone https://github.com/PavelBackend/secunda_test.git

# Переходим в директорию проекта
cd secunda_test

# Запускаем контейнеры
docker compose -f ./deploy/docker-compose.yml --env-file .env up --build -d

# Применяем миграции
docker compose -f ./deploy/docker-compose.yml exec main_service alembic -c api/alembic.ini upgrade head

http://localhost:8000/docs будет доступна документация

# Останавливаем контейнеры
docker compose -f ./deploy/docker-compose.yml down
