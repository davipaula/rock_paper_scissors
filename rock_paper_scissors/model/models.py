import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class TurnResult:
    is_draw: bool
    winner: str | None


@dataclass
class Score:
    first_player_wins: int
    second_player_wins: int
    draws: int


@dataclass
class Turn:
    winner: str
    timestamp: datetime.datetime


@dataclass
class Game:
    id: int
    first_player: str
    second_player: str
    turns: List[Turn] | None = None
