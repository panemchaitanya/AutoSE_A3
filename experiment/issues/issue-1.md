# Issue 1 (bug report) - posted to the fork on GitHub

Title: update() and remove() silently do nothing when I pass the doc id as a string

Body:

I spent an hour debugging this. `db.get(doc_id='1')` finds my document fine,
but when I pass the same id as a string to `update` or `remove`, nothing
happens. No error, no warning, the document is just unchanged.

```python
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)
db.insert({'x': 1})

print(db.get(doc_id='1'))            # {'x': 1}  <- works
print(db.update({'x': 2}, doc_ids=['1']))  # []   <- silently did nothing!
print(db.all())                      # [{'x': 1}] <- unchanged
print(db.remove(doc_ids=['1']))      # []   <- same here
print(len(db))                       # 1
```

Passing the int `1` instead of `'1'` works. My ids come from a web form so
they are always strings, and I really do not want to crash on every bad
input either - but a silent no-op on a write is the worst of both worlds.
Please make these consistent with `get` (which accepts the string form).

TinyDB 4.9.0, Python 3.12.
