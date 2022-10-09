import datetime
import json
import logging
from dataclasses import asdict
from typing import List

from model.models import Game, Turn, TurnResult
from settings import GAMES_JSON_PATH

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GameRepository:
    def __init__(self):
        self.games = self.load_existing_games()

    def load_existing_games(self) -> List[Game]:
        with open(GAMES_JSON_PATH) as file:
            data = json.load(file)

        games = list()

        for game in data["games"]:
            turns = [Turn(**turn) for turn in game["turns"]]
            games.append(Game(game["id"], game["first_player"], game["second_player"], turns))

        return games

    def load_by_players(self, first_player: str, second_player: str) -> Game | None:
        for game in self.games:
            if game.first_player == first_player and game.second_player == second_player:
                return game

        return None

    def create_game(self, first_player: str, second_player: str):
        return Game(id=self._get_last_game_id(), first_player=first_player, second_player=second_player, turns=None)

    def _get_last_game_id(self):
        return self.games[-1].id + 1

    def add_turn_to_game(self, first_player: str, second_player: str, turn_result: TurnResult) -> Game:
        turn = Turn(winner=turn_result.winner, timestamp=datetime.datetime.now())

        saved_games = self.games

        game_exists = False
        for game in saved_games:
            if game.first_player == first_player and game.second_player == second_player:
                game_exists = True
                game.turns.append(turn)

        if not game_exists:
            new_game = self.create_game(first_player, second_player)
            new_game.turns = [turn]

            self.games.append(new_game)

        json_games = [asdict(saved_game) for saved_game in saved_games]

        logger.info("Saving game")
        with open(GAMES_JSON_PATH, "w") as file:
            json.dump({"games": json_games}, file, default=str, indent=2)

        logger.info("Game saved")

        return self.load_by_players(first_player, second_player)
