class GameState():
    def __init__(self) :
        #board id a 8*8 2d list, each element of the list has 2 characters.
        #First character represents the color of piece, 'b' or 'w'.
        #Second character represents the type of piece. 'K', 'Q','B','N','R','P'.
        #"--" represents the empty space on board with no piece.
        self.board =[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"], 
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]   
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
    
    '''Take a Move as a parameter and execuutes it(this will not work for castling, pawn promotion and en-passent)''' 
    def makeMove(self, move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap player
    
    '''Undo the last move made.'''
    def undoMove(self):
        if(self.moveLog)!= 0:  #make sure there is a move to undo
            move= self.moveLog.pop() #return the last element and remove it
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swap player
    
    '''All moves considering check'''
    def getValidMoves(self):    
        return self.getAllPossibleMoves()  #for now not consider for checks.

    '''All moves without considering check'''
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):  #number of rows
            for column in range (len(self.board[row])):  #number of columns in a row
                turn = self.board[row][column][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    self.moveFunctions[piece](row, column, moves) #calls the appropriate move function based on piece type
    
        return moves
                    
    
    '''Get all the pawn moves for the pawn located at row, col and add this moves to the list(move[])'''
    def getPawnMoves(self, row, column, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[row-1][column] == "--": #1 sq moves
                moves.append(Move((row, column),(row-1, column), self.board))
                if row == 6 and self.board[row-2][column] == "--": #2 sqs move
                    moves.append(Move((row, column), (row-2,column), self.board))
            if column-1 >= 0: #for left side
                if self.board[row-1][column-1][0] == 'b':  #black piece to capture
                    moves.append(Move((row, column),(row-1, column-1), self.board))
            if column+1 <= 7: #for right side
                if self.board[row-1][column+1][0] == 'b': #black piece to capture
                    moves.append(Move((row, column),(row-1, column+1), self.board))
        
        else:
            if self.board[row+1][column] == "--": #1 sq moves
                moves.append(Move((row, column), (row+1, column), self.board))
                if row == 1 and self.board[row+2][column] == "--": #2 sqs move
                    moves.append(Move((row, column), (row+2, column), self.board))
            if column-1 >= 0: #for left side
                if self.board[row+1][column-1][0] == 'w': #white piece to capture
                    moves.append(Move((row, column),(row+1, column-1), self.board))
            if column+1 <= 7: #for right side
                if self.board[row+1][column+1][0] == 'w': #white piece to capture
                    moves.append(Move((row, column),(row+1, column+1), self.board))

        #add pawn promotion later
                

    '''Get all the rook moves for the pawn located at row, col and add this moves to the list(move[])'''
    def getRookMoves(self, row, column, moves):
       directions =((-1, 0), (0, -1), (1, 0), (0, 1)) #up left down right
       enemyColor = "b" if self.whiteToMove else "w"
       for d in directions:
           for i in range(1, 8):  #rook can move max of 7 sqs
               endRow = row + d[0] * i
               endCol = column + d[1] * i
               if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                   endPiece = self.board[endRow][endCol]
                   if endPiece == "--":
                       moves.append(Move((row, column),(endRow, endCol), self.board))
                   elif endPiece[0] == enemyColor: #enemy piece valid
                       moves.append(Move((row, column),(endRow, endCol), self.board))
                       break
                   else:  #friendly piece
                       break
               else:  #off board 
                   break
               
    '''Get all the knight moves for the pawn located at row, col and add this moves to the list(move[])'''
    def getKnightMoves(self, row, column, moves):
        knightMoves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2), (1, -2), (-1, -2))
        allyColor = "w" if self.whiteToMove else "b"
        for k in knightMoves:
            endRow = row + k[0]
            endCol = column + k[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  #neither enemy nor "--"
                    moves.append(Move((row, column), (endRow, endCol), self.board))
                

    '''Get all the bitshop moves for the pawn located at row, col and add this moves to the list(move[])'''
    def getBishopMoves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1,8): #bishop can move max of 7 sqs
                endRow = row + d[0] * i
                endCol = column + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:  #friendly piece
                        break
                else:  #off board
                    break                

    '''Get all the queen moves for the pawn located at row, col and add this moves to the list(move[])'''
    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    '''Get all the king moves for the pawn located at row, col and add this moves to the list(move[])'''
    def getKingMoves(self, row, column, moves):
        kingMoves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = column + kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  #neither enemy nor "--" 
                    moves.append(Move((row, column), (endRow, endCol), self.board))   

class Move():

    #maps key to value
    #key:value
    ranksToRows ={"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRank = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] 
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol

    '''Overriding the equals method'''
    def __eq__(self, other) :
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    
    def getChessNotation(self):
        #you can add this like real chess notation
        return self.getRankFile(self.startRow, self.startCol)+self.getRankFile(self.endRow, self.endCol)

    
    def getRankFile(self, row, col):
        return self.colsToFiles[col]+self.rowsToRank[row] #b6,a7