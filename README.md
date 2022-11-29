# About
Universal python client for MYSQL, ORACLE, POSTGRES.

### Features
<ul>
    <li>Inline CLI usage</li>
    <li>Script usage</li>
    <li>CSV Export</li>
    <li>ZIP export result</li>
</ul> 

# Requirements

Language: `python>=3.7`

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
### CLI example
```shell
python  dbclient.py -c "postgres://user:password@hostname:port/database"
command> SELECT * FROM systems ORDER BY id;
+----+-----------------+------------+------------+
| id | system          | system_key | system_eng |
+----+-----------------+------------+------------+
| 1  | Анализаторы SNT | SNT        | None       |
| 2  | Капкан          | KAPKAN     | None       |
| 3  | Спайдер         | SPIDER     | SPIDER     |
| 4  | Профит          | PROFIT     | PROFIT     |
+----+-----------------+------------+------------+
```

### Script example

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