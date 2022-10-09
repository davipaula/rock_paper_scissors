# Davi's Rock, Paper, Scissors implementation

## Introduction
Hi 👋🏾! This is my implementation of a simple Rock, Paper, Scissors game for the Anaconda challenge.

This implementation is for a Back End role, so I only focused on the back end features.

## Installation
The application was developed with Python 3.10 using FastAPI.

 1. Clone this repository
 2. Create a virtual environment to install the dependencies (not mandatory, but recommended). To do this, run this command in the root folder of the application
```bash
[alice@laptop rock_paper_scissors] virtualenv venv
```

Activate the virtual environment with:

- MacOS / Linux 
```bash
[alice@laptop rock_paper_scissors] source venv/bin/activate
```

- Windows
```shell
venv\scripts\activate.bat
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
[alice@laptop rock_paper_scissors] pip install -r requirements.txt
```


## Using the application
To start the server, run the following command from the root folder of the application:
```bash
[alice@laptop rock_paper_scissors] make run
```

If you do not have `make` installed in your computer, run the following commands:
```
[alice@laptop rock_paper_scissors] cd rock_paper_scissors
[alice@laptop rock_paper_scissors] python -m uvicorn main:app
```

You can start a game by sending a `POST` request to http://127.0.0.1:8000/v1/turn

### Payload

The endpoint expects a payload with the following configuration:
```json
{
	"first_player_name": Name of first player,
	"first_player_move": Move of the first player,
	"second_player_name": Name of the second player,
	"second_player_move": Move of the second player
}
```
The moves accepted are `rock`, `paper` or `scissors`.

## Thought process during the development
- This application is missing the features to allow playing against the computer and to start a new game. Whenever a game
is found for the same pair of `first_player_name` and `second_player_name`, the results of this previous game is loaded.
- The idea was to make the implementation as simple as possible, but with possibility of extending it in the future. I 
followed the best practices whenever as possible, but due to the limited amount of time I focused on having a working 
solution in sacrifice of code performance.
- I took the decision to not use a database and to store the data into JSON files instead. The main reason was to avoid 
having to setup the DB connections, database schema and all the boilerplate code involved in the process. This decision,
however, had a high cost later in the development, because I had to implement some basic data manipulation (insert, update,
auto increment etc.) by hand.
- This implementation does not contain tests. I had issues setting up the test suite in the beginning of the project and 
couldn't make PyTest work properly. As I was losing precious time for implementation, I opted to test the application 
manually, which slowed the development process.

## Possible improvements
- Other than implementing the missing features, the future iterations of this application could allow players to connect
from different clients, like in a P2P online game. This could be implemented with the support of the package `websockets`,
which works well with FastAPI.