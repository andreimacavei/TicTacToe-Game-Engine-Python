import unittest
import json
import sys

    
# define constants
DRAW = 0
PLAYER_ONE_WON = 1
PLAYER_TWO_WON = 2
PLAYER_ONE_NOT_READY = 3
PLAYER_TWO_NOT_READY = 4
ILLEGAL_MOVE_BY_PLAYER_ONE = 5
ILLEGAL_MOVE_BY_PLAYER_TWO = 6
CROSS_CHECK_FAILED = 7
GAME_INCONSISTENCY = 8

EVERYTHING_OK = 10
INPUT_NOT_A_HASH = 11
HASH_WITHOUT_STATUS_KEY = 12
VALUE_FOR_STATUS_IS_NOT_READY = 13

def verify_game_state_consistency(game_state, who_moves_next, player_role_id):

    why_the_game_ended_reason_id = DRAW
    size_of_owned_by_x = len(game_state['owned_by_x'])
    size_of_owned_by_zero = len(game_state['owned_by_zero'])

    if size_of_owned_by_x == size_of_owned_by_zero:
        player_role_id = 1

    if size_of_owned_by_x == 1 + size_of_owned_by_zero:
        player_role_id = 2

    if player_role_id != who_moves_next:
        why_the_game_ended_reason_id = CROSS_CHECK_FAILED

    if size_of_owned_by_x < size_of_owned_by_zero:
        why_the_game_ended_reason_id = GAME_INCONSISTENCY

    if size_of_owned_by_x > 1 + size_of_owned_by_zero:
        why_the_game_ended_reason_id = GAME_INCONSISTENCY

    return why_the_game_ended_reason_id

def verify_readiness_of_game_bot(parsed_response):
     
    if (type(parsed_response) is not dict):
        return INPUT_NOT_A_HASH
    
    if ('status' not in parsed_response):
        return HASH_WITHOUT_STATUS_KEY

    if (parsed_response['status'] != 'ready'):
        return VALUE_FOR_STATUS_IS_NOT_READY

    return EVERYTHING_OK


def start_game():
    output_of_game_engine_input_of_player_1 = sys.argv[1]
    output_of_player_1_input_of_game_engine = sys.argv[2]
    output_of_game_engine_input_of_player_2 = sys.argv[3]
    output_of_player_2_input_of_game_engine = sys.argv[4]

    request_status = {'request': 'status'}
    
    print "waiting to write"

    f = open(output_of_game_engine_input_of_player_1, 'w')
    print >> f, json.dumps(request_status)
    f.close()
    
    print "waiting to read"

    f = open(output_of_player_1_input_of_game_engine, 'r')
    try:
        raw_response = f.read()
    finally:
        f.close()
    
    parsed_response = json.loads(raw_response)


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
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next, player_role_id)

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
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next, player_role_id)

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
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next, player_role_id)

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
        why_the_game_ended_reason_id = verify_game_state_consistency(game_state, who_moves_next, player_role_id)

        # assert
        self.assertEqual(why_the_game_ended_reason_id, GAME_INCONSISTENCY)

    def test_that_parsed_response_is_a_hash(self):

        # define input
        parsed_response = []
        return_code = 0
        
        # apply transformation
        return_code = verify_readiness_of_game_bot(parsed_response)

        # assert
        self.assertEqual(return_code, 11)
    
    def test_that_parsed_response_contains_status_key(self):

        # define input
        parsed_response = {}
        return_code = 0
        
        # apply transformation
        return_code = verify_readiness_of_game_bot(parsed_response)

        # assert
        self.assertEqual(return_code, 12)

    def test_that_status_key_of_parsed_response_points_to_ready(self):
        
        # define input
        parsed_response = {'status': 'not ready'}
        return_code = 0
        
        # apply transformation 
        return_code = verify_readiness_of_game_bot(parsed_response)
        # assert
        self.assertEqual(return_code, 13)


unittest.main()
#start_game()

