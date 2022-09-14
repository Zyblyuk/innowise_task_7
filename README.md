## innowise_task_7
### Task 7. Alert project
###### Zyblyuk Roman


# Запуск Проекта 
Проект запускается командой в терминале:
```
docker-compose up 
```
После чего он установит все зависимости и запустит контейнер

![alt text](https://github.com/Zyblyuk/innowise_task_7/blob/main/PrtScr/1.png)

# Класс BugCatcherByRule

Создал класс BugCatcherByRule
```
from BugCatcher import BugCatcherByRule


alerts = BugCatcherByRule(csv_file, columns_name)
```

где csv_file - это путь к csv файлу, а columns_name имена столбцов


Мы можем отсортировать данные обратившись к Dataframe полю data  
```
alerts.data = alerts.data[
    (alerts.data["severity"] == "Error") &
    (alerts.data["error_code"] > 0)
    ]
```
Здесь я оставил только данные с критическими ошибками

Затем приводим столбец с датой к DateTime формату,
используя атрибут anything_to_datetime, 
который может конвертировать любой формат строк

```

alerts.anything_to_datetime('sdk_date')
```

Для задания правил для оповещения используется атрибут send_alerts_by_rules,
Который принимает значения:
date_column, group_by_key, n, column_where, value_where
где:

date_column - временной столбец,

group_by_key - Ключ, принимает значения day, month, year, hour, minute или second,
нужен для задания времени, например:

Фатальные ошибки случившееся в течении одной минуты, дня, года и тд.

n - количество ошибок за group_by_key, например:

Более чем n фатальных ошибок случившееся в течении group_by_key.

column_where, value_where - (*необязательные значения) поваляют выбрать данные для конкретного значения 


```
#Оповещение о более чем 10 фатальных ошибках менее чем за одну минуту:
alerts.send_alerts_by_rules("sdk_date", "minute", 10)

# Оповещение о более чем 10 фатальных ошибках менее чем за один час для конкретного bundle_id:
alerts.send_alerts_by_rules("sdk_date", "hour", 10, 'bundle_id', "com.pregnantcatemma.virtualpet")

# Оповещение о более чем 300 фатальных ошибках менее чем за один час день:
alerts.send_alerts_by_rules("sdk_date", "day", 300)
```
Использование класса облегчено сознание новых правил
или прям все поля вывесли у каждой ошибки 