# ITK Wallet Service

Тестовое задание

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM с асинхронной поддержкой
- **PostgreSQL** - база данных
- **Alembic** - миграции БД
- **Docker & Docker Compose** - контейнеризация

## Требования

- Python 3.13+
- Docker и Docker Compose

## Настройка окружения

### Переменные окружения (.env)

Создайте файл `.env` в корне проекта:

```env
# Приложение
APP_NAME=CUSTOM_APP_NAME
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=false
DATABASE_ECHO=false

# PostgreSQL
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mydatabase
```

**Важно:** При запуске через Docker Compose значение `POSTGRES_HOST` должно быть `db`, так как это имя контейнера PostgreSQL в `docker-compose.yml`.

## Установка и запуск

### Запуск через Docker

1. **Создайте файл `.env`** в корне проекта (см. раздел выше).

2. **Соберите и запустите контейнеры:**

```bash
docker-compose up --build -d
```

3. **Примените миграции:**

```bash
docker-compose exec api alembic upgrade head
```

Приложение будет доступно по адресу: http://localhost:8000

## Остановка Docker контейнеров

```bash
docker-compose down
```

**Для удаления volumes (включая данные БД):**

```bash
docker-compose down -v
```

## API Документация

После запуска приложения доступна автоматическая документация:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### Кошельки (Wallets)

- **POST** `/api/v1/wallets` - Создать новый кошелек
  - Body (опционально): `{"balance": 5000}` (по умолчанию 2000)

- **GET** `/api/v1/wallets/{wallet_uuid}` - Получить информацию о кошельке

- **POST** `/api/v1/wallets/{wallet_uuid}/operation` - Выполнить операцию
  - Body: `{"operation_type": "DEPOSIT" or "WITHDRAW", "amount": 1000}`

### Системные

- **GET** `/` - Главная страница
- **GET** `/health` - Health check

## Тестирование

Для запуска тестов локально (без Docker):

1. **Создайте и активируйте виртуальное окружение:**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# или
venv\Scripts\activate      # Windows
```

2. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

3. **Запустите тесты:**

```bash
pytest
```

**С подробным выводом:**

```bash
pytest -v
```
