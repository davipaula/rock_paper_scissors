from collections import Counter

from pydantic import validator, BaseModel


class TurnPayload(BaseModel):
    first_player_name: str
    first_player_move: str
    second_player_name: str
    second_player_move: str

    @validator("first_player_move", "second_player_move")
    def move_is_valid(cls, v):
        if v not in {"rock", "paper", "scissors"}:
            raise ValueError(
                f"Move {v} is not valid. Valid moves: rock, paper, scissors"
            )

        return v


class GameResponse(BaseModel):
    is_draw: bool
    winner: str | None
    accumulated_score: Counter
