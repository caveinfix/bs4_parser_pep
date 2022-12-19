
# Проект: парсер PEP

Что делает парсер:
- Парсит данные обо всех документах PEP со страницы: https://peps.python.org/
- Сравнивает статус на каждой отдельной странице PEP со статусом в общем списке
- Считает количетсво PEP в каждом статусе и общее количество PEP
- Сохраняет результат в табличном виде в csv-файл.



## Установка и запуск

#### Скачать проект:

```http
  https://github.com/caveinfix/foodgram-project-react.git
```

#### Установить виртуальное окружение и зависимости:

```http
  python -m venv venv
  source venv/Scripts/activate
  pip install -r requirements.txt
```


#### Вызов справки для просмотра доступных аргументов:
```http
python main.py -h
```

| Аргумент | Задача     |
| :-------- | :------- | 
| `whats-new`      | `Парсит справочную информацию с каждой страницы со статьями о нововведениях в Python.` |
| `latest-versions`      | `Парсит информацию о версиях Python — номера, статусы и ссылки на документацию.` |
| `download`      | `Cкачивает актуальный архив с документацией Python на Ваш локальный диск.` |
| `pep`      | `Парсит данные обо всех документах PEP, сравнивает статусы, считает и сохраняет в таблице csv.` |

Пример запуска с аргументом:
```http
python main.py whats-new
```

#### Необязательные аргументы:
| Аргумент | Задача     |
| :-------- | :------- | 
| `-c, --clear-cache`      | `Очистка кеша.` |
| `-o {pretty,file}, --output`      | `Дополнительные способы вывода данных.` |

Пример запуска с необязательным аргументом:
```http
python main.py latest-versions -c --output file
```
## 🚀 Автор
Филипп @caveinfix

e-mail: caveinfix@gmail.com