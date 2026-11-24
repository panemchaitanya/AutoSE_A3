from tinydb import TinyDB
from tinydb.storages import MemoryStorage

def test_increment_missing_field():
    """Given a document without a 'count' field, when db.update(increment('count'), doc_ids=[1]) is executed, then the document shall be updated to include 'count': 1."""
    db = TinyDB(storage=MemoryStorage)
    db.insert({})
    from tinydb.operations import increment
    db.update(increment('count'), doc_ids=[1])
    assert db.get(doc_id=1) == {'count': 1}

def test_increment_missing_field_with_n():
    """Given a document without a 'count' field, when db.update(increment('count', n=5), doc_ids=[1]) is executed, then the document shall be updated to include 'count': 5."""
    db = TinyDB(storage=MemoryStorage)
    db.insert({})
    from tinydb.operations import increment
    db.update(increment('count', n=5), doc_ids=[1])
    assert db.get(doc_id=1) == {'count': 5}

def test_add_missing_field():
    """Given a document without a 'val' field, when db.update(add('val', 5), doc_ids=[1]) is executed, then the document shall be updated to include 'val': 5."""
    db = TinyDB(storage=MemoryStorage)
    db.insert({})
    from tinydb.operations import add
    db.update(add('val', 5), doc_ids=[1])
    assert db.get(doc_id=1) == {'val': 5}

def test_subtract_missing_field():
    """Given a document without a 'val' field, when db.update(subtract('val', 3), doc_ids=[1]) is executed, then the document shall be updated to include 'val': -3."""
    db = TinyDB(storage=MemoryStorage)
    db.insert({})
    from tinydb.operations import subtract
    db.update(subtract('val', 3), doc_ids=[1])
    assert db.get(doc_id=1) == {'val': -3}
