# About
Универсальный клиент выполнения SQL скрипта в СУБД MYSQL, ORACLE, POSTGRES с экспортом результатов в CSV файл.

Разочарован в rlwrap м SQLPlus. :sad: 

# Requirements

`python>=3.7`

```requirements.txt
build==0.7.0
colorama==0.4.4
cx-Oracle==8.2.1
packaging==21.3
pep517==0.12.0
psycopg2==2.9.1
PyMySQL==1.0.2
pyparsing==3.0.7
tomli==2.0.1
```

```shell
pip install -r requirements.txt
```

# Build

```shell
python -m pip install --upgrade build
python -m build
```

# Install package

```shell
pip install pydb-x.y.z-py3-none-any.whl
```

# Usage package

For example: direct usage past connection config and sql query into script

```python
from pydb.exporter import Exporter
from pydb.dbms import UniDbConnector


cfg = dict(host='localhost', port=3306, user='', password='', database='profit', dbms='mysql')
u = UniDbConnector(config=cfg)

q = 'SELECT * FROM table ;'
data = u.fetchall(query=q)

e = Exporter(filename='data')
e.to_csv(data=data)

```