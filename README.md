# Blogicum

Blogicum — это социальная сеть, платформа для ведения блогов.
Можно вести собственный блог, читать блоги других участников и комментировать их посты.
К каждой публикации можно прикрепить фотографию. Реализована регистрация 
и авторизация пользователей, подключена возможность отправки писем с кодом для регистрации
на электронную почту. Прописана админ-зона сайта, существует три категории пользователей: 
обычный, администратор и супер-пользователь. Администратор может редактировать посты и комментарии 
других пользователей, или снимать их с публикации. Посты можно сортировать по авторству, по категориям
и по месту. На сайте реализована пагинация.

Бэкенд приложения написан на `Python`, а именно на фреймворке `Django`.




##### _Как запустить проект на своём ПК:_
- Заходим в IDE, открываем терминал. Выбираем нужную директорию, куда будем копировать проект.
- С помощью команды `git clone https://github.com/FvckingMad/Blogicum.git` копируем удалённый репозиторий на ваш компьютер
- С помощью команды `python -m venv venv` создаём виртуальное окружение
- Активируем виртуальное окружение командой `source venv\Scripts\activate`  
- Устанавливаем необходимые зависимости из текстового файла командой `pip install -r requirements.txt`
- Создаём и применяем миграции командами `python manage.py makemigrations` и `python manage.py migrate`
- Собираем статику приложения командой `python manage.py collectstatic`
- Наполняем базу данных информацией из заготовленного файла командой `python manage.py loaddata db.json`
- Командой `python manage.py runserver` локально запускаем сервер на своём ПК, он будет доступен по адресу  `http://127.0.0.1:8000/`

![](https://github.com/FvckingMad/Blogicum/blob/main/main_page.png)
