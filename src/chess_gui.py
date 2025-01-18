import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon
import chess

class ChessGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess GUI with python-chess")
        self.setGeometry(100, 100, 600, 600)

        # Chessboard logic from python-chess
        self.board = chess.Board()

        # Set up the GUI layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)  
        self.central_widget.setLayout(self.grid_layout)


        # Track selected square for moving pieces
        self.selected_square = None

        # Create board buttons
        self.squares = {}
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                
                button = QPushButton()
                button.setFixedSize(80,80)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.clicked.connect(lambda _, sq=square: self.handle_click(sq))
                
                self.grid_layout.addWidget(button, row, col)
                self.squares[square] = button

                if (row + col) % 2 == 0:
                    button.setStyleSheet("background-color: #EEEED2;")  # Light square color
                else:
                    button.setStyleSheet("background-color: #769656;")  # Dark square color
        
        self.update_board()

    def update_board(self):
        """Updates the GUI to reflect the current state of the board."""
        for square, button in self.squares.items():
            piece = self.board.piece_at(square)
            if piece:
                color = "w" if piece.color == chess.WHITE else "b"
                piece_name = piece.piece_type
                piece_map = {
                    chess.PAWN: "p",
                    chess.ROOK: "r",
                    chess.KNIGHT: "n",
                    chess.BISHOP: "b",
                    chess.QUEEN: "q",
                    chess.KING: "k"
                }
                piece_image = os.path.join(r'src\assets', 'pieces', f'{color + piece_map[piece_name]}.png')
                icon = QIcon(piece_image)
                button.setIcon(icon)
                button.setIconSize(button.size())
            else:
                button.setIcon(QIcon())  # Clear the button if no piece is on the square

    def handle_click(self, square):
        """Handles user clicking on a square."""
        if self.selected_square is None:
            self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
            self.selected_square = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessGUI()
    window.show()
    sys.exit(app.exec())
