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
        self.whiteToMove = True
        self.moveLog = []
    