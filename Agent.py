from Shape import Shape
import time
class Agent:

    def __init__(self,game):
        self.game = game
        #coef valus 1:holes 2:bumpiness 3:avg height 4:comp wrows
        self.coef = [0 ,0,-.51,1]

    def evalMove(self,move):
        sum = move[0][0]*self.coef[0]
        sum+= move[0][1]*self.coef[1]
        sum += move[0][2]*self.coef[2]
        return sum
    def chooseMove(self,piece):
        pos_moves = self.gen_move_set(piece)

        ranking = sorted(pos_moves,key= self.evalMove, reverse=True)

        return ranking[0]


    def valOfPiece(self,piece):
        #calculates bumpiness, new holes, change in heights, rows cleared

        new_piece = Shape(piece.piece_value,self.game.width,self.game.height)
        for part in range(len(piece.pos)):
            new_piece.pos[part][0] = piece.pos[part][0]
            new_piece.pos[part][1] = piece.pos[part][1]
        for i in range(21):
            if not self.game.canMoveDown(new_piece):

                break
            new_piece.moveDown()
        bumpiness = self.calcBumpiness(new_piece)
        avg_hieght = self.calcHeights(new_piece)
        comp_rows = self.calcCompletedRows(new_piece)
        holes = self.calcNewHoles(new_piece)

        return holes, bumpiness, avg_hieght, comp_rows
        #find lowest cell parts of a piece


    def calcTop(self,piece):
        highest = dict()
        for part in piece:
            if not part[1] in highest.keys():
                highest[part[1]] = part[0]
            elif highest[part[1]] > part[0]:
                highest[part[1]] = part[0]
        return highest

    def calcBottom(self,piece):
        lowest = dict()
        # calculates the bottom of a peice
        for part in piece:
            if not part[1] in lowest.keys():
                lowest[part[1]] = part[0]
            elif lowest[part[1]] < part[0]:
                lowest[part[1]] = part[0]
        return lowest

    def calcColHeight(self,col):

        for row in range(self.game.height):
            if self.game.board[row][col] <0 and self.game.board[row][col] != -10:
                return row
        return self.game.height

    def calcHeights(self,piece):
        #calculates the top of a piece
        highest = self.calcTop(piece.pos)

        height_changes = 0
        for col in highest:
            height_changes += (self.game.height - highest[col])

        return  height_changes

    def calcBumpiness(self,piece):
        #may need to compare to old bumpiness
        bumpiness = []
        highest = self.calcTop(piece.pos)
        cols = sorted(list(highest.keys()))
        print(piece)
        print(highest)

        for i in range(self.game.width-1):

            if i in highest.keys() and i+1 in highest.keys():
                added_height = abs(highest[i] -highest[i+1])
                bumpiness.append(added_height)
            elif i  in highest.keys() and i+1 not in highest.keys():
                added_height = abs(highest[i] - self.game.col_heights[i+1])
                bumpiness.append(added_height)

            elif i not in highest.keys() and i+1 in highest.keys():
                added_height = abs(highest[i+1] - self.game.col_heights[i])
                bumpiness.append(added_height)
            else:
                added_height = abs(self.game.col_heights[i]-self.game.col_heights[i+1])
                bumpiness.append(added_height)
        print(bumpiness)
        return sum(bumpiness)


    def calcNewHoles(self,piece):
        holes = 0

        lowest = self.calcBottom(piece.pos)
        for col, row in lowest.items():

            if row == self.game.height -1:
                continue
            elif self.game.board[row+1][col] == 0:
                holes += 1
        return holes
    def calcCompletedRows(self,piece):
        rows_to_check = set([part[0] for part in piece.pos])

        completed_rows = 0
        for row in rows_to_check:

            add = True
            for col in range(self.game.width):

                if [row,col] not in piece.pos and self.game.board[row][col] >= 0:

                    add = False
            if add:
                completed_rows += 1
        return completed_rows

    def gen_move_set(self,piece):
        start_time = time.time()
        actual_moves = ""
        pos_moves = []
        proxy_piece = pos_move = Shape(piece.piece_value,self.game.width,self.game.height)
        path = [0, 0, 0]
        for part in range(len(piece.pos)):
            proxy_piece.pos[part][0] = piece.pos[part][0]
            proxy_piece.pos[part][1] = piece.pos[part][1]

        while(self.game.canMoveLeft(proxy_piece)):
            path[0] = path[0] - 1
            proxy_piece.moveLeft()


        while(self.game.canMoveRight(proxy_piece)):
            pos_move = Shape(piece.piece_value, self.game.width, self.game.height)
            for part in range(len(piece.pos)):
                pos_move.pos[part][0] = proxy_piece.pos[part][0]
                pos_move.pos[part][1] = proxy_piece.pos[part][1]

            pos_moves.append([pos_move,[path[0],path[1],path[2]]])
            path[0] = path[0] + 1
            proxy_piece.moveRight()
        pos_moves.append([proxy_piece,[path[0],path[1],path[2]]])

        rotations = []
        for move in pos_moves:
            path = move[1]
            for i in range(3):


                if not self.game.canRotateClockwise(move[0]):

                    break
                rot_move = Shape(piece.piece_value, self.game.width, self.game.height)
                for part in range(len(move[0].pos)):
                    rot_move.pos[part][0] =  move[0].pos[part][0]
                    rot_move.pos[part][1] = move[0].pos[part][1]

                rotations.append([rot_move,[path[0],path[1],path[2]]])
                path[1] += 1

                move[0].rotateClockwise()


        pos_moves = pos_moves + rotations
        evals = []

        for move in pos_moves:
            evals.append([self.valOfPiece(move[0]),move])

        return evals






