## Документация по проекту
Для запуска проекта необходимо:
- Клонировать репозиторий проекта
```
git clone https://github.com/nastine/idaprojecttest.git
```
- Установить зависимости
```
pip install -r requirements.txt
```
- Перейти в папку приложения
```
cd imgservice
```
- Cоздать миграции приложения для базы данных
```
python manage.py migrate
```
- Команда для запуска приложения
```
python manage.py runserver
```
