pghero
======

pghero python port

– Work in progress.

Based on:
* [https://github.com/ankane/pghero/blob/master/lib/pghero.rb](https://github.com/ankane/pghero/blob/master/lib/pghero.rb)
* [http://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/](http://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/)
* The internetz.

Installation
------------
```bash
$ pip install pghero
```

Usage
-----

```python
from pghero.core import pghero
from sqlalchemy import create_engine 

db_path = 'postgres://username@host:port/db' 
db = create_engine(db_path)

pghero = pghero('sqlalchemy', db)
running_queries = pghero.running_queries() 
print running_queries

[out] => [86889, u'idle in transaction', datetime.timedelta(6, 21444, 452065), u'BEGIN', datetime.datetime(2014, 8, 3, 14, 6, 30, 186085, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=120, name=None))]
```
