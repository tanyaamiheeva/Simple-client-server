POSSIBLE_FIELDS = ['guests', 'youngest', 'duration']
PRICE_OF_FAMILY_ROOM = 3000
PRICE_OF_BIG_ROOM = 2500
PRICE_OF_SMALL_ROOM = 2000
PRICE_OF_SINGLE_ROOM = 1500


class Reservation:
    def __init__(self, reservation_id, guests=0, youngest_guest=0, duration=0):
        self.id = reservation_id
        self.youngest_guest = youngest_guest
        self.guests_number = guests
        self.duration_of_stay = duration
        self.status = 'queue'
        self.room_type = 'none'
        self.bill = 0


class Reception:
    def __init__(self):
        self.clients = []
        self.first_in_queue = 0
        self.family_rooms = 5
        self.big_rooms = 5
        self.small_rooms = 5
        self.single_rooms = 5

    def create_reservation(self, guests=0, youngest=0, duration=0):
        reservation_id = len(self.clients)
        new_reservation = Reservation(reservation_id, guests, youngest, duration)
        room = self.get_best_variant(youngest, guests)
        if room == 'failed':
            new_reservation.status = 'rejected'
        else:
            new_reservation.room_type = room
        self.clients.append(new_reservation)
        print(reservation_id)
        return reservation_id

    def get_best_variant(self, youngest, guests):
        if youngest < 12 and self.family_rooms > 0:
            self.family_rooms -= 1
            return 'family room'
        elif guests > 4 and self.big_rooms > 0:
            self.big_rooms -= 1
            return 'big room'
        elif 4 >= guests > 1 and self.small_rooms > 0:
            self.small_rooms -= 1
            return 'small room'
        elif guests == 1 and self.single_rooms > 0:
            self.single_rooms -= 1
            return 'single room'
        else:
            return 'failed'

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
        return reservation.id - self.first_in_queue

    def get_bill(self, reservation_id):
        reservation = self.clients[reservation_id]
        if reservation.room_type == 'family room':
            reservation.bill = PRICE_OF_FAMILY_ROOM * reservation.duration_of_stay
        elif reservation.room_type == 'big room':
            reservation.bill = PRICE_OF_BIG_ROOM * reservation.duration_of_stay
        elif reservation.room_type == 'small room':
            reservation.bill = PRICE_OF_SMALL_ROOM * reservation.duration_of_stay
        elif reservation.room_type == 'single room':
            reservation.bill = PRICE_OF_SINGLE_ROOM * reservation.duration_of_stay
        return reservation.bill
