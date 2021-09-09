from booking import utils
from booking.models.rooms import Rooms

# from booking.config import config_api_setup
# from booking.database import Database


class Book(Rooms):
    """Book class model."""

    def do_book_room(self, user_id: int, data: dict) -> dict:
        """Book room and return data."""
        pp = self.get_price_policies()
        options = self.get_all_options()
        room = self.get_room_by_id(data['room_id'])
        price = utils.handle_pricing(data, pp, room, options)
        data['price'] = price

        if self.db.engine is not None:
            self.db.insert_reservation_into_db(user_id, data)
        return data

    def delete_booking_room(self, booking_id):
        """Delete booking room by its id"""
        if self.db.engine is not None:
            return self.db.delete_reservation_into_db(booking_id)
        else:
            return None
