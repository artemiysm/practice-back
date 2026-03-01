#  Смирнов.А.А Сервис Опросов
> **Survey Service** — Сервис опросов

В этом документе описано всё, что было выполнено в рамках первого чекпоинта проекта **Survey Service**.

---

##  Выполненные задачи

| № | Задача | Статус |
|---|--------|--------|
| 1 | Выбор стека технологий |  Выполнено |
| 2 | Инициализация проекта и Git-репозитория |  Выполнено |
| 3 | Проектирование ER-диаграммы базы данных |  Выполнено |
| 4 | Проектирование списка API эндпоинтов |  Выполнено |
| 5 | Создание и запуск миграций |  Выполнено |
| 6 | Написание README с описанием проекта |  Выполнено |

---

## 1.  Выбор стека технологий

Для реализации проекта был выбран следующий стек:

| Компонент | Технология | Обоснование выбора |
|-----------|------------|-------------------|
| **Язык программирования** | Python 3.10+ | Простой синтаксис, богатая экосистема библиотек |
| **Веб-фреймворк** | Flask | Лёгкий, гибкий, идеально подходит для REST API |
| **ORM** | SQLAlchemy | Мощная абстракция работы с БД, поддержка миграций |
| **База данных** | PostgreSQL | Надёжная, поддержка ENUM-типов, индексов, транзакций |
| **Миграции** | Flask-Migrate (Alembic) | Управление версиями схемы базы данных |
| **Авторизация** | Flask-JWT-Extended | JWT-токены для безопасной аутентификации |

---

## 2.  Инициализация проекта и Git

### Структура проекта
| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/surveys` | Получить список опросов автора | Автор (JWT) |
| POST | `/api/surveys` | Создать новый опрос (черновик) | Автор (JWT) |
| GET | `/api/surveys/<id>` | Получить опрос по ID | Публичный / Автор |
| PUT | `/api/surveys/<id>` | Редактировать опрос | Автор, только `draft` |
| DELETE | `/api/surveys/<id>` | Удалить опрос | Автор, только `draft` |
| POST | `/api/surveys/<id>/publish` | Опубликовать опрос | Автор |
| POST | `/api/surveys/<id>/close` | Закрыть опрос | Автор |

### Вопросы

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/surveys/<id>/questions` | Добавить вопрос к опросу | Автор, только `draft` |
| PUT | `/api/surveys/<id>/questions/<qid>` | Редактировать вопрос | Автор, только `draft` |
| DELETE | `/api/surveys/<id>/questions/<qid>` | Удалить вопрос | Автор, только `draft` |

###  Прохождение опросов

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/surveys/<id>/submit` | Отправить ответы на опрос | Респондент (JWT) |

###  Аналитика

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/surveys/<id>/results` | Получить результаты опроса | Автор (JWT) |
| GET | `/api/surveys/<id>/results/export` | Экспорт результатов в JSON | Автор (JWT) |

---
##  ER-диаграмма базы данных

```mermaid
erDiagram
    USERS ||--o{ SURVEYS : "создаёт"
    USERS ||--o{ RESPONSES : "проходит"
    SURVEYS ||--|{ QUESTIONS : "содержит"
    QUESTIONS ||--o{ OPTIONS : "имеет варианты"
    SURVEYS ||--o{ RESPONSES : "получает ответы"
    RESPONSES ||--|{ ANSWERS : "включает ответы"
    QUESTIONS ||--o{ ANSWERS : "получает ответы на"
    OPTIONS ||--o{ ANSWERS : "выбран в"

    USERS {
        int id PK
        string email UK
        string password_hash
        timestamp created_at
    }
    
    SURVEYS {
        int id PK
        int author_id FK
        string title
        string description
        enum status
        timestamp created_at
    }
    
    QUESTIONS {
        int id PK
        int survey_id FK
        string text
        enum q_type
        int order_index
    }
    
    OPTIONS {
        int id PK
        int question_id FK
        string text
    }
    
    RESPONSES {
        int id PK
        int survey_id FK
        int user_id FK
        timestamp submitted_at
    }
    
    ANSWERS {
        int id PK
        int response_id FK
        int question_id FK
        string text_value
        int option_id FK
    }
```
## 5.  Миграции базы данных

### Команды для работы с миграциями

```bash
# Инициализация миграций 
flask db init

# Создание новой миграции после изменений в моделях
flask db migrate -m "Initial migration"

# Применение миграций к базе данных
flask db upgrade

# Откат последней миграции
flask db downgrade

# Проверка статуса миграций
flask db current