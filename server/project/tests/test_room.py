import unittest
from project.tests.base import BaseTestCase
import project.controllers.room_controller as room_controller


class TestRoomController(BaseTestCase):
    """ Tests for Room Controller """

    def test_create_unique_room_id(self):
        """ Ensure the length of the room id is four and unique. """

        test_id = room_controller.create_unique_room_id()
        test_id_two = room_controller.create_unique_room_id()
        self.assertEqual(len(test_id), 4)
        self.assertNotEqual(test_id, test_id_two)

    def test_join_game_room(self):
        """ Ensure the user joins in a room correctly. """

        room_controller.join_game_room('ABCD', 'chris')
        validate = room_controller.is_user_in_room('ABCD', 'chris')
        self.assertTrue(validate, True)


if __name__ == '__main__':
    unittest.main()
