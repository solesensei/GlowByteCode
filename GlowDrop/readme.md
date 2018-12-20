# GlowDrop
Скрипт предназначен для отправки и скачивания файлов через rest api confluence GBC

## Использование
### Отправка файла
Загрузка файла в attachements wiki GBC
```bash
python GlowDrop.py -s filepath
```

## Скачивание файла
Поиск по всем отправленным файлам и скачивание найденного
```bash
python GlowDrop.py -g filename
```

## Отправка email через smtp
Отправка email сообщения с ссылкой на скачивание отправленного файла (требуется авторизация GBC)
```bash
python GlowDrop.py -s file -e
```

## Файл конфигурации
Генерация начального файла конфигурации
```bash
python GlowDrop.py --make_conf
```

### Помощь
Для контекстного меню помощи используйте 
```bash
python GlowDrop.py --help
```