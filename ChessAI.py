import random
from typing import Counter

knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

bishopScores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 2, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4],
]

queenScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 2, 2, 3, 2, 1],
    [1, 2, 3, 2, 2, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

rookScores = [
    [4, 3, 3, 4, 4, 3, 3, 4],
    [2, 2, 2, 3, 3, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 3, 3, 2, 2, 2],
    [4, 3, 3, 4, 4, 3, 3, 4],
]

whiteKingScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0],
]

blackKingScores = [
    [0, 0, 2, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

whitePawnScores = [
    [9, 9, 9, 9, 9, 9, 9, 9],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [1, 1, 2, 1, 2, 1, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

blackPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 1, 2, 1, 2, 1],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [6, 6, 6, 6, 6, 6, 6, 6],
    [9, 9, 9, 9, 9, 9, 9, 9],
]

piecePositionScores = {'N' : knightScores, 'Q': queenScores, 'B' : bishopScores,
                        'R': rookScores, 'bp': blackPawnScores, 'wp': whitePawnScores,
                         'wK' : whiteKingScores, 'bK' : blackKingScores}

pieceScores = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

"""
Algorithm that picks random moves.
"""
def randomAlgorithm(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

"""
An algorithm that chooses the piece with the highest points
"""
def greedyAlgorithm(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if score >= maxScore:
            maxScore = score
            bestMove = playerMove

        gs.undoMove()

    return bestMove

"""
A greedy algorithm that looks two moves ahead instead of one
"""
def lessGreedyAlgorithm(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.checkmate:
            gs.whiteToMove = not gs.whiteToMove
            return bestPlayerMove
        else:
            opponentMaxScore = -CHECKMATE
            if gs.stalemate:
                opponentMaxScore = STALEMATE
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()

            if opponentMinMaxScore > opponentMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove
        gs.undoMove()

    return bestPlayerMove



"""
Calls the recursve method findMoveMinMax the first time 
"""
def minMaxAlgorithm(gs, validMoves):
    global nextMove, DEPTH
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

"""
Recursive function that looks at moves ahead. Depth = number of moves ahead
"""
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move

            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

"""
Calls the recursve method findMoveNegaMax the first time 
"""
def negaMaxAlgorithm(gs, validMoves):
    global nextMove, DEPTH, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

"""
Same as findMoveMinMax but it negates the score
"""
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

"""
Calls the recursve method findMoveNegaMax the first time 
"""
def alphaBetaNegaMaxAlgorithm(gs, validMoves, depth):
    global nextMove, counter, DEPTH
    DEPTH = depth
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

"""
Same as findMoveNegaMax but with alpha beta pruning implemented
"""
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Move ordering - Implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, - alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: # Pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE # Black wins
        else:
            return CHECKMATE # White wins

    elif gs.stalemate:
        return STALEMATE # Draw

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # Score it possitionally
                piecePositionScore = 0
                if square[1] == 'p' or square[1] == 'K': # For pawns
                    piecePositionScore = piecePositionScores[square][row][col]
                else: # For other pieces
                    piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == "w":
                    score += pieceScores[square[1]] + piecePositionScore * 0.1
                elif square[0] == "b":
                    score -= pieceScores[square[1]] + piecePositionScore * 0.1

    return score   

"""
Score the board based on material
"""
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]

    return score