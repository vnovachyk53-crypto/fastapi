# Workout Tracker — SQLAlchemy ORM + MySQL 8

Готове виконання домашнього завдання: FastAPI, Pydantic 2, SQLAlchemy ORM 2.x та MySQL 8 (PyMySQL).

## 1. Що реалізовано

### Частина A — основа застосунку
- Моделі `User` і `Workout`, зовнішній ключ `workouts.owner_id -> users.id`.
- Створення таблиць під час запуску API.
- `POST /users`.
- `POST /workouts`.
- `GET /workouts?owner_id=1&limit=20&offset=0`; `limit` обмежений діапазоном 1–100.
- Окремі Pydantic-схеми створення та відповіді. Для вхідних схем установлено `extra="forbid"`.
- `seed.py`: 3 користувачі та 18 тренувань чотирьох видів, розподілених щонайменше на три календарні місяці.

### Частина B — статистика
- `GET /stats/summary?owner_id=1`
- `GET /stats/by-kind?owner_id=1`
- `GET /stats/by-month?owner_id=1`
- `GET /stats/top-users?min_workouts=3`
- `GET /stats/done-ratio?owner_id=1`

### Частина C — захист
- `GET /stats/group?group_by=kind&metric=sum_duration&owner_id=1`
- Для групування та метрик використано `Enum`, `GROUP_COLUMNS` і `METRICS`; `getattr()` для імен колонок або SQL-функцій не використовується.
- Усі персональні статистичні ендпоінти мають обов'язковий `owner_id` і умову `Workout.owner_id == owner_id`.
- Підключення має `hide_parameters=True`, `echo=False`; API не повертає текст SQL або внутрішній текст винятку.
- Обмеження `CHECK`, `UNIQUE` та `FOREIGN KEY` продубльовано на рівні MySQL.

### Бонус
- `GET /stats/running-total?owner_id=1`
- `GET /stats/rank?owner_id=1`

## 2. Що спрощено в коді

- У маршрутах використано звичайний `Depends(get_db)` замість окремого типу `SessionDep`.
- Параметри URL описані прямо в функціях через `Query(...)`.
- Прибрано необов’язкові ORM-зв’язки `relationship`, бо для цього завдання достатньо зовнішнього ключа `owner_id`.
- `Mapped` і `mapped_column` залишено: це стандартний стиль SQLAlchemy 2, який використовується і в навчальних матеріалах.
- `case()` та `over()` залишено, оскільки вони потрібні для умовного підрахунку й бонусних віконних функцій.

## 3. Що потрібно встановити

Потрібні Python 3.10+ та MySQL 8. У терміналі в корені папки проєкту виконайте:

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Якщо PowerShell забороняє активацію середовища, можна запускати інтерпретатор напряму: `.venv\Scripts\python.exe`.

## 4. Створення бази MySQL

Створіть базу даних. Наприклад, у MySQL Workbench відкрийте SQL-вкладку та виконайте вміст `database_setup.sql` або виконайте команду:

```bash
mysql -u root -p < database_setup.sql
```

Далі скопіюйте `.env.example` у `.env` і впишіть власні дані підключення:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=workout_tracker
DB_USER=root
DB_PASSWORD=ВАШ_ПАРОЛЬ_MYSQL
```

`DB_USER` і `DB_PASSWORD` — це логін і пароль саме від MySQL, не від Windows.

## 5. Заповнення тестовими даними

У корені проєкту виконайте:

```bash
python seed.py
```

Скрипт безпечно пропускає користувачів, які вже є, та не дублює тренування для них під час повторного запуску.

## 6. Запуск API

```bash
uvicorn main:app --reload
```

Відкрийте документацію в браузері: <http://127.0.0.1:8000/docs>.

## 7. Приклади запитів

Після `seed.py` у свіжій базі перший користувач зазвичай матиме `id=1`:

```text
GET  http://127.0.0.1:8000/workouts?owner_id=1&limit=20&offset=0
GET  http://127.0.0.1:8000/stats/summary?owner_id=1
GET  http://127.0.0.1:8000/stats/by-kind?owner_id=1
GET  http://127.0.0.1:8000/stats/by-month?owner_id=1
GET  http://127.0.0.1:8000/stats/top-users?min_workouts=3
GET  http://127.0.0.1:8000/stats/done-ratio?owner_id=1
GET  http://127.0.0.1:8000/stats/group?group_by=kind&metric=sum_duration&owner_id=1
GET  http://127.0.0.1:8000/stats/running-total?owner_id=1
GET  http://127.0.0.1:8000/stats/rank?owner_id=1
```

Щоб створити користувача, у Swagger (`/docs`) виконайте `POST /users` з тілом:

```json
{
  "name": "Іван Петренко",
  "email": "ivan@example.com"
}
```

Щоб додати тренування, виконайте `POST /workouts`:

```json
{
  "owner_id": 1,
  "title": "Ранкова пробіжка",
  "kind": "run",
  "duration_min": 45,
  "distance_km": 5.2,
  "done_on": "2026-10-30"
}
```

## 8. Пояснення схем відповідей

| Ендпоінт | Поля відповіді |
|---|---|
| `/stats/summary` | `total_workouts`, `total_duration_min`, `total_distance_km`, `avg_duration_min`, `min_distance_km`, `max_distance_km` |
| `/stats/by-kind` | `kind`, `workouts_count`, `total_duration_min`, `total_distance_km` для кожного виду |
| `/stats/by-month` | `month` у форматі `YYYY-MM`, `workouts_count`, `total_distance_km` |
| `/stats/top-users` | `user_id`, `name`, `workouts_count` |
| `/stats/done-ratio` | `long_workouts` (тривалість ≥ 60 хв), `total_workouts` |
| `/stats/group` | `group` (значення дозволеної групи), `value` (значення дозволеної метрики) |
| `/stats/running-total` | `workout_id`, `done_on`, `distance_km`, `running_total_km` |
| `/stats/rank` | `kind`, `total_duration_min`, `rank` |

Якщо вибірка порожня, `SUM` повертає `NULL`, тому в сумових полях застосовано `coalesce(..., 0)`. `AVG`, `MIN` та `MAX` для порожньої вибірки лишаються `null`, оскільки значення для них не існує.

## 9. Важливе уточнення щодо `top-users` та авторизації

Завдання описує `/stats/top-users` без `owner_id` і вимагає порівняти користувачів між собою. Тому це глобальний рейтинг, який групує тренування за користувачами; персональні статистичні маршрути окремо фільтруються за `owner_id`. Це єдиний змістовний виняток із правила персональної області видимості.

У завданні не описано механізм входу/авторизації. Тому `owner_id` тут є параметром фільтра, а не доказом особи користувача. Для справжнього публічного сервісу `owner_id` потрібно брати з автентифікованого користувача на сервері, а не довіряти значенню від клієнта.

## 10. Структура папок

```text
workout_tracker/
├── app/
│   ├── routers/
│   │   ├── stats.py
│   │   ├── users.py
│   │   └── workouts.py
│   ├── services/
│   │   └── stats_service.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── schemas_stats.py
├── .env.example
├── database_setup.sql
├── main.py
├── requirements.txt
├── seed.py
└── README.md
```
