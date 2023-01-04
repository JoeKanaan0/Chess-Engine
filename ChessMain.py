"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object. 
"""

import pygame as p
from ChessEngine import GameState, Move
from ChessAI import randomAlgorithm, alphaBetaNegaMaxAlgorithm
import button

p.init()
BOARD_WIDTH = BOARD_HEIGHT = 512 # 400 is another good option.
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 # The dimension for the chess board is 8 by 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION # Get the size of the individual square
MAX_FPS = 15 # For animations
IMAGES = {}
PLAYER_ONE = True # If a Human is playing white, than this will be True. If an Ai then False
PLAYER_TWO = True # Same as above but for black
AI = alphaBetaNegaMaxAlgorithm # If an Ai is playing
DEPTH = 1 # How many moves ahead the AI is looking


"""
Check if the user wants to play against a human or an AI
"""
def getHumanOrAI(screen):
    global PLAYER_TWO

    #load button images
    human_img = p.image.load('images/human-button.png').convert_alpha()
    ai_img = p.image.load('images/AI-button.png').convert_alpha()

    #create button instances
    human_button = button.Button(150, 200, human_img, 0.16)
    ai_button = button.Button(450, 200, ai_img, 0.24)

    # Render text above the buttons
    font = p.font.SysFont('inkfree',30,italic=True,bold=True)

    text = font.render('Play Against:',True,(0, 0, 0))
    textrect = text.get_rect()
    textrect.center = ((BOARD_WIDTH//2 + 30*4, 50))

    #game loop
    while True:

        screen.fill((255, 255, 255))
        screen.blit(text, textrect)

        if human_button.draw(screen):
            PLAYER_TWO = True
            return False
        if ai_button.draw(screen):
            PLAYER_TWO = False
            return getDifficulty(screen)

        #event handler
        for event in p.event.get():
            #quit game
            if event.type == p.QUIT:
                return True

        p.display.update()


"""

