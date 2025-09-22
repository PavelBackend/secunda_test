Описание:
- Убрал .env из .gitignore для легкого запуска тестового, в реальный проектах так, конечно, не делаю
- Для авторизации в документации справа вверху кнопка authorize, туда вставляем TfeP1_MhMB0qKt16IKr0EB6vadQP7dSTfblxO72L8Fg

Запуск:
# Клонируем репозиторий
git clone https://github.com/PavelBackend/secunda_test.git

# Запускаем контейнеры
docker compose -f secunda_test/deploy/docker-compose.yml --env-file secunda_test/.env up --build -d

# Применяем миграции
docker compose -f secunda_test/deploy/docker-compose.yml exec main_service alembic -c api/alembic.ini upgrade head

http://localhost:8000/docs будет доступна документация

# Тестовые данные, уже добавленные в миграции:

Здания
1. Main Street 1 — Москва центр (lat=55.751244, lon=37.618423)
2. Main Street 2 — рядом с #1 (lat=55.752000, lon=37.619000)
3. Main Street 3 — Санкт-Петербург (lat=59.9342802, lon=30.3350986)

Организации
1. Test Org 1 → Main Street 1 → активности: Web Development, Frontend
2. Test Org 2 → Main Street 1 → University Education, High School
3. Test Org 3 → Main Street 2 → Mobile Development, Android
4. Test Org 4 → Main Street 3 → Clinic, General Medicine
5. Test Org 5 → Main Street 3 → School Education, Primary School

Активности:
1. IT Services → Web Development → Frontend/Backend
2. IT Services → Mobile Development → iOS/Android
3. Education → School Education → Primary/High School
4. Education → University Education
5. Healthcare → Clinic → General Medicine

# Останавливаем контейнеры
docker compose -f secunda_test/deploy/docker-compose.yml down (-v чтобы удалить тома не забудьте после просмотра тестового, у вас же еще будут тестовые с базой на дефолтном порте))
