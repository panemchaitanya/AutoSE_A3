# Issue 2 (bug report) - posted to the fork on GitHub

Title: increment() crashes with KeyError when the field does not exist yet

Body:

I'm using `tinydb.operations.increment` for a page-view counter. The first
time a page is viewed the document has no `count` field yet, and instead of
just starting the counter at 1, TinyDB blows up:

```python
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from tinydb.operations import increment

db = TinyDB(storage=MemoryStorage)
db.insert({'page': '/home'})

db.update(increment('count'), doc_ids=[1])
# KeyError: 'count'
```

I would expect a counter on a missing field to simply start from 0, i.e.
after the call above the document should be `{'page': '/home', 'count': 1}`.
Same goes for `add` and `subtract`: adding 5 to a missing field should give
5, subtracting 3 should give -3. Right now I have to defensively insert
`count: 0` everywhere, which defeats the point.

TinyDB 4.9.0, Python 3.12.