"""
def getDifficulty(screen):
    global DEPTH

    #load button images
    one_img = p.image.load('images/one.jpg').convert_alpha()
    two_img = p.image.load('images/two.jpg').convert_alpha()
    three_img = p.image.load('images/three.jpg').convert_alpha()
    four_img = p.image.load('images/four.jpg').convert_alpha()

    #create button instances
    one_button = button.Button(190, 200, one_img, 0.4)
    two_button = button.Button(290, 200, two_img, 0.4)
    three_button = button.Button(390, 200, three_img, 0.4)
    four_button = button.Button(490, 200, four_img, 0.4)

    # Render text above the buttons
    font = p.font.SysFont('inkfree',30,italic=True,bold=True)
    text = font.render('Choose Difficulty:',True,(0, 0, 0))
    textrect = text.get_rect()
    textrect.center = ((BOARD_WIDTH//2 + 30*4, 50))

    #game loop
    while True:

        screen.fill((246, 246, 248))
        screen.blit(text, textrect)

        if one_button.draw(screen):
            DEPTH = 1
            return False
        if two_button.draw(screen):
            DEPTH = 2
            return False
        if three_button.draw(screen):
            DEPTH = 3
            return False
        if four_button.draw(screen):
            DEPTH = 4
            return False

        #event handler
        for event in p.event.get():
            #quit game
            if event.type == p.QUIT:
                return True

        p.display.update()




"""
Initialize a global dictionary of images. This will be called exactly once in the main.
"""
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    # Note we can access an image using the disctionary by saying "IMAGES['wp']"

"""
The main driver for our code. This will handle user input and updating the graphics
"""
def main():
    closed = False # Checks if the user closed the window
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    closed = getHumanOrAI(screen)
    gs = GameState()
    moveLogFont = p.font.SysFont("Helvitca", 16, False, False)
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made
    animate = False # Flag variable for when we should animate
    showMove = False # Flag variable for when we should show the square that was moved
    loadImages() # only do this once, before the while loop
    running = True
    sqSelected = () # No sqaure is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # Keeps track of player clicks (two tuples [(6, 4), (4, 4)])
    gameOver = False
    AIthinking = False
    moveFinderProcess = None
    while (running and closed == False):
        humanTurn = (gs.whiteToMove and PLAYER_ONE) or (not gs.whiteToMove and PLAYER_TWO)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() # Gets the (x,y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: # The user clicked the same square twice or clicked the mouseLog
                        sqSelected = () # Deselect
                        playerClicks = [] # Clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # Append for both the first and the second click
                    if len(playerClicks) == 2 and humanTurn: # After the second click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print(move.getChessNotation())
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                showMove = True
                                animate = True
                                sqSelected = () # Reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Undo when 'Z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                if e.key == p.K_SPACE: # Reset the board when r is pressed                    
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI move finder
        if not gameOver and not humanTurn:
            if not gs.whiteToMove:
                AImove = AI(gs, validMoves, DEPTH)
                if AImove is None:
                    AImove = randomAlgorithm(validMoves)
                gs.makeMove(AImove)
                moveMade = True
                animate = True

            elif gs.whiteToMove:
                AImove = AI(gs, validMoves, DEPTH)
                if AImove is None:
                    AImove = randomAlgorithm(validMoves)
                gs.makeMove(AImove)
                moveMade = True
                animate = True


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        if gs.checkmate or gs.stalemate:
            gameOver = True
            text = "Draw by stalemate" if gs.stalemate else "Black wins by checkmate" if gs.whiteToMove else "White wins by checkmate"
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont, showMove)

"""
Responsible for all the graphics within a current GameState
"""
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont, showMove):
    drawBoard(screen) # Draw the squares on the board
    if showMove:
        showMoves(gs.moveLog[-1], screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # Draw pieces on top of these squares
    drawMoveLog(screen, gs, moveLogFont)

"""
Draw the squares on the board.
"""
def drawBoard(screen):
    global colors
    colors = [p.Color((238,238,210)), p.Color((118,150,86))] # White and Green
    for i in range(DIMENSION): # Loop through the rows
        for j in range(DIMENSION): # Loop through the columns
            color = colors[(i + j) % 2 == 0]
            p.draw.rect(screen, color, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Highlight square selected and moved for piece selected
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # Make sure that sqSelected is a piece that can be moved
            # Highlight the selected square
            s = p.Surface((SQ_SIZE - 4, SQ_SIZE - 4))
            s.set_alpha(100) # Transparancy value -> 0 transparent, 255 epaque
            s.fill(p.Color(0, 0, 255))
            p.draw.rect(screen, "white", p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            screen.blit(s, (c*SQ_SIZE + 2, r*SQ_SIZE + 2))
            
            # Highlight moves form that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol *SQ_SIZE + 2, move.endRow * SQ_SIZE + 2))


"""
Draws the pieces on the board using the current GameState
"""
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Draws the moveLog 
"""
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)

    movesPerRow = 3
    padding = 5
    textY = padding
    textX = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j] + "   "
        textObject = font.render(text, True, p.Color("White"))
        textLocation = moveLogRect.move(textX, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + 3


"""
Animating a move
"""
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 5 # Frames to move one square
    frameCount = framePerSquare * 3 
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2 == 0]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)

        p.draw.rect(screen, color, endSquare)
        # Draw captured piece onto rectangle
        if move.pieceCaptured != "--" and frame < 4/6 * frameCount:
            #if move
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        # Draw moving piece
        if move.pieceMoved != "--":
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.display.flip()
            clock.tick(60)

"""
Showing the starting square of the last moved piece
"""
def showMoves(move, screen):
        c, r = move.startCol, move.startRow
        s = p.Surface((SQ_SIZE - 4, SQ_SIZE - 4))
        s.set_alpha(100) # Transparancy value -> 0 transparent, 255 epaque
        s.fill(p.Color(0, 0, 255))
        p.draw.rect(screen, "yellow", p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(s, (c *SQ_SIZE + 2, r * SQ_SIZE + 2))


"""
Draws a text when the game is over
"""
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Gray"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()
