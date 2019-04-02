# CISParser

Утилита для парсинга `.xml` содержимого кампаний RTDM из SAS MC: Decision Services

Преобразует в чистый, читаемый и стандартизированный исходный код, пригодный для хранения и чтения изменений в системах контроля версий.

## Использование

### Вход

Текстовое содержимое **RTDM** стратегии полученное через SAS Management Console через плагин Decision Servives 

```txt
company_name.xml
```

Доступен режим батчевой обработки сразу нескольких кампаний

```txt
directory_with_companies/
                        company1.xml
                        company2.xml
                        ...
                        companyN.xml
```


### Выход

Обработанный `.xml` файл унифицированного формата


### Флаги

Доступные флаги можно посмотреть командой вызова контекстной помощи

```bash
./CISParser.exe --help
# or
python CISParser.py -h
```

## Конфиг

Возможно использовать конфиг файл для настройки параметров работы скрипта

Создать конфиг можно следующей командой

```bash
./CISParser.exe --config
# or
python CISParser.py --config
```

Пример конфиг файла:

```yaml
# Config file for CISParser
# ----------------------------------- #
debug: False   # Launch in debug mode

# ----------------------------------- #
path:   './xml'   # Set path to process
config: True   # Path to config file
encode: True   # Do not change encoding of files to UTF-8 and remove ASCII codes
xml:    True   # Do not delete metadata and convert to real xml format
parse:  True   # Do not parse CIS xml
sort:   True   # Do not sort CIS campaign
wrap:   True   # Do not wrap groups of nodes
```

## Build exe

```bash
pyinstaller --onefile .\\spec\\CISParser.spec
```

## Инструменты

Python 3.7.1, Windows 10

made with ❤ by Sole