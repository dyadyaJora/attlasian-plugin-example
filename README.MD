# Плагин для Atlassian Jira Connect.


Приложение создано на двух технологиях NodeJS и Python. Решение представляет собой веб приложения, которые отдают в статику конфиг для Jira-плагина, слушают webhook с функцией обратного вызова для события 'installed', а также url `/example`, который представляет собой пример запуска скрипта.

# Зависимости

`MongoDb`. В системе должен быть запущен демон `mongod`. Например это можно сделать командой:

    service mongod start
    
# Запуск проекта

## Для NodeJS

    cd nodejs
    npm install
    node app.js

## Для Python

    cd python
    pip install -r requirements.txt
    python app.py
    
