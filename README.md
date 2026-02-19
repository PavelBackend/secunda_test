Описание:
- Для авторизации в документации справа вверху находится кнопка "Authorize", туда необходимо вставить API KEY: TfeP1_MhMB0qKt16IKr0EB6vadQP7dSTfblxO72L8Fg

Запуск:
# Клонируем репозиторий
git clone https://github.com/PavelBackend/secunda_test.git && cd secunda_test

# Копируем конфиг окружения
cp .env.example .env

# Запускаем контейнеры (миграции применяются автоматически при старте)
docker compose -f deploy/docker-compose.yml up --build -d

По пути http://localhost:8000/docs будет доступна документация

# Прогон автотестов (выполняются в отдельной БД secunda_test, создаётся автоматически)
docker compose -f deploy/docker-compose.yml exec main_service pytest

# Данные для ручного тестирования (уже добавленные в миграции):

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
docker compose -f deploy/docker-compose.yml down

# Остановка контейнеров и удаление томов
docker compose -f deploy/docker-compose.yml down -v
