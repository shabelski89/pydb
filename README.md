# About
Универсальный клиент выполнения SQL скрипта в СУБД MYSQL, ORACLE, POSTGRES с экспортом результатов в CSV файл.

Разочарован в rlwrap м SQLPlus. :sad: 

# Requirements
```shell
python>=3.7
build>=0.7.0
colorama>=0.4.4
cx-Oracle>=8.2.1
packaging>=21.3
pep517>=0.12.0
psycopg2>=2.9.1
PyMySQL>=1.0.2
pyparsing>=3.0.7
tomli>=2.0.1
```

# Help

```python
from pydb.dbms import UniDbConnector
from pydb.exporter import Exporter

```
