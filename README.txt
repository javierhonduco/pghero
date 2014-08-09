pghero
======

pghero python port

– Work in progress.

Based on:
* [https://github.com/ankane/pghero/blob/master/lib/pghero.rb](https://github.com/ankane/pghero/blob/master/lib/pghero.rb)
* [http://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/](http://www.craigkerstiens.com/2013/01/10/more-on-postgres-performance/)
* The internetz.

Usage
-----

```python
from core import pghero 
from sqlalchemy import create_engine 

db_path = 'postgres://username@host:port/db' 

db = create_engine(db_path)

pghero = pghero('sqlalchemy', db)
```
