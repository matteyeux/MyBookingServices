# from booking import utils
from booking.models.rooms import Rooms

# from booking.config import config_api_setup
# from booking.database import Database


class Book(Rooms):
    """Book class model."""

    def do_book_room(self, data: dict) -> dict:
        """book room."""
        # pp = self.get_price_policies()
        # room = self.get_room_by_id(data['room_id'])
        #  price = utils.handle_pricing(data, pp, room)
        return {}
