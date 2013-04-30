import unittest
from tictactoe_game_engine import *

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
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, CROSS_CHECK_FAILED)

    def test_that_game_engine_correctly_verifies_consistency_2(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1']
        game_state['owned_by_zero'] = []
        who_moves_next = 1
        player_role_id = 1

        # apply_transformation
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, CROSS_CHECK_FAILED)

    def test_that_game_engine_correctly_verifies_consistency_3(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = []
        game_state['owned_by_zero'] = ['a2']
        who_moves_next = 1
        player_role_id = 0

        # apply_transformation
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, GAME_INCONSISTENCY)

    def test_that_game_engine_correctly_verifies_consistency_4(self):

        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1', 'a2']
        game_state['owned_by_zero'] = []
        who_moves_next = 1
        player_role_id = 0

        # apply_transformation
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, GAME_INCONSISTENCY)

    def test_that_parsed_response_is_a_hash(self):

        # define input
        parsed_response = []

        # apply transformation
        return_code = verify_readiness_of_game_bot(parsed_response)

        # assert
        self.assertEqual(return_code, INPUT_NOT_A_HASH)

    def test_that_parsed_response_contains_status_key(self):

        # define input
        parsed_response = {}

        # apply transformation
        return_code = verify_readiness_of_game_bot(parsed_response)

        # assert
        self.assertEqual(return_code, HASH_WITHOUT_STATUS_KEY)

    def test_that_status_key_of_parsed_response_points_to_ready(self):

        # define input
        parsed_response = {'status': 'not ready'}

        # apply transformation
        return_code = verify_readiness_of_game_bot(parsed_response)
        # assert
        self.assertEqual(return_code, VALUE_FOR_STATUS_IS_NOT_READY)
    
    def test_corectness_of_verify_win_combinations_1(self):
        
        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1', 'b3', 'c1']
        game_state['owned_by_zero'] = ['a2', 'b1', 'c3']
        who_just_moved = 2

        # apply transformation
        game_result = verify_win_combinations(game_state, who_just_moved)
        
        # assert
        self.assertEqual(game_result, DRAW)
    
    def test_corectness_of_verify_win_combinations_2(self):
        
        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1', 'b3', 'c1', 'b1']
        game_state['owned_by_zero'] = ['a2', 'b2', 'c3']
        who_just_moved = 1        

        # apply transformation
        game_result = verify_win_combinations(game_state, who_just_moved)
        
        # assert
        self.assertEqual(game_result, PLAYER_ONE_WON)
    
    def test_corectness_of_verify_win_combinations_3(self):
        
        # define input
        game_state = {}
        game_state['owned_by_x'] = ['a1', 'b3', 'c1', 'a3']
        game_state['owned_by_zero'] = ['a2', 'b2', 'c3', 'c2']
        who_just_moved = 2        

        # apply transformation
        game_result = verify_win_combinations(game_state, who_just_moved)
        
        # assert
        self.assertEqual(game_result, PLAYER_TWO_WON)

unittest.main()

