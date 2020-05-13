from system import Reservation, Reception
import reception
import unittest


class TestReception(unittest.TestCase):
    def setUp(self) -> None:
        self.reception = Reception()

    def tearDown(self) -> None:
        self.reception = Reception()

    def test_DefaultReception(self):
        self.assertEqual(self.reception.single_rooms, 5)
        self.assertEqual(self.reception.small_rooms, 5)
        self.assertEqual(self.reception.family_rooms, 5)
        self.assertEqual(self.reception.big_rooms, 5)
        self.assertEqual(self.reception.first_in_queue, 0)
        self.assertEqual(self.reception.clients, [])

    def test_CreateReservation(self):
        id1 = self.reception.create_reservation(6, 3, 3)
        self.assertIsInstance(id1, int)
        self.assertEqual(id1, 0)
        self.assertEqual(self.reception.clients[id1].room_type, 'family room')
        self.assertEqual(self.reception.clients[id1].youngest_guest, 3)
        self.assertEqual(self.reception.clients[id1].guests_number, 6)
        self.assertEqual(self.reception.clients[id1].duration_of_stay, 3)
        self.assertEqual(self.reception.get_status(id1), 'completed')
        self.assertEqual(self.reception.first_in_queue, 1)
        self.assertEqual(self.reception.departure(id1), 9000)

        id2 = self.reception.create_reservation(1, 34, 44)
        self.assertIsInstance(id2, int)
        self.assertEqual(id2, 1)
        self.assertEqual(self.reception.clients[id2].room_type, 'single room')
        self.assertEqual(self.reception.clients[id2].youngest_guest, 34)
        self.assertEqual(self.reception.clients[id2].guests_number, 1)
        self.assertEqual(self.reception.clients[id2].duration_of_stay, 44)
        self.assertEqual(self.reception.get_status(id2), 'completed')
        self.assertEqual(self.reception.first_in_queue, 2)
        self.assertEqual(self.reception.departure(id2), 66000)

        id3 = self.reception.create_reservation(2, 34, 2)
        self.assertIsInstance(id3, int)
        self.assertEqual(id3, 2)
        self.assertEqual(self.reception.clients[id3].room_type, 'small room')
        self.assertEqual(self.reception.clients[id3].youngest_guest, 34)
        self.assertEqual(self.reception.clients[id3].guests_number, 2)
        self.assertEqual(self.reception.clients[id3].duration_of_stay, 2)
        self.assertEqual(self.reception.get_status(id3), 'completed')
        self.assertEqual(self.reception.first_in_queue, 3)
        self.assertEqual(self.reception.departure(id3), 4000)

        id4 = self.reception.create_reservation(8, 34, 1)
        self.assertIsInstance(id4, int)
        self.assertEqual(id4, 3)
        self.assertEqual(self.reception.clients[id4].room_type, 'big room')
        self.assertEqual(self.reception.clients[id4].youngest_guest, 34)
        self.assertEqual(self.reception.clients[id4].guests_number, 8)
        self.assertEqual(self.reception.clients[id4].duration_of_stay, 1)
        self.assertEqual(self.reception.get_status(id4), 'completed')
        self.assertEqual(self.reception.first_in_queue, 4)
        self.assertEqual(self.reception.departure(id4), 2500)

    def test_Queue(self):
        id1 = self.reception.create_reservation(6, 3, 3)
        id2 = self.reception.create_reservation(1, 43, 2)
        self.assertEqual(self.reception.get_status(id2), 'queue')
        self.assertEqual(self.reception.get_bill(id2), 3000)
        self.assertEqual(self.reception.get_position_in_queue(id2), 1)

    def test_RoomsAreLimited(self):
        id1 = self.reception.create_reservation(4, 23, 3)
        id2 = self.reception.create_reservation(4, 23, 3)
        id3 = self.reception.create_reservation(4, 23, 3)
        id4 = self.reception.create_reservation(4, 23, 3)
        id5 = self.reception.create_reservation(4, 23, 3)
        id6 = self.reception.create_reservation(4, 23, 3)
        self.assertEqual(self.reception.clients[id6].room_type, 'none')
        self.assertEqual(self.reception.get_status(id6), 'rejected')

    def test_Clients(self):
        id1 = self.reception.create_reservation(4, 23, 3)
        self.assertIsInstance(self.reception.clients[id1], Reservation)
        self.assertEqual(len(self.reception.clients), 1)

    def test_RoomsCount(self):
        id1 = self.reception.create_reservation(4, 23, 3)
        self.assertEqual(self.reception.clients[id1].room_type, 'small room')
        self.assertEqual(self.reception.small_rooms, 4)


if __name__ == '__main__':
    unittest.main()
