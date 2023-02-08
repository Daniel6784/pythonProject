from Shape import Shape
from colorama import Fore, Back, Style
import random

class TetrisBoard:

    def __init__(self, width,height):
        #initialize board
        self.board = [[0]*width for x in range(height)]
        self.width = width
        self.height = height
        self.cleared_rows = 0

        self.col_heights = [self.height]*self.width
        self.shadow_piece = []


        self.scoring_table = [ 0, 100,300,500,800]
        self.speed_table =   [1,1.2,1.4,1.6,1.8,2]
        self.score = 0
        self.level = 1
        self.cleared_levels = 0

        self.curPiece = []
        self.bag = [1,2,3,4,5,6,7]
        random.shuffle(self.bag)
        self.piece_index = 0
        self.nexPiece = Shape(self.randomPiece(),self.width,self.height)


    def randomPiece(self):
        if self.piece_index == 6:
            random.shuffle(self.bag)
            self.piece_index = 0
        self.piece_index += 1
        return self.bag[self.piece_index]

    def addRandomPiece(self):
        self.curPiece = self.nexPiece
        self.nexPiece = Shape(self.randomPiece(),self.width,self.height)
        for part in self.curPiece.pos:

            if self.board[part[0]][part[1]] <0:
                #print("Could not add Piece ")
                #print("Game Over")
                #print(self.score)
                return False
        return True

    def addPiece(self,piece):
        self.curPiece = Shape(piece,self.width,self.height)
        self.nexPiece = Shape(piece,self.width,self.height)
        self.shadow_piece = Shape(piece,self.width,self.height)
        self.cur_piece_index = 0

        for part in self.curPiece.pos:

            if self.board[part[0]][part[1]] <0:
                print("Could not add Piece ")
                print("Game Over")
                return False

        return True

    def canMoveDown(self,piece):
        for i,j in piece.pos:
            if i+1 == self.height:
                return False
            elif self.board[i+1][j] <0:
                return False
        return True

    def moveDown(self,piece):
        if not  self.canMoveDown(piece) and piece is self.curPiece:
            for i,j in self.curPiece.pos:
                 if self.col_heights[j] >= i:

                     self.col_heights[j] = i

                 self.board[i][j] = -1*piece.piece_value
            return 2
        piece.moveDown()
        return 0



    def canMoveLeft(self,piece):
        for i,j in piece.pos:
            if j-1<0:
                return False
            elif self.board[i][j-1]<0 and self.board[i][j-1] != -10:
                return False
        return True


    def moveLeft(self,piece):

        if not self.canMoveLeft(piece):
            return
        self.curPiece.moveLeft()




    def canMoveRight(self,piece):

        for i, j in piece.pos:
            if j+1 >= self.width:
                return False
            elif self.board[i][j+1] <0 and self.board[i][j+1] != -10:
                return False
        return True

    def moveRight(self,piece):

        if not self.canMoveRight(piece):
            return

        piece.moveRight()

        return 0

    def canRotateClockwise(self,piece):
        rotation_matrix = piece.rotations[piece.piece_value][piece.rotation]

        for part,move in zip(piece.pos,rotation_matrix):

            if part[0]+move[0]<0:
                return False
            elif part[0]+move[0] >=self.height:
                return False
            elif part[1]+move[1] < 0:
                return False
            elif part[1]+move[1]+1 >=self.width:
                return False
            elif self.board[part[0]+move[0]][part[1]+move[1]]<0 and self.board[part[0]+move[0]][part[1]+move[1]] != -10:
                return False

        return True

    def rotateClockwise(self,piece):
        if not self.canRotateClockwise(piece):
            #print("coudl not rotate")
            return
        piece.rotateClockwise()




        return 0

    def canRotateAntiClockwise(self):
        rotation_matrix = self.rotations[self.pieceValue][self.rotation-1]
        for part,move in zip(self.curPiece,rotation_matrix):

            if part[0]-move[0]<0:
                return False
            elif part[0]-move[0] >=self.height:
                return False
            elif part[1]-move[1] < 0:
                return False
            elif part[1]-move[1]+1 >=self.width:
                return False
            elif self.board[part[0]+move[0]][part[1]-move[1]]<0:
                return False
        return True

    def rotateAntiClockwise(self):
        if not self.canRotateClockwise():
            #print("could not rotate")
            return
        self.clearPiece()
        rotation_matrix = self.rotations[self.pieceValue][self.rotation-1]
        for part, move in zip(self.curPiece, rotation_matrix):
            self.board[part[0] + move[0]][part[1] + move[1]] = self.pieceValue
            part[0] = part[0] - move[0]
            part[1] = part[1] - move[1]
        self.rotation = (self.rotation - 1) % 4

        return 0


    def isComplete(self, row):
        complete = True
        for block in self.board[row]:
            complete = complete and (block<0)
        return complete

    def checkForCompletions(self):
        complete_rows = list(filter(self.isComplete, range(self.height)))

        return complete_rows

    def removecompletedRows(self, rows):

        self.score += self.scoring_table[len(rows)]*self.level

        self.cleared_levels += len(rows)
        if self.cleared_levels>1 and self.cleared_levels %10 == 0:
            self.level += 1

        for completed_row in rows:
            for col in range(self.width):
                self.board[completed_row][col] = 0
                self.col_heights[col] = self.col_heights[col] + 1
            for row in range(completed_row-1):
                for col in range(self.width):
                    if self.board[completed_row -row-1][col]<0:
                        self.board[completed_row - row][col] = self.board[completed_row - row-1][col]
                        self.board[completed_row -row-1][col] = 0








    def update_shadow(self):

        for spart, cpart in zip(self.shadow_piece.pos,self.curPiece.pos):
            spart[0] = cpart[0]
            spart[1] = cpart[1]

        for i in range(21):
            if not self.canMoveDown(self.shadow_piece):
                break
            for part in self.shadow_piece.pos:
                part[0] += 1



    def __repr__(self):
        output = ""
        for row in self.board:
            output += "["
            for col in row:
                if col != 0:
                    output += Fore.RED + f"{col}, "+Style.RESET_ALL
                else:
                    output += f"{col}, "
            output += "]\n"
        return output

    def __eq__(self, other):
        same = True
        for spart, opart in zip(self.pos, other.pos):
            same = same and spart[0] == opart[0] and spart[1] == opart
        return same
    def printPiece(self):
        for part in self.curPiece:
            print(part)