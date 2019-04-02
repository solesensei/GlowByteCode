# XMLGenerator

Инструмент по генерации `xml` для регрессов. (создавалась под SGCheck, требует доработки).

## [Библиотеки](./modules)

Реализованные библиотеки

### [clean_base.py](./modules/clean_base.py)

Инструмент для очистки `.csv` баз данных с export-base и получения чистой версии для парсинга

```py
def start_cleaning(datapath, delimiter=';', quotechar='"'):
    """
        Returns filename of clean version of input base
        --
        datapath : str - path to base.csv
    """
```

### [inn.py](./modules/inn.py)

Библиотека получения ИНН из базы export-base

```py
def get_company_inn(datapath, delimiter=';', quotechar='"'):
    """
    Returns 'INN' list from database
    --
    datapath : str - path to database with 'INN' column
    """
```