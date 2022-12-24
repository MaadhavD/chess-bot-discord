import discord
from discord.ext import commands
import chess
import chess.pgn
import chess.svg
import chess.engine
import chess.uci
import tkinter as tk

# Replace YOUR_BOT_TOKEN with the token for your Discord bot
TOKEN = 'YOUR_BOT_TOKEN'

# Initialize the Discord client and the bot
client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Create a chess board and engine
board = chess.Board()
engine = chess.uci.popen_engine("stockfish")
engine.uci()

# Set up the GUI
class ChessWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.initUI()

    def initUI(self):
        # Set up the chess board and pieces
        self.board = tk.Label(self, image="chessboard.png")
        self.board.pack()

        self.pieces = []
        for i in range(64):
            label = tk.Label(self, image='')
            self.pieces.append(label)

        # Set up the drag and drop functionality
        for piece in self.pieces:
            piece.bind("<Button-1>", self.on_drag_start)
            piece.bind("<B1-Motion>", self.on_drag_move)
            piece.bind("<ButtonRelease-1>", self.on_drag_release)

    def update_board(self):
        # Update the positions of the pieces on the board
        for i, piece in enumerate(self.pieces):
            row, col = divmod(i, 8)
            x = col * 50
            y = row * 50
            piece.place(x=x, y=y)

            # Get the piece at the current position on the chess board
            pos = chess.square(i)
            square = board.piece_at(pos)
            if square is None:
                piece.configure(image='')
            else:
                piece.configure(image=f"{square.symbol()}.png")

    def on_drag_start(self, event):
        # Get the source square for the move
        self.source_square = event.widget
        self.source_square.lift()
        self.drag_x = event.x
        self.drag_y = event.y

    def on_drag_move(self, event):
        # Move the piece along with the mouse cursor
        self.source_square.place(x=event.x_root - self.drag_x, y=event.y_root - self.drag_y)

    def on_drag_release(self, event):
        # Get the destination square for the move
        self.dest_square = event.widget
# Set up the Discord bot commands
@bot.command()
async def newgame(ctx):
    # Start a new game
    board.reset()
    widget.update_board()

@bot.command()
async def move(ctx, source, dest):
    # Make a move on the chess board
    move = chess.Move.from_uci(f"{source}{dest}")
    if move in board.legal_moves:
        board.push(move)
        widget.update_board()
    else:
        await ctx.send("Invalid move!")

@bot.command()
async def showboard(ctx):
    # Send an image of the current chess board to Discord
    img = chess.svg.board(board=board, size=400)
    await ctx.send(file=discord.File(img))

@bot.command()
async def play(ctx):
    # Make a move using the chess engine
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    widget.update_board()
    await ctx.send(f"I made the move {result.move}")

# Run the Discord bot
client.run(TOKEN)

# Set up the tkinter GUI and run the main loop
root = tk.Tk()
widget = ChessWidget(master=root)
root.mainloop()
