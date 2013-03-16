import unittest

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
       
    def test_that_game_engine_correctly_verifies_consistency(self):
       
        # define input
        game_state = {}
        game_state['owned_by_x'] = []
        game_state['owned_by_zero'] = []
        who_moves_next = 2
        why_the_game_ended_reason_id = 0

        # apply_transformation


        # assert
        self.assertEqual(why_the_game_ended_reason_id, 7)

unittest.main()

