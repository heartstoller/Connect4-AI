# Connect 4 AI

This project is a Python-based implementation of the classic Connect 4 game, enhanced with AI opponents of varying difficulty levels. Built using **Pygame** for a graphical user interface and **NumPy** for game logic, this game offers a visually appealing and engaging gameplay experience.

---

## Features

- **Dynamic Visual Game Board**: Interactive GUI built with Pygame.
- **Difficulty Levels**:
  - Easy: Random moves.
  - Medium: Monte Carlo simulations.
  - Hard: Minimax algorithm with Alpha-Beta Pruning.
- **Win/Loss Detection**: Automatically identifies game outcomes.
- **Retry Option**: Players can restart the game after it ends.
- **User-Friendly Interface**: Difficulty selection and seamless gameplay.

---

## How It Works

1. **Game Initialization**: The board is represented as a 6x7 grid using NumPy.
2. **Gameplay Mechanics**:
   - Players take turns dropping pieces into columns.
   - AI moves are calculated based on the selected difficulty level.
   - The board updates in real time to reflect player and AI actions.
3. **Win Detection**:
   - Four consecutive pieces in any direction (horizontal, vertical, or diagonal) result in a win.
   - If the board fills up without a winner, the game ends in a draw.
4. **Game End**:
   - The winner is announced.
   - Players are prompted to restart or exit the game.

---

## AI Search Strategies

### Monte Carlo Simulation (Medium Difficulty)
The AI simulates a large number of random plays from the current board state to the game's end. Each potential move is scored based on its likelihood of leading to a win. This method balances computational efficiency with reasonable strategic strength.

### Minimax with Alpha-Beta Pruning (Hard Difficulty)
The Minimax algorithm evaluates all possible moves and outcomes up to a certain depth to make optimal decisions. Alpha-Beta pruning skips unnecessary branches in the decision tree, allowing deeper searches and highly strategic gameplay.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/heartstoller/connect4-ai.git
   cd connect4-ai
   ```

2. **Install Dependencies**:
   ```bash
   pip install pygame numpy
   ```

3. **Run the Game**:
   ```bash
   python connect4.py
   ```

---

## Team Members

- Aman Backer 
- Aswin Shobanan 
- Ananthakrishnan S 
- Mallik Siva Sujith 

---

## License

This project is licensed under the MIT License. Feel free to use and modify the code as per your needs.

---

## Acknowledgments

- **Libraries Used**:
  - [Pygame](https://www.pygame.org/): For graphical user interface.
  - [NumPy](https://numpy.org/): For game board logic.

Thank you for exploring this project! We hope you enjoy playing our Connect 4 AI game.
