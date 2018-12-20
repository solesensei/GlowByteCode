# Auto FAT / UAT
Скрипт автоматически создающий PDF документы FAT и UAT с цифровой подписью используя Pylatex.

Автор: Гончаренко Дмитрий, GlowByte Consulting

## Использование 

1. Положить в папку картинку с подписью на прозрачном фоне с названием: `sign.png`.
2. Заполнить файл `fat.txt`
3. Запустить `makeFAT.exe` через консоль или кликом

## LaTeX
Для корректной работы требуется установить LaTeX.

1. Скачайте __latex_portable.zip__ : `rsbt-assasrm1~/home/sas/tex/`
2. Разархивируйте __latex_portable.zip__
3. Добавьте в PATH: `PATH_TO_LATEX_FOLDER\texmfs\install\miktex\bin`
4. Выполните `latex.cmd`
5. Проверьте что все работает командой `tex` в терминале

```bash
$ tex
This is TeX, Version 3.14159265 (MiKTeX 2.9.6730)
**
```

## Pyinstaller

__On Windows 10:__

```bash
# Creating init .spec file 
pyinstaller --onefile --icon=.\\img\\rsb.ico pyTeX.py -n makeFAT
```
```bash
# Modifing makeFAT.spec with this line
a.datas += [ ('rsb.png', '.\\img\\rsb.png', 'DATA'), ('rsb.ico', '.\\img\\rsb.ico', 'DATA')]
```
```bash
# Creating exe 
pyinstaller.exe --onefile --icon=.\\img\\rsb.ico --specpath=./spec/ makeFAT.spec
```
