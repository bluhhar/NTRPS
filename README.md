# «Новые технологии в РПС»

### План
```diff
+ Лабораторная работа №1
! Лабораторная работа №2
- Лабораторная работа №3
```

### Установка
```shell
git clone https://github.com/bluhhar/NTRPS
python -m venv venv
venv\Scripts\activate.bat (тут проверить cmd (venv) в VS Code в Terminal добавить command prompt)
pip install -r requirements.txt
```
## [Лабораторная работа №1](https://github.com/bluhhar/NTRPS/blob/main/lab1/lab01__Python_M_PIN_RIS_2306_Timofeev%20Aleksander.docx) (+)

### [Вариант №1 (ЦРБ Валюты)](#section-1)
С использованием веб-сайта https://www.cbr-xml-daily.ru получить курс доллара по дням на максимально возможный период. Результат сохранить в выходной файл dataset.csv, где каждая строка будет содержать дату и курс, разделенные запятой.

**Примечания**

Пример ссылки для получения данных: https://www.cbr-xml-daily.ru/archive/2023/09/13/daily_json.js

**Используемые сторонние библиотеки:**

> requests

### [Вариант №5 (Яндекс.Картинки)](#section-2)

С использованием страницы https://yandex.ru/images/ сформировать запросы для поиска изображений, контент на которых соответствует классам polar bear и brown bear. Для каждого класса должно быть загружено не менее 1000 изображений. Изображения для каждого класса должны находиться в подпапке папки dataset с соответсвующим названием.

**Не допускается:**

* Создание папок вручную. В коде должен быть отражен процесс создания папок и перемещения/загрузки в них файлов.
* Дублирование изображений для класса.

**Примечания**
* Каждое изображение должно иметь расширение .jpg
* Именовать файлы необходимо порядковым номером (от 0 до 999).
* Для дальнейшего удобства необходимо дополнять имя файла ведующими нулями (например, 0000, 0001, ..., 0999). Для этого необходимо использовать один из методов класса str.

**Вариант подразумевает два уровня сложности:**

* Для первого уровня сложности достаточно загрузить лишь миниатюры изображений.
* Для второго уровня сложности необходимо загрузить полноразмерные изображения.

**Используемые сторонние библиотеки:**

> requests \
> beautifulsoup4

### [Вариант №10 (Текстовые)](#section-2)

С использованием сервиса livelib соберите по 1000 рецензий для каждого количества звёзд для различных книг. То есть суммарный объём датасета 5000 рецензий. Сохраните каждый отзыв в отдельный текстовый файл, где на первой строке будет указано название книги.

**Не допускается:**

* Создание папок вручную. В коде должен быть отражен процесс создания папок и перемещения/загрузки в них файлов.
* Дублирование изображений для класса.

**Примечания**
* Именовать файлы необходимо порядковым номером (от 0 до 999).
* Для дальнейшего удобства необходимо дополнять имя файла ведующими нулями (например, 0000, 0001, ..., 0999). Для этого необходимо использовать один из методов класса str.
* Каждую рецензию сохраните в отдельный текстовый файл в соответствующую подпапку папки dataset. (Пути должны быть dataset/0/0001.txt, dataset/1/0001.txt, и т. д. по количеству звёзд)
* Обратите внимание, на то что страницы с отзывами необходимо обрабатывать в цикле.

**Вариант подразумевает два уровня сложности:**

* Для первого уровня сложности достаточно сохранить начало отзыва, показываемое на странице.
* Для второго уровня сложности необходимо сохранить отзыв полностью.

**Используемые сторонние библиотеки:**

> requests \
> beautifulsoup4