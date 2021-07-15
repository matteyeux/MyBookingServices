from booking.database import Database


class Rooms:
    """Rooms class model."""

    def __init__(self):
        self.db = Database(
            user="etna",
            password="etna",
            host="localhost",
            database="mybookingservices",
        )

    def get_all_rooms(self):
        """Return all rooms."""
        return self.db.get_rooms()

    def get_room_by_id(self, room_id: int = 1):
        """Get room info by ID."""
        # if room_id == 0 get latest added room ?
        return self.db.get_room_by_id(room_id)
