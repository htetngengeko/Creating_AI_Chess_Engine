import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #dimension of a chess board is 8*8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

'''initialize a globel dictionary(like redux) to call it just once in main.'''

def loadImages():
    pieces =['bp','bR','bN','bB','bQ','bK','wp','wR','wB','wN','wR','wQ','wK']
    for piece in pieces:
      IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    #we can access images by calling IMAGES['bp']
     
'''The main driver of code.This handle user input and updating the graphics.'''

def main():
   p.init()
   screen = p.display.set_mode((WIDTH, HEIGHT))
   clock = p.time.Clock()
   screen.fill(p.Color("white"))
   game_state = ChessEngine.GameState()
   validMoves = game_state.getValidMoves()
   moveMade = False #flag variable for a move is made

   loadImages()  #only do this once before while loop
   running = True
   sqSelected = () #no sq is selected.keep track of the last click of the user (tuple:(row,col))
   playerClicks = [] #keep track of player clicks(two tuples:[(6,4), (4,4)])

   while running:
      for e in p.event.get():
         if e.type == p.QUIT:
            running = False

         #mouse handler
         elif e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos() #(x,y) location of mouse
            col = location[0] // SQ_SIZE
            row = location[1] // SQ_SIZE

            if sqSelected == (row,col):  #if user click the same sq twice
               sqSelected = () #deselect
               playerClicks = [] #clear player clicks
            
            else :
               sqSelected = (row,col)
               playerClicks.append(sqSelected) #append for both 1st and 2nd click
            
            if len(playerClicks) == 2:  #after 2nd click
               move = ChessEngine.Move(playerClicks[0], playerClicks[1], game_state.board)
               print(move.getChessNotation())
               if move in validMoves:
                  game_state.makeMove(move)
                  moveMade = True
                  sqSelected=() #reset user click
                  playerClicks=[]
               else:
                  playerClicks = [sqSelected]
         
         #key handler
         elif e.type == p.KEYDOWN:
            if e.key == p.K_z: #undo when 'z' is pressed
               game_state.undoMove()
               moveMade = True
         
      if moveMade:
         validMoves = game_state.getValidMoves()
         moveMade = False
               
      drawGameState(screen,game_state)
      clock.tick(MAX_FPS)
      p.display.flip()

'''Responsible for all the graphics within a current game state.'''

def drawGameState(screen,game_state):
   drawBoard(screen) #draw square on the board
   #add in piece highlighting or move suggestions(later)
   drawPieces(screen, game_state.board) #draw pieces on top of those squares

'''Draw the squares on the board. The top square is always light.'''
def drawBoard(screen):
   colors = [p.Color("white"), p.Color("gray")]
   for r in range(DIMENSION):
      for c in range(DIMENSION):
         color = colors[((r+c)%2)]
         p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''Draw the pieces on the board using the current GameState.board'''
def drawPieces(screen, board):
   for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__=="__main__":
    main()

   

