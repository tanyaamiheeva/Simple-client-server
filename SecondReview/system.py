from utility import Constants
POSSIBLE_FIELDS = ['guests', 'youngest', 'duration']


class Rooms:
    def __init__(self):
        self.family_rooms = Constants.family_rooms_count
        self.big_rooms = Constants.big_rooms_count
        self.small_rooms = Constants.small_rooms_count
        self.single_rooms = Constants.single_rooms_count
        self.prices = Constants.prices


class Reservation:
    def __init__(self, reservation_id, guests=0, youngest_guest=0, duration=0):
        self.id = reservation_id
        self.youngest_guest = youngest_guest
        self.guests_number = guests
        self.duration_of_stay = duration
        self.status = 'queue'
        self.room_type = None
        self.bill = 0


class Reception:
    def __init__(self):
        self.clients = []
        self.first_in_queue = 0
        self.rooms = Rooms()

    def create_reservation(self, guests, youngest, duration):
        reservation_id = len(self.clients)
        new_reservation = Reservation(reservation_id, guests, youngest, duration)
        room = self.get_best_variant(youngest, guests)
        if room is None:
            new_reservation.status = 'rejected'
        else:
            new_reservation.room_type = room
            new_reservation.bill = self.rooms.prices[room] * duration
        self.clients.append(new_reservation)
        return reservation_id

    def get_best_variant(self, youngest, guests):
        if youngest < Constants.youngest_age and self.rooms.family_rooms > 0:
            self.rooms.family_rooms -= 1
            return 'family room'
        elif guests > Constants.guests_for_big_room and self.rooms.big_rooms > 0:
            self.rooms.big_rooms -= 1
            return 'big room'
        elif Constants.guests_for_big_room >= guests > 1 and self.rooms.small_rooms > 0:
            self.rooms.small_rooms -= 1
            return 'small room'
        elif guests == Constants.single_guest and self.rooms.single_rooms > 0:
            self.rooms.single_rooms -= 1
            return 'single room'
        else:
            return None

    def get_status(self, reservation_id):
        self.registration(reservation_id)
        return self.clients[reservation_id].status

    def get_room_type(self, reservation_id):
        return self.clients[reservation_id].room_type

    def registration(self, reservation_id):
        reservation = self.clients[reservation_id]
        if reservation_id != self.first_in_queue:
            return
        if reservation.status == 'queue':
            reservation.status = 'completed'
            self.first_in_queue += 1

    def departure(self, reservation_id):
        reservation = self.clients[reservation_id]
        bill = self.get_bill(reservation_id)
        if reservation.status == 'completed':
            reservation.status = 'outdated'

        return bill

    def get_position_in_queue(self, reservation_id):
        reservation = self.clients[reservation_id]
        return reservation.id - self.first_in_queue + 1

    def get_bill(self, reservation_id):
        return self.clients[reservation_id].bill
