from system import Reservation, Reception
import reception
import unittest


class TestReception(unittest.TestCase):
    def setUp(self) -> None:
        self.reception = Reception()

    def tearDown(self) -> None:
        self.reception = Reception()

    def testDefaultReception(self):
        self.assertEqual(self.reception.rooms.single_rooms, 5)
        self.assertEqual(self.reception.rooms.small_rooms, 5)
        self.assertEqual(self.reception.rooms.family_rooms, 5)
        self.assertEqual(self.reception.rooms.big_rooms, 5)
        self.assertEqual(self.reception.first_in_queue, 0)
        self.assertEqual(self.reception.clients, [])

    def testCreateReservation(self):
        reservations = [self.reception.create_reservation(6, 3, 3),
                        self.reception.create_reservation(1, 34, 44),
                        self.reception.create_reservation(2, 34, 2),
                        self.reception.create_reservation(8, 34, 1)]
        for i in range(0, len(reservations)):
            self.assertIsInstance(reservations[i], int)
            self.assertEqual(reservations[i], i)
            self.assertEqual(self.reception.get_status(reservations[i]), 'completed')
            self.assertEqual(self.reception.first_in_queue, i + 1)

        self.assertEqual(self.reception.clients[reservations[0]].room_type, 'family room')
        self.assertEqual(self.reception.clients[reservations[0]].youngest_guest, 3)
        self.assertEqual(self.reception.clients[reservations[0]].guests_number, 6)
        self.assertEqual(self.reception.clients[reservations[0]].duration_of_stay, 3)
        self.assertEqual(self.reception.departure(reservations[0]), 9000)

        self.assertEqual(self.reception.clients[reservations[1]].room_type, 'single room')
        self.assertEqual(self.reception.clients[reservations[1]].youngest_guest, 34)
        self.assertEqual(self.reception.clients[reservations[1]].guests_number, 1)
        self.assertEqual(self.reception.clients[reservations[1]].duration_of_stay, 44)
        self.assertEqual(self.reception.departure(reservations[1]), 66000)

        self.assertEqual(self.reception.clients[reservations[2]].room_type, 'small room')
        self.assertEqual(self.reception.clients[reservations[2]].youngest_guest, 34)
        self.assertEqual(self.reception.clients[reservations[2]].guests_number, 2)
        self.assertEqual(self.reception.clients[reservations[2]].duration_of_stay, 2)
        self.assertEqual(self.reception.departure(reservations[2]), 4000)

        self.assertEqual(self.reception.clients[reservations[3]].room_type, 'big room')
        self.assertEqual(self.reception.clients[reservations[3]].youngest_guest, 34)
        self.assertEqual(self.reception.clients[reservations[3]].guests_number, 8)
        self.assertEqual(self.reception.clients[reservations[3]].duration_of_stay, 1)
        self.assertEqual(self.reception.departure(reservations[3]), 2500)

    def testQueue(self):
        reservations = [self.reception.create_reservation(6, 3, 3),
                        self.reception.create_reservation(1, 43, 2)]
        self.assertEqual(self.reception.get_status(reservations[1]), 'queue')
        self.assertEqual(self.reception.get_bill(reservations[1]), 3000)
        self.assertEqual(self.reception.get_position_in_queue(reservations[1]), 2)

    def testRoomsAreLimited(self):
        reservations = [self.reception.create_reservation(4, 23, 3) for i in range(6)]
        self.assertEqual(self.reception.clients[reservations[5]].room_type, 'none')
        self.assertEqual(self.reception.get_status(reservations[5]), 'rejected')

    def testClients(self):
        id = self.reception.create_reservation(4, 23, 3)
        self.assertIsInstance(self.reception.clients[id], Reservation)
        self.assertEqual(len(self.reception.clients), 1)

    def testRoomsCount(self):
        id = self.reception.create_reservation(4, 23, 3)
        self.assertEqual(self.reception.clients[id].room_type, 'small room')
        self.assertEqual(self.reception.rooms.small_rooms, 4)


if __name__ == '__main__':
    unittest.main()
