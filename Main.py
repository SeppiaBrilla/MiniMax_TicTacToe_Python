from graphics import *


def main():
    win = GraphWin("Tris", 300, 300) #boring intial usefull stuff 
    Field = []
    NumericField = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    player1 = Player()
    player2 = Player()
    turn = 1
    for y in range(3): #creating the game field 
        for x in range(3):
            Field.append(Rectangle(Point(x * 100, y * 100), Point(x * 100 + 100, y * 100 + 100)))

    for i in Field: #drawing it
        i.draw(win)

    while 1: #the actual game 
        if turn == 1:
            Mouse = win.getMouse() #waiting for player moovement
            rectangle = GetRectangle(Mouse.x, Mouse.y, Field)
            if NumericField[GetIndex(rectangle.getCenter().getX())][GetIndex(rectangle.getCenter().getY())] == 0: #check if the selected spot is free
                player1.AddMove(Xmove(rectangle.getP1(), rectangle.getP2(), AddPoint(rectangle.getP1(), Point(0, +100)), #adding the move to the player move 
                                      AddPoint(rectangle.getP2(), Point(0, -100))))
                NumericField[GetIndex(rectangle.getCenter().getX())][GetIndex(rectangle.getCenter().getY())] = turn #adding the move to the numeric field, it is just like the field but not used for graphic reasons
                player1.Moves[len(player1.Moves) - 1].Draw(win)
                turn = 2
        else:
                Move(NumericField,player2,Field)
                player2.Moves[len(player2.Moves) - 1].Draw(win)
                turn = 1
                
        print(NumericField)
        winner = ceckWin(NumericField)
        if not winner == 0: #if someone has won everything nned to be resetted 
            print("Player " + str(winner) + " win!")  
            for m in player1.Moves:
                m.Undraw()
            for m in player2.Moves:
                m.Undraw()
            player1.Moves.clear()
            player2.Moves.clear()
            NumericField = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        if IsFull(NumericField): #same if the field is full and it is a tie
            print("Tie!")
            for m in player1.Moves:
                m.Undraw()
            for m in player2.Moves:
                m.Undraw()
            player1.Moves.clear()
            player2.Moves.clear()
            NumericField = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

#stuff not usefull for the algorithm
def GetRectangle(mousex, mousey, RectangleList):
    for i in RectangleList:
        if i.getP1().x <= mousex <= i.getP2().x and i.getP1().y <= mousey <= i.getP2().y:
            return i


def GetIndex(OI):
    if OI == 50:
        return 0
    if OI == 150:
        return 1
    if OI == 250:
        return 2


def AddPoint(point1, point2):
    returnValue = Point(0, 0)
    returnValue.x = point1.x + point2.x
    returnValue.y = point1.y + point2.y

    return returnValue

	
def IsFull(NumericField):
	for i in range(3):
		for j in range(3):
			if NumericField[i][j] == 0:
				return False
	
	return True

def ceckWin(NumericField):
    if NumericField[0][0] == NumericField[0][1] == NumericField[0][2]:
        return NumericField[0][0]
    if NumericField[0][0] == NumericField[1][0] == NumericField[2][0]:
        return NumericField[0][0]
    if NumericField[0][0] == NumericField[1][1] == NumericField[2][2]:
        return NumericField[0][0]
    if NumericField[2][0] == NumericField[2][1] == NumericField[2][2]:
        return NumericField[2][0]
    if NumericField[0][2] == NumericField[1][2] == NumericField[2][2]:
        return NumericField[0][2]
    if NumericField[0][2] == NumericField[1][1] == NumericField[2][0]:
        return NumericField[0][2]
    if NumericField[0][1] == NumericField[1][1] == NumericField[2][1]:
        return NumericField[0][1]
    if NumericField[1][0] == NumericField[1][1] == NumericField[1][2]:
        return NumericField[1][0]
    return 0



#the MINIMAX algorithm 
def Move(board, iaMoves, fied):
    BestScore = -100000
    move = [-1,-1]

    for i in range(3): #tryng all the possibilities 
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = MiniMax(board, 0, False)
                board[i][j] = 0
                if score > BestScore: #choosing the best one 
                    BestScore = score
                    move[0] = i
                    move[1] = j
        
    
    if not move[0] == move[1] == -1: #if there's a good one adding it to the O moves
        board[move[0]][move[1]] = 2
        iaMoves.AddMove(Omove(GetRectangle(move[0] * 100 + 50, move[1] * 100 + 50, fied).getCenter(),50))
    else:
        print("errore")




def MiniMax(board, depth, IsMaximazing):
    res = ceckWin(board) #is the game ended?
    if res == 2: 
        return 100
    
    if res == 1:
        return -100
    
    if IsFull(board):
        return 0

    if IsMaximazing: #are we maximizing our possibilities or minimizin?
        bestscore = -100000
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = MiniMax(board, depth + 1, False)
                    board[i][j] = 0
                    bestscore = max(bestscore, score) #take the move that, with recursive call give us the best chances 
        
        return bestscore 
    else: 
        bestscore = 100000
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = MiniMax(board, depth + 1, True)
                    board[i][j] = 0
                    bestscore = min(bestscore, score) #take the move that, with recursive call give us the worst chances 
        return bestscore


class Xmove:
    def __init__(self, P1, P2, P3, P4):
        self.firstLine = Line(P1, P2)
        self.secondLine = Line(P3, P4)

    def Draw(self, win):
        self.firstLine.draw(win)
        self.secondLine.draw(win)

    def Undraw(self):
        self.firstLine.undraw()
        self.secondLine.undraw()


class Omove:
    def __init__(self, center, rad):
        self.circle = Circle(center, rad)

    def Draw(self, win):
        self.circle.draw(win)

    def Undraw(self):
        self.circle.undraw()


class Player:
    def __init__(self):
        self.Moves = []

    def AddMove(self, X):
        self.Moves.append(X)


if __name__=="__main__":
    main()
