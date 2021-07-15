from booking.database import Database


class Book:
    """Rooms class model."""

    def __init__(self):
        self.db = Database(
            user="etna",
            password="etna",
            host="localhost",
            database="mybookingservices",
        )

    def get_available_rooms(self):
        """Get available rooms to book."""
        return self.db.get_available_rooms()
