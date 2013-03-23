import unittest

class GameEngine():

    @staticmethod
    def verify_game_state_consistency(game_state, who_moves_next, player_role_id):

        why_the_game_ended_reason_id = 0
        size_of_owned_by_x = len(game_state['owned_by_x'])
        size_of_owned_by_zero = len(game_state['owned_by_zero'])

        if size_of_owned_by_x == size_of_owned_by_zero:
            player_role_id = 1

        if size_of_owned_by_x == 1 + size_of_owned_by_zero:
            player_role_id = 2

        if player_role_id != who_moves_next:
            why_the_game_ended_reason_id = 7

        if size_of_owned_by_x < size_of_owned_by_zero:
            why_the_game_ended_reason_id = 8

        if size_of_owned_by_x > 1 + size_of_owned_by_zero:
            why_the_game_ended_reason_id = 8

        return why_the_game_ended_reason_id




class TicTacToeTestSuite(unittest.TestCase):

    def test_that_a_player_cannot_move_into_an_already_occupied_board_cell(self):
        # define_input
        game_state = {}
        game_state['owned_by_x'] = ['c3']
        game_state['owned_by_zero'] = []
        game_state['who_moves_next'] = 0
        game_state['last_move_was_valid'] = True

        next_move = 'c3'

        # apply transformation
        occupied_board_positions = game_state['owned_by_x'] + game_state['owned_by_zero']
        game_state['last_move_was_valid'] = not next_move in occupied_board_positions

        # assert
        self.assertFalse(game_state['last_move_was_valid'])

    def test_that_game_engine_correctly_verifies_consistency_1(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = []
        game_state['owned_by_zero'] = []
        who_moves_next = 2
        player_role_id = 0

        # apply_transformation
        why_the_game_ended_reason_id = GameEngine.verify_game_state_consistency(game_state, who_moves_next, player_role_id)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, 7)

    def test_that_game_engine_correctly_verifies_consistency_2(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1']
        game_state['owned_by_zero'] = []
        who_moves_next = 1
        player_role_id = 1

        # apply_transformation
        why_the_game_ended_reason_id = GameEngine.verify_game_state_consistency(game_state, who_moves_next, player_role_id)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, 7)

    def test_that_game_engine_correctly_verifies_consistency_3(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = []
        game_state['owned_by_zero'] = ['a2']
        who_moves_next = 1
        player_role_id = 0

        # apply_transformation
        why_the_game_ended_reason_id = GameEngine.verify_game_state_consistency(game_state, who_moves_next, player_role_id)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, 8)

    def test_that_game_engine_correctly_verifies_consistency_4(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1', 'a2']
        game_state['owned_by_zero'] = []
        who_moves_next = 1
        player_role_id = 0

        # apply_transformation
        why_the_game_ended_reason_id = GameEngine.verify_game_state_consistency(game_state, who_moves_next, player_role_id)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, 8)


unittest.main()

