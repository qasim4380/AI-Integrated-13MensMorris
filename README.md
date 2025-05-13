AI-Integrated-13MensMorris
A Python-based implementation of the traditional 13 Men's Morris board game, featuring a graphical interface built with Pygame and core game logic written in Python. This project allows players to take turns placing and moving pieces on a custom board while aiming to form "mills" (three pieces in a line) and capture the opponent's pieces.

Overview:
13 Men's Morris is a strategic two-player board game that extends the classic Nine and Twelve Men's Morris variants. Players alternate turns to place and move their 13 pieces, with the goal of forming mills and reducing the opponent's pieces to fewer than three or blocking all possible moves.

This implementation includes:

Turn-based gameplay logic

Interactive Pygame GUI

Valid move detection and basic mill checking

Jumping phase when 3 pieces left.

Modular code with separate logic and GUI components

Easy to extend with AI or networked multiplayer

Features:
Two-player local gameplay

Graphical board rendering using Pygame

Mouse-click-based piece placement

Basic move validation and player switching

Simple win condition detection (can be extended)

Technologies Used:
Python 3
Pygame
NumPy (for board state representation)

Getting Started...
Prerequisites:
Make sure you have Python 3 and Pygame installed:
pip install pygame numpy

Run the Game:

python 13_morris_game_gui.py
A game window will open. Players take turns by clicking on valid positions on the board to place their pieces.

Project Structure:

13-mens-morris/
│
├── 13_morris_game_gui.py     # GUI
├── 13_morris_game_backend.py # Bsckend 
├── README.md                 # Project description

Future Improvements:
Mill detection and piece removal

Phase transitions (placement → movement → flying)

AI opponent using Minimax or Alpha-Beta Pruning

Online multiplayer support

Visual enhancements (animations, sounds)

📜 License
This project is licensed under the MIT License.

🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.
