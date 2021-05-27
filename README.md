# ml_engineering_example

В этом репозитории представлен пример организации кода для задачи предсказания влажности листа.

## Описание задачи:

Влажность листьев - это метеорологический параметр, который описывает количество росы и осадков, оставшихся на поверхности.

Существуют датчики для детекции влажности листьев. В приложенном excel-файле результаты измерения такого датчика https://metos.at/ru/portfolio/leaf-wetness/

Кроме того, в той же таблице записаны результаты прочих метеорологических измерений, данные собирались синхронно с фиксацией влажности листьев в том же месте, где располагался датчик.

Оцените возможность определения влажности листьев без использования датчика (используя прочие данные из таблицы). 

Ноутбук с изначальным решением находится в `notebooks/result_from_attendee.ipynb` .

## Запуск

Данные задачи `station_data.xlsx` необходимо положить в папку `datasets`. Чтобы запускать ноутбуки нужно создать ссылку как в `notebooks/01_EDA.ipynb` .

Используется виртуальное окружение с Python 3.6 и версиями библиотек `requirements.txt` .

```pip install -r requirements.txt```

## Запуск линтера (локальный)

Flake8 инструмент, который проверяет PEP8, сложность кода по Mccabe и частые ошибки Python. К нему есть много расширений с дополнительными проверками. К нему устанавливается плагин Wemake-python-styleguide, который как раз и содержит много полезных расширений. У него активная стадия разработки и примерно 1400 Stars на Github. Flakehell утилита, которая позволяет добавить уже разработанный код в "исключения" и не проверять его, пока он не начнет меняться.

Теорию про линтеры подробнее можно почитать тут:

https://habr.com/ru/company/oleg-bunin/blog/433480/

https://github.com/wemake-services/wemake-python-styleguide

Конфиг берется из файла .pyproject.toml. Там описаны правила, которые Flake8 НЕ отлавливает.

```flakehell lint source --config pyproject.toml```

## Запуск теста

```pytest source```
