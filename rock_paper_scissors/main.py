from fastapi import FastAPI

from model.payload import TurnPayload
from service import result_calculator

app = FastAPI()

@app.post("/v1/turn")
def play_turn(turn: TurnPayload):
    return result_calculator.process_request(turn)
