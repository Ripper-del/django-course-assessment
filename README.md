# Online Course Exam

Реалізація модуля іспитів для платформи онлайн-навчання на базі Django. Студенти проходять тести після курсів, система автоматично підраховує результат.

---

## Реалізований функціонал

- **Моделі** — `Question` (питання), `Choice` (варіанти відповідей), `Submission` (спроба студента)
- **Адмін-панель** — управління питаннями та варіантами відповідей через Django Admin
- **Іспит** — форма з вибором відповідей, обробка POST-запиту, підрахунок балів
- **Результат** — відображення набраних балів після проходження тесту
- **Курси** — перегляд каталогу курсів із записом

---

## Технології

| Компонент | Технологія |
|---|---|
| Фреймворк | Django |
| База даних | SQLite (dev) / PostgreSQL (prod) |
| Фронтенд | Django Templates + Bootstrap |
| Розгортання | IBM Cloud Foundry |

---

## Структура проекту

```
myproject/          # налаштування Django (settings, urls)
onlinecourse/       # основний застосунок
├── models.py       # Course, Lesson, Question, Choice, Submission
├── views.py        # логіка запису на курс, іспиту, результату
├── admin.py        # налаштування адмін-панелі
└── templates/      # HTML-шаблони курсів та іспитів
static/             # статичні файли
```

---

## Запуск

```bash
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Застосунок доступний за адресою `http://localhost:8000`  
Адмін-панель: `http://localhost:8000/admin`
