# project_2025.12.09

Performance Report Generator
Скрипт для агрегации данных о производительности сотрудников из нескольких CSV-файлов и генерации отчёта с усреднённой эффективностью по должностям.

Содержимое репозитория
report_script.py — основной скрипт для генерации отчёта.
test_report_script.py — интеграционный тест с использованием pytest.
Примеры данных в формате CSV (employees1.csv, employees2.csv) — для демонстрации работы.

Быстрый старт
1. Установка зависимостей

```sh
pip install -r requirements.txt
```

2. Запуск отчёта

```sh
python report_script.py --files employees1.csv employees2.csv --report performance
```

Пример вывода:

```sh
Report: performance
+---------------------+-----------------------+
| Position            |   Average Performance |
+=====================+=======================+
| Backend Developer   |                  4.83 |
| DevOps Engineer     |                  4.8  |
| Data Engineer       |                  4.7  |
| Fullstack Developer |                  4.7  |
| Frontend Developer  |                  4.65 |
| Data Scientist      |                  4.65 |
| Mobile Developer    |                  4.6  |
| QA Engineer         |                  4.5  |
+---------------------+-----------------------+
```

Запуск тестов

```sh
pytest test_report_script.py -v
```
Тест создаёт временные CSV-файлы на основе примеров, выполняет скрипт через подпроцесс и проверяет корректность вывода и сортировки.
