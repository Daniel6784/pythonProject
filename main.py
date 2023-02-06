import pygame

import TetrisBoard
from TetrisBoard import *
import time
import random
import sys

import Agent



class Runner:
    def __init__(self):
        pygame.key.set_repeat(200)
        self.game = TetrisBoard(10,22)
        self.moves = dict()

        background_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((400, 800))
        self.screen.fill(background_color)
        self.live_colors = [ 0,(255, 0 ,0), (0, 255,0), (0,0,255),(255,0,255),(255,255,0), (0,255,255),(255,255,255)]
        self.dead_colors = [ 0,(127, 0 ,0), (0, 127,0), (0,0,127),(127,0,127),(127,127,0), (0,127,127),(127,127,127)]


        self.moves[pygame.K_DOWN] = self.game.moveDown
        self.moves[1073741906] = self.game.rotateClockwise
        self.moves[pygame.K_LEFT] = self.game.moveLeft
        self.moves[pygame.K_RIGHT] = self.game.moveRight


        self.game.addPiece(2)
        self.game.update_shadow()


        pygame.display.flip()

        self.drawBoard()
        self.start_time = time.time()
        for i in range(5):
            self.game.moveDown(self.game.curPiece)
        self.counter = 0
        while True:
            self.drawBoard()



            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    print(self.game)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:


                    if event.key in self.moves.keys():

                        if self.moves[event.key](self.game.curPiece) == 2:
                            self.pieceDeath()
                        self.game.update_shadow()

            time_diff = time.time() - self.start_time
            speed = 0
            if self.game.level>= 10:
                speed = 10
            else:
                speed = self.game.level
            if time_diff> (1/self.game.speed_table[speed])*self.counter:
                self.counter += 1
                if self.game.moveDown(self.game.curPiece) == 2:
                    self.pieceDeath()
                    print(self.game.score)
                    print(self.game.level)
                    print(self.game.cleared_levels)


    def pieceDeath(self):
        self.start_time = time.time()
        self.counter = 0
        rows_to_clear = self.game.checkForCompletions();
        self.game.removecompletedRows(rows_to_clear)
        new_piece = random.randint(1, 7)
        self.game.addPiece(new_piece)
        self.game.update_shadow()


    def drawBoard(self):

        for i in range(self.game.height-2):

            for j in range(self.game.width):
                if [i+2,j] in self.game.curPiece.pos:
                    pygame.draw.rect(self.screen, self.live_colors[self.game.curPiece.piece_value], (30 * j, 30 * i, 30, 30),2,3)
                elif [i+2,j] in self.game.shadow_piece.pos:
                    pygame.draw.rect(self.screen, (255, 255, 255), (30 * j, 30 *i, 30, 30),2,3)

                elif self.game.board[i+2][j]<0 and self.game.board[i+2][j] != -10:

                    pygame.draw.rect(self.screen, self.dead_colors[-1*self.game.board[i+2][j]],(30*j,30*i,30,30))


                else:
                    pygame.draw.rect(self.screen, (50,50,50), (30*j,30*i,30,30))
                    # setting up grid for the board
        for i in range(self.game.height):
                    pygame.draw.line(self.screen, (0, 0, 0), (0, i * 30), (300, i * 30))
        for j in range(self.game.width):
                    pygame.draw.line(self.screen, (0, 0, 0), (j * 30, 0), (j * 30, 600))
        pygame.display.flip()

class Player(Runner) :

    def __init__(self,agent):

        self.agent = agent
        self.game = agent.game
        background_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((400, 800))
        self.screen.fill(background_color)
        self.live_colors = [0, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 0), (0, 255, 255),
                            (255, 255, 255)]
        self.dead_colors = [0, (127, 0, 0), (0, 127, 0), (0, 0, 127), (127, 0, 127), (127, 127, 0), (0, 127, 127),
                            (127, 127, 127)]

    def display(self):

        self.agent.game.addPiece(2)

        self.game.update_shadow()

        self.drawBoard()
        pygame.display.flip()


        choice = self.agent.chooseMove(self.game.curPiece)


        moves_to_make = choice[1][1]


        while True:
            self.drawBoard()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()
            if moves_to_make[1] > 0:
                for i in range(moves_to_make[1]):
                    self.game.rotateClockwise(self.game.curPiece)
                    self.drawBoard()
                    pygame.time.wait(50)
            if moves_to_make[0]< 0:

                for i in range(-1*moves_to_make[0]):

                    self.game.moveLeft(self.game.curPiece)
                    self.drawBoard()
                    pygame.time.wait(50)

            if moves_to_make[0]>0:
                for i in range(moves_to_make[0]):

                    self.game.moveRight(self.game.curPiece)
                    self.drawBoard()
                    pygame.time.wait(50)
            if moves_to_make[2] >0:
                for i in range(moves_to_make[2]):

                    self.game.rotateClockwise(self.game.curPiece)
                    self.drawBoard()
                    pygame.time.wait(50)
            while self.game.canMoveDown(self.game.curPiece) :
                self.game.moveDown(self.game.curPiece)
                self.drawBoard()
                pygame.time.wait(50)

            self.game.moveDown(self.game.curPiece)
            print(self.agent.calcHeights(self.game.curPiece))
            print(self.game)

            if choice[0][3] >0:
                rows_completed = self.game.checkForCompletions()
                self.game.removecompletedRows(rows_completed)

                self.drawBoard()

            if  not self.agent.game.addPiece(2):
                pygame.quit()
                sys.exit()

            self.game.update_shadow()

            self.drawBoard()
            pygame.display.flip()

            choice = self.agent.chooseMove(self.game.curPiece)


            moves_to_make = choice[1][1]



    def Play(self):
        print("Playing game")
        counter = 0
        actions = [self.game.moveDown,self.game.moveRight,self.game.moveLeft, self.game.rotateClockwise]
        while(self.game.addPiece(random.randint(1, 7))):


            choice = self.agent.chooseMove(self.game.curPiece)
            self.game.curPiece = choice[1][0]


            while(self.game.canMoveDown(self.game.curPiece)):
                self.game.moveDown(self.game.curPiece)
            self.game.moveDown(self.game.curPiece)

            if choice[0][3] >0:
                rows_completed = self.game.checkForCompletions()
                self.game.removecompletedRows(rows_completed)

            counter += 1
        print(self.game.score)




def TestAgent():
    game = TetrisBoard(10,20)
    agent = Agent.Agent(game)
    print(game)
    game.addPiece(2)
    """
    for i in range(4):
        game.moveRight(game.curPiece)
    for i in range(20):
        game.moveDown(game.curPiece)
    game.addPiece(2)
    for i in range(4):
        game.moveLeft(game.curPiece)
    for i in range(20):
        game.moveDown(game.curPiece)
    print(game)
    game.addPiece(2)
    game.rotateClockwise(game.curPiece)
    print(f" calc bumpiness in middle {agent.valOfPiece(game.curPiece)}")
    print(game)
    print(game.curPiece.pos)
    """
    #agent.valOfPiece(game.curPiece)
    start_time = time.time()
    for i in range(1):
        print("generating move set")
        agent.gen_move_set(game.curPiece)
    print(f" 100 rounds of this took {time.time()- start_time} seconds")







def main(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    pygame.init()
    game = TetrisBoard(10,22)
    agent = Agent.Agent(game,[0,-1,0,0])
    player = Player(agent)
    print(player.Play())
    #Runner()
    #TestAgent()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

