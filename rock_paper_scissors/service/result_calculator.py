import logging
from collections import Counter

from model.models import TurnResult, Game

from model.payload import TurnPayload, GameResponse
from repository.game_repository import GameRepository

WINNER_BY_MOVE = {"rock": "scissor", "paper": "rock", "scissors": "paper"}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calculate_turn_result(turn: TurnPayload):
    is_draw = False
    winner = None

    if turn.first_player_move == turn.second_player_move:
        is_draw = True
    elif turn.second_player_move == WINNER_BY_MOVE.get(turn.first_player_move):
        winner = turn.first_player_name
    else:
        winner = turn.second_player_name

    return TurnResult(is_draw, winner)


def process_request(turn: TurnPayload) -> GameResponse:
    # Load saved games
    repository = GameRepository()

    accumulated_score = _get_current_accumulated_scores(repository, turn)
    logger.info(f"Loaded accumulated scores {accumulated_score}")

    # Calculate current result
    turn_result = calculate_turn_result(turn)
    logger.info(f"Calculated current turn results: {turn_result}")

    # Update accumulated result
    if turn_result.is_draw:
        accumulated_score[None] += 1
    else:
        accumulated_score[turn_result.winner] += 1
    logger.info(f"Updated accumulated score: {accumulated_score}")

    # Update game with turn and Return game with accumulated score
    updated_game = repository.add_turn_to_game(turn.first_player_name, turn.second_player_name, turn_result)
    logger.info(f"Updated game with turn and accumulated score: {updated_game}")

    updated_scores = calculate_scores(updated_game)
    logger.info(f"Calculated updated accumulated score: {updated_scores}")

    return GameResponse(is_draw=turn_result.is_draw, winner=turn_result.winner, accumulated_score=updated_scores)


def _get_current_accumulated_scores(repository, turn):
    # Check if game exists based on usernames
    game = repository.load_by_players(turn.first_player_name, turn.second_player_name)
    if not game:
        logging.info("Game not found. Creating new game")
        # If not, create a game
        game = repository.create_game(turn.first_player_name, turn.second_player_name)
    logging.info(f"Prepared game {game}")
    # Load current scores
    return calculate_scores(game)


def calculate_scores(game: Game):
    results = Counter()
    if game.turns:
        results = Counter(turn.winner for turn in game.turns)

    if game.first_player not in results:
        results[game.first_player] = 0

    if game.second_player not in results:
        results[game.second_player] = 0

    # TODO change this to not use None
    if None not in results:
        results[None] = 0

    # This is a bad workaround to format the None results as draw
    results["draw"] = results[None]
    del results[None]

    # Sum results by turn
    return results


def increment_result():
    # API is stateless. It's not possible to store the current results in memory
    # Need to implement saving results before this feature
    pass
