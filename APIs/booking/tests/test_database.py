from booking.database import Database


def test_database_access():
    """Check if Database.engine is None
    when using wrong creds."""
    db = Database(
        user='pouet',
        password='pouet',
        host='127.0.0.1',
        database='mydb',
    )
    assert db.engine is None
