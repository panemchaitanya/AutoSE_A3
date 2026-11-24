from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

def test_table_search_limit_two():
    """Given a table with multiple matching documents, When calling table.search(cond, limit=2), Then at most 2 matching documents are returned in document id order."""
    db = TinyDB(storage=MemoryStorage)
    table = db.table('test')
    table.insert({'value': 1})
    table.insert({'value': 2})
    table.insert({'value': 3})
    table.insert({'value': 4})
    
    cond = Query()
    results = table.search(cond.value > 0, limit=2)
    assert len(results) == 2
    assert results[0].doc_id == 1
    assert results[1].doc_id == 2

def test_table_search_limit_none():
    """Given a table with matching documents, When calling table.search(cond, limit=None), Then all matching documents are returned in document id order."""
    db = TinyDB(storage=MemoryStorage)
    table = db.table('test')
    table.insert({'value': 1})
    table.insert({'value': 2})
    table.insert({'value': 3})
    
    cond = Query()
    results = table.search(cond.value > 0, limit=None)
    assert len(results) == 3
    assert [r.doc_id for r in results] == [1, 2, 3]

def test_table_search_limit_exceeds_count():
    """Given a table with matching documents, When calling table.search(cond, limit=100) where 100 exceeds match count, Then all matching documents are returned."""
    db = TinyDB(storage=MemoryStorage)
    table = db.table('test')
    table.insert({'value': 1})
    table.insert({'value': 2})
    
    cond = Query()
    results = table.search(cond.value > 0, limit=100)
    assert len(results) == 2
    assert [r.doc_id for r in results] == [1, 2]

def test_tinydb_search_limit():
    """Given a database instance db, When calling db.search(cond, limit=5), Then at most 5 matching documents from the default table are returned."""
    db = TinyDB(storage=MemoryStorage)
    for i in range(10):
        db.insert({'value': i})
        
    cond = Query()
    results = db.search(cond.value >= 0, limit=5)
    assert len(results) == 5
    assert [r.doc_id for r in results] == [1, 2, 3, 4, 5]
