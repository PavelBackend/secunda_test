# REST API справочника организаций

REST API на FastAPI для работы с каталогом организаций, зданий и видов деятельности.

## Стек

- **FastAPI** + **Pydantic** — веб-фреймворк и валидация
- **SQLAlchemy 2.0 async** + **asyncpg** — асинхронная работа с БД
- **GeoAlchemy2** + **PostGIS** — геопространственные запросы
- **Alembic** — миграции
- **PostgreSQL 16** — база данных
- **Docker** + **Docker Compose** — контейнеризация
- **Poetry** — управление зависимостями

## Реализованный функционал

- Список организаций в конкретном здании
- Список организаций по виду деятельности (прямое соответствие)
- Список организаций по дереву деятельности — поиск с учётом всех дочерних видов деятельности (до 3 уровней вложенности)
- Поиск организаций в заданном радиусе от точки на карте (через `ST_DWithin`)
- Поиск организаций в прямоугольной области (через `ST_Intersects`)
- Поиск организаций по названию (регистронезависимый, частичное совпадение)
- Получение информации об организации по идентификатору
- Авторизация через статический API-ключ в заголовке `X-API-Key`
- Swagger UI с описанием всех методов: `http://localhost:8000/docs`

## Запуск

```bash
# Клонируем репозиторий
git clone https://github.com/PavelBackend/secunda_test.git && cd secunda_test

# Копируем конфиг окружения
cp .env.example .env

# Запускаем контейнеры (миграции и заполнение тестовыми данными применяются автоматически)
docker compose -f deploy/docker-compose.yml up --build -d
```

Документация будет доступна по адресу `http://localhost:8000/docs`.

Для авторизации в Swagger нажмите кнопку **Authorize** (правый верхний угол) и введите API-ключ TfeP1_MhMB0qKt16IKr0EB6vadQP7dSTfblxO72L8Fg.

## Тесты

```bash
# Запуск автотестов (выполняются в отдельной БД, создаётся автоматически)
docker compose -f deploy/docker-compose.yml exec main_service pytest
```

## Управление контейнерами

```bash
# Остановка
docker compose -f deploy/docker-compose.yml down

# Остановка с удалением томов
docker compose -f deploy/docker-compose.yml down -v
```

## Тестовые данные

Данные добавляются автоматически через миграцию при старте.

**Здания:**

| Адрес | Координаты |
|-------|-----------|
| Main Street 1 | 55.751244, 37.618423 (Москва) |
| Main Street 2 | 55.752000, 37.619000 (рядом с #1) |
| Main Street 3 | 59.934280, 30.335099 (Санкт-Петербург) |

**Организации:**

| Организация | Здание | Виды деятельности |
|-------------|--------|-------------------|
| Test Org 1 | Main Street 1 | Web Development, Frontend |
| Test Org 2 | Main Street 1 | University Education, High School |
| Test Org 3 | Main Street 2 | Mobile Development, Android |
| Test Org 4 | Main Street 3 | Clinic, General Medicine |
| Test Org 5 | Main Street 3 | School Education, Primary School |

**Дерево деятельности (3 уровня):**

```
IT Services
├── Web Development
│   ├── Frontend
│   └── Backend
└── Mobile Development
    ├── iOS
    └── Android

Education
├── School Education
│   ├── Primary School
│   └── High School
└── University Education

Healthcare
└── Clinic
    └── General Medicine
```
