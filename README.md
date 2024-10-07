# Project Overview
This project implements an advanced AI agent for the game of Tic-Tac-Toe. The agent uses game-playing algorithms to make optimal moves in a variant of Tic-Tac-Toe. This project is part of Homework 3 for the CS3411 course at UNSW.

The goal of the agent is to play against a human or another agent and make strategic decisions that maximize its chances of winning while minimizing the opponent's.

# How to Use
## Requirements
- A C compiler (like gcc) is required to compile the code.
- Make sure to have an environment where you can run C programs.
## Compilation
To compile the project, run the following command:

``` bash
gcc -o tictactoe_agent tictactoe_agent.c
```
### Running the Program
Once compiled, you can run the program using:

``` bash
./tictactoe_agent
``` 
The program will then start a Tic-Tac-Toe game, where you can choose to play against the AI agent or simulate a game between two agents.

Input
During the game, you will be prompted to enter moves in the form of grid coordinates. The AI will respond with its own moves based on the current board state.

## Features
- Minimax Algorithm: The AI uses the Minimax algorithm to evaluate possible moves and determine the best one.
- Alpha-Beta Pruning: Optimization of the Minimax algorithm by pruning branches of the search tree that do not need to be explored.
- Game State Evaluation: The agent can intelligently evaluate the board to decide whether to play defensively or offensively.
- Human vs AI or AI vs AI: Play against the AI or watch two AI agents play against each other.
## Example
Here’s how a typical game might look in the terminal:

```sql
Copy code
Welcome to Advanced Tic-Tac-Toe!
Choose your mode: (1) Human vs AI, (2) AI vs AI
1
Enter your move (row and column): 1 1
AI played at 2 2
Your move: ...
```

## Strategy
The AI agent evaluates every possible move by simulating all potential future game states and selecting the move that maximizes its chances of winning. It is highly strategic and difficult to beat, especially in the late game when few moves remain.
