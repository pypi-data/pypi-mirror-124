# dnevnikru

> Модуль для работы с сайтом dnevnik.ru на python

Объект Dnevnik принимает в себя login и password от аккаунта в дневнике <br/>
Методы: homework, marks, searchpeople, birthdays, week <br>
##### Ознакомиться с полным функционалом модуля можно тут: [Wiki][wiki] <br>
(Не работает в регионах, где вход в Дневник осуществляется только через ГосУслуги!)
## Установка

Windows:

Поместите файл ```dnevnikru.py``` в папку с вашим проектом

```python
from dnevnikru import Dnevnik
```

## Примеры использования

```python
from dnevnikru import Dnevnik

dn = Dnevnik(login='Your login', password='Your password')

homework = dn.homework(studyyear=2020, datefrom='01.12.2020', dateto='30.12.2020')
marks = dn.marks(index=0, period=1)
class_11b = dn.searchpeople(grade='11Б')
birthdays = dn.birthdays(day=9, month=5)
schedule = dn.week(info="schedule", weeks=-1)
```

_Ещё больше примеров использования и параметров в методах смотрите на странице [Wiki][wiki]._

## Зависимости

Для работы модуля понадобятся библиотеки `requests`, `lxml`, `bs4`

```cmd
pip install -r requirements.txt
```

## Релизы

* 0.0.1
  * Первая версия проекта

## Связь

Aleksandr – tg: [@paracosm17](https://t.me/paracosm17) – email: paracosm17@yandex.ru <br>
<br>
Contributors: <br>
<br>
<a href="https://github.com/paracosm17"><img src="https://avatars.githubusercontent.com/u/85677238?v=4&size=40" /></a>
<a href="https://github.com/stepanskryabin"><img src="https://avatars.githubusercontent.com/u/47498917?v=4&size=40" /></a>
<a href="https://github.com/vypivshiy"><img src="https://avatars.githubusercontent.com/u/59173419?v=4&size=40" /></a>

Distributed under the Apache License 2.0 license. See ``LICENSE`` for more information.

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/paracosm17/dnevnikru/wiki
