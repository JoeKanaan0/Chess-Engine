"""
This class is responsible for storing all the information about the current state of a chess game.
It will also be responsible for determining the valid moves at the current state. It will also keep a move log
"""

class GameState():
    def __init__(self):
        # The board is an 8 by 8 2D list and each element of the list has two characters. 
        # The first character represents the color of the piece 'b' or 'w'
        # The second character represents the type of the pice 'p', 'B', 'N', 'R', 'Q', 'K'
        # "--" represents an empty space with no place.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.moveFunctions = {'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.stalemate = False
        self.checkmate = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () # Coordinates for the square where en passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        
    def makeMove(self, move):

        # Make the move regardless of what it is
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log the move so we can undo it or review the game later.
        self.whiteToMove = not self.whiteToMove # Swap Players

        # Update the king's location:
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Check to see if it's a pawn promotion move
        if move.isPawnPromotion:
            # choice = input("Promote to Queen (Q), Bishop (B), Rook (R), Knight (N)")
            # self.board[move.endRow][move.endCol] = move.pieceMoved[0] + choice.upper()
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # Check to see if it's an En-Passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" # Capturing the pawn

        # Update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # Only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
            self.enpassantPossibleLog.append(self.enpassantPossible)
        else:
            self.enpassantPossible = ()
        
        # Castling move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # Kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # Move the rook to the new square
                self.board[move.endRow][move.endCol + 1] = "--" # Remove the rook from the old square

            else: # Queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        # Update castling rights - whenever a rook or a king moves
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0: # Make sure the moveLog isn't empty
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Switch back turns
            # Update the king's position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # Undo en-passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # Leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            if len(self.enpassantPossibleLog) > 0:
                self.enpassantPossible = self.enpassantPossibleLog.pop()
                #self.enpassantPossible = self.enpassantPossibleLog[-1]

            # Undo castling rights
            self.castleRightsLog.pop() # Get rid of the new castle rights from the move we are undoing
            newRights = self.castleRightsLog[-1] # Set the current castle rights to the last one in the list
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            # Undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            self.checkmate = False
            self.stalemate = False


    """
    Updates castle rights after a given move
    """
    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0: # Left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: # Right rook
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0: # Left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: # Right rook
                    self.currentCastlingRight.bks = False

        # If a rook is captured
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                else: 
                    self.currentCastlingRight.wks = False

        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                else:
                    self.currentCastlingRight.bks = False


    """
    All moves considering the king is in check
    """
    def getValidMoves(self):
        tempCastleRight = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                    self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)

        tempEnpassantPossible = self.enpassantPossible
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1: # Only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # To block a check you must move a piece into one of the squares between the enemy piece and the king
                check = self.checks[0] # Check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # Enemy piece causing the check
                validSquares = [] # Squares that pieces can move to
                # If knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # Check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # Once you get to piece and checks
                            break

                # Get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1): # Go the the list backwards when removing items
                    if moves[i].pieceMoved[1] != 'K': # Move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: # Move doesn't block check or capture piece
                            moves.remove(moves[i])

                if len(moves) == 0:
                    self.checkmate = True

                if len(moves) == 0 and not self.inCheck:
                    self.stalemate = True
                    self.checkmate = False
                        
            else: # Double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)

                if len(moves) == 0:
                    self.checkmate = True

                if len(moves) == 0 and not self.inCheck:
                    self.stalemate = True
                    self.checkmate = False
            
        else: # Not in check so all moves are fine
            moves = self.getAllPossibleMoves()
            if len(moves) == 0:
                self.stalemate = True

            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRight
        return moves        

    """
    Determine if they enemy can attack the square r, c
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # Switch to opponent's turn
        oppMoves = self.getAllPossibleMoves() # Generate the opponent's moves
        self.whiteToMove = not self.whiteToMove # Switch the turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # Sqaure is under attack
                return True
        return False

    """
    All moves without the check
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # Number of rows
            for c in range(len(self.board[r])): # Number of columns
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves

    """
    Returns if the player is in check, a list of pins, and a list of checks
    """
    def checkForPinsAndChecks(self):
        pins = [] # Squares where the allied pinned piece is and direction pinned from
        checks = [] # Squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # Check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # Reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or check possible in this direction
                            break

                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # There are 5 possiblities here in this complex conditional

                        # 1) Orthoginally away from the king and piece is a rook
                        # 2) Diagonally away from the king and the piece is a bishop
                        # 3) 1 square diagonally away from the king and the piece is a pawn
                        # 4) Any direction and the piece is a queen
                        # 5) Any direction 1 sqaure away from the king and the piece is a king(This is
                        # to prevent a king move to a square controlled by another king)
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or \
                                    (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):

                            if possiblePin == (): # No Piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # Piece blocking so pin
                                pins.append(possiblePin)
                                break

                        else: # Enemy piece not applying check
                            break
                

        # Check for knight checks 
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for k in knightMoves:
            endRow = startRow + k[0]
            endCol = startCol + k[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                piece = self.board[endRow][endCol]  
                if (piece[0] == enemyColor and piece[1] == 'N'):
                    inCheck = True
                    checks.append((endRow, endCol, k[0], k[1]))
        return inCheck, pins, checks
            

    """
    Get all the possible moves for the pawn located at r, c
    """
    def getPawnMoves(self, r, c, moves):

        # Check to see if the pawn is pinned
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # Generate the white's two square movement
        if self.whiteToMove and r == 6:
            if self.board[r - 2][c] == "--" and self.board[r - 1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 2, c), self.board))

        # Generate the blacks's two square movement
        if not self.whiteToMove and r == 1:
            if self.board[r + 2][c] == "--" and self.board[r + 1][c] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 2, c), self.board))  

        # Get the movement and king info based on the current turn
        directions = (1, -1)
        direction = directions[self.whiteToMove]
        locations = (self.blackKingLocation, self.whiteKingLocation)
        kingRow, kingCol = locations[self.whiteToMove]
                 
        # Generate the one square movement based on the turn
        if self.board[r + 1 * direction][c] == "--": 
            if not piecePinned or pinDirection == (1 * direction, 0):
                moves.append(Move((r, c), (r + 1 * direction, c), self.board))

        # Get the enemy color
        enemyColors = ["w", "b"]
        enemyColor = enemyColors[self.whiteToMove]

        # Generate the en-passant movement based on the turn
        if c + 1 <= 7:
                if self.board[r + 1 * direction][c + 1][0] == enemyColor:
                    if not piecePinned or pinDirection == (1 * direction, 1):
                        moves.append(Move((r, c), (r + 1 * direction, c + 1), self.board))
                elif (r + 1 * direction, c + 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1 * direction, 1):
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c: # King is left of the pawn
                                # Between the king and the pawn, outside range between pawn border
                                insideRange = range(kingCol + 1, c)
                                outsideRange = range(c + 2, 8)
                            else: # King on the right of the pawn
                                insideRange = range(kingCol - 1, c + 1, -1)
                                outsideRange = range(c - 1, -1, -1)
                            for i in insideRange:
                                if self.board[r][i] != "--": # Some other piece besides the enpassant pawns blocks
                                    blockingPiece = True

                            for i in outsideRange:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                    if not blockingPiece:
                                        attackingPiece = True
                                elif square != "--":
                                    blockingPiece = True
                        if not attackingPiece or blockingPiece:
                            moves.append(Move((r, c), (r + 1 * direction, c + 1), self.board, isEnpassantMove = True))

        if c - 1 >= 0:
                if self.board[r + 1 * direction][c - 1][0] == enemyColor:
                    if not piecePinned or pinDirection == (1 * direction, -1):
                        moves.append(Move((r, c), (r + 1 * direction, c - 1), self.board))
                elif (r + 1 * direction, c - 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1 * direction, -1):
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c: # King is left of the pawn
                                # Between the king and the pawn, outside range between pawn border
                                insideRange = range(kingCol + 1, c - 1)
                                outsideRange = range(c + 1, 8)
                            else: # King on the right of the pawn
                                insideRange = range(kingCol - 1, c, -1)
                                outsideRange = range(c - 2, -1, -1)
                            for i in insideRange:
                                if self.board[r][i] != "--": # Some other piece besides the enpassant pawns blocks
                                    blockingPiece = True

                            for i in outsideRange:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                    if not blockingPiece:
                                        attackingPiece = True
                                elif square != "--":
                                    blockingPiece = True
                        if not attackingPiece or blockingPiece:
                            moves.append(Move((r, c), (r + 1 * direction, c - 1), self.board, isEnpassantMove = True))                        

    """
    Get all the possible moves for the rook located at r, c
    """
    def getRookMoves(self, r, c, moves):

        # Check to see if the piece is pinned
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # Can't remove queen from pin on rook moves
                    self.pins.remove(self.pins[i])
                break

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        color = self.board[r][c][0]

        for d in directions:
            for i in range(1, 8):
                endRow = r + i * d[0]
                endCol = c + i * d[1]
                if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                    if 0 <= endRow<= 7 and 0 <= endCol <= 7:
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        else:
                            if self.board[endRow][endCol][0] is not color:
                                moves.append(Move((r, c), (endRow, endCol), self.board))
                            break

    """
    Get all the possible moves for the king located at r, c
    """
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # Not an ally piece (empty or enemy piece)
                    # place king on end square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, _, _ = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # Place king back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
    

    """
    Get all the possible moves for the queen located at r, c
    """
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    """
    Get all the possible moves for the bishop located at r, c
    """
    def getBishopMoves(self, r, c, moves):

        # Check to see if the piece is pinned
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # Can't remove queen from pin on bishop moves
                    self.pins.remove(self.pins[i])
                break

        color = self.board[r][c][0]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d in directions:
            for i in range(1, 8):
                endRow = r + i * d[0]
                endCol = c + i * d[1]
                if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                    if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        else:
                            if self.board[endRow][endCol][0] is not color:
                                moves.append(Move((r, c), (endRow, endCol), self.board))
                            break

    """
    Get all the possible moves for the knight located at r, c
    """
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, 1), (2, -1), (-2, -1), (2, 1), (1, 2), (-1, -2), (-1, 2), (1, -2))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    
        return moves

    """
    Generate all valid castle moves for the king at (r, c) and add them to the list of moves.
    """
    def getCastleMoves(self, r, c, moves):
        if self.inCheck:
            return # Can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

            
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():

    # maps keys to values
    # key : value
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                   "5" : 3, "6" : 2, "7" : 1, "8" : 0}

    rowsToRanks = {v : k for k, v in ranksToRows.items()}

    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
                   "e" : 4, "f" : 5, "g" : 6, "h" : 7}

    colsToFiles = {v : k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # En-passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
           self.pieceCaptured = board[self.startRow][self.endCol]

        # Pawn Promotion
        self.isPawnPromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7))

        # Castle move
        self.isCastleMove = isCastleMove

        # Check if the we captured a piece
        self.isCapture = self.pieceCaptured != "--"

    """
    Overring the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.getChessNotation() == other.getChessNotation()
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[r] + self.rowsToRanks[c]

    # Overriding to the String function
    def __str__(self):
        # Castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
            # "O-O" Kingside castle
            # "O-O-O" Queenside castle
        
        endSquare = self.getRankFile(self.endRow, self.endCol)
        # Pawn moves
        if self.pieceMoved[1] == "p":
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            
            # Pawn promotion

        # Two of the same type of piece moving to a square, 

        # piece moves
        moveString = self.pieceMoved[1]
        if self.pieceMoved[1]:
            if self.isCapture:
                moveString += "x"
            return moveString + endSquare