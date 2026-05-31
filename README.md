# Product Prioritization Tool

Инструмент для приоритизации продуктовых фич по методологиям WSJF, RICE и ICE с трекингом метрик после релиза.

## Стек

- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: Streamlit
- **БД**: PostgreSQL
- **Инфра**: Docker Compose

## Функциональность

- Добавление фич с автоматическим подсчётом WSJF / RICE / ICE score
- Ранжированный список фич с фильтрацией по статусу
- Трекинг метрик после релиза (DAU, конверсия, выручка и др.)
- Визуализация динамики метрик

## Запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/zeralina/pmtool.git
cd pmtool
```

### 2. Запустить базу данных
```bash
docker compose up -d db
```

### 3. Запустить backend
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

### 4. Запустить frontend
```bash
cd ..
streamlit run frontend/app.py
```

## API

[Документация доступна по адресу: `http://127.0.0.1:8000/docs`](https://pmtool-production-5b83.up.railway.app/docs)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | /features | Все фичи |
| POST | /features | Добавить фичу |
| GET | /features/{id} | Одна фича |
| PUT | /features/{id} | Обновить статус |
| DELETE | /features/{id} | Удалить фичу |
| GET | /features/{id}/metrics | Метрики фичи |
| POST | /features/{id}/metrics | Добавить метрику |

## Формулы

**WSJF** = (Business Value + Time Criticality + Risk Reduction) / Job Size

**RICE** = (Reach × Impact × Confidence) / Effort

**ICE** = Impact × Confidence × Ease

## Демо

- **Приложение**: https://pmtool-dnsb2mlpfwuxgzeal5g4qg.streamlit.app
- **API docs**: https://pmtool-production-5b83.up.railway.app/docs