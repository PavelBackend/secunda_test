Описание:
- Убрал .env из .gitignore для легкого запуска тестового, в реальный проектах так, конечно, не делаю
- Для авторизации в документации справа вверху кнопка authorize, туда вставляем TfeP1_MhMB0qKt16IKr0EB6vadQP7dSTfblxO72L8Fg

Запуск:
# Клонируем репозиторий
git clone https://github.com/PavelBackend/secunda_test.git

# Переходим в директорию проекта
cd secunda_test

# Запускаем контейнеры
docker compose -f ./deploy/docker-compose.yml --env-file .env up --build -d

# Применяем миграции
docker compose -f ./deploy/docker-compose.yml exec main_service alembic -c api/alembic.ini upgrade head

# Перезапускаем контейнеры, чтобы автоматически добавить тестовые данные
docker compose -f ./deploy/docker-compose.yml --env-file .env up --build -d

http://localhost:8000/docs будет доступна документация

# Останавливаем контейнеры
docker compose -f ./deploy/docker-compose.yml down
