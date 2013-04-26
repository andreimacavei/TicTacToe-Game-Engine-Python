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

STATUS_MESSAGES = {

    DRAW: 'Draw',
    PLAYER_ONE_WON: 'Player 1 won',
    PLAYER_TWO_WON: 'Player 2 won',
    PLAYER_ONE_NOT_READY: 'Player 1 is not ready',
    PLAYER_TWO_NOT_READY: 'Player 2 is not ready',
    ILLEGAL_MOVE_BY_PLAYER_ONE: 'Illegal move by player 1',
    ILLEGAL_MOVE_BY_PLAYER_TWO: 'Illegal move by player 2',
    CROSS_CHECK_FAILED: 'Cross check failed',
    GAME_INCONSISTENCY: 'Game inconsistency',

    EVERYTHING_OK: 'Everything is ok',
    INPUT_NOT_A_HASH: 'The input i recieved was not a hash',
    HASH_WITHOUT_STATUS_KEY: 'Hash i recieved does not have a status key',
    VALUE_FOR_STATUS_IS_NOT_READY: 'The status key does not point to ready'

}

class PlayerInfo:

    def __init__(self, input_channel, output_channel, player_role, game_state_key):
        self.input_channel = input_channel
        self.output_channel = output_channel
        self.player_role = player_role
        self.game_state_key = game_state_key

def verify_game_state_consistency(game_state, who_moves_next):

    why_the_game_ended_reason_id = DRAW
    size_of_owned_by_x = len(game_state['owned_by_x'])
    size_of_owned_by_zero = len(game_state['owned_by_zero'])
    
    print game_state['owned_by_x']
    print game_state['owned_by_zero']
    print size_of_owned_by_x
    print size_of_owned_by_zero

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

    # Verify readiness of player 1
    print "waiting to write : output -> player1"

    f = open(output_of_game_engine_input_of_player_1, 'w')
    print >> f, json.dumps(request_status)
    f.close()

    print "waiting to read : input <- player1"

    f = open(output_of_player_1_input_of_game_engine, 'r')
    try:
        raw_response = f.read()
    finally:
        f.close()
    try:
        parsed_response = json.loads(raw_response)
    except:
        print "player 2 won"
        exit
    return_code = verify_readiness_of_game_bot(parsed_response)
    if (return_code != EVERYTHING_OK):
        print STATUS_MESSAGES[return_code]
        exit

    # Verify readiness of player 2
    print "waiting to write : output -> player2"

    f = open(output_of_game_engine_input_of_player_2, 'w')
    print >> f, json.dumps(request_status)
    f.close()

    print "waiting to read : input <- player2"

    f = open(output_of_player_2_input_of_game_engine, 'r')
    try:
        raw_response = f.read()
    finally:
        f.close()
    try:
        parsed_response = json.loads(raw_response)
    except:
        print "player 1 won"
        exit

    return_code = verify_readiness_of_game_bot(parsed_response)
    if (return_code != EVERYTHING_OK):
        print STATUS_MESSAGES[return_code]
        exit

    # Players are ready - starting the actual game
    who_moves_next = 2
    game_state = {
        'owned_by_x' : [],
        'owned_by_zero' : []    
    }

    player_data = {
        1: PlayerInfo(
                output_of_game_engine_input_of_player_1,
                output_of_player_1_input_of_game_engine,
                'x',
                'owned_by_x'
           ),
        2: PlayerInfo(
                output_of_game_engine_input_of_player_2,
                output_of_player_2_input_of_game_engine,
                'zero',
                'owned_by_zero'
           )
    }
    
    for turn in range(1,10):
        who_moves_next = 3 - who_moves_next
        return_code = verify_game_state_consistency(game_state, who_moves_next)
        if return_code !=  DRAW:
            print STATUS_MESSAGES[return_code]
            exit
        
        request_status = {
            'request': 'play_your_turn',
            'player_role': player_data[who_moves_next].player_role,
            'owned_by_x': game_state['owned_by_x'],
            'owned_by_zero': game_state['owned_by_zero']
        }
        # Signal player to make his turn
        print "waiting to move : player " , who_moves_next
        
        f = open(player_data[who_moves_next].input_channel, 'w')
        print >> f, json.dumps(request_status)
        f.close()
       

        print "waiting to read : player " , who_moves_next

        f = open(player_data[who_moves_next].output_channel, 'r')
        try:
            raw_response = f.read()
        finally:
            f.close()
        try:
            parsed_response = json.loads(raw_response)
        except:
            print "player ? won"
            exit
        
        # show status
        print parsed_response['turn'].encode('ascii')
        game_state[player_data[who_moves_next].game_state_key].append(
            parsed_response['turn'].encode('ascii')
        )

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


#unittest.main()
start_game()

