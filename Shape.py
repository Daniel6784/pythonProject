class Shape:



    def __init__(self,piece_value,width,height):

        self.rotation = 0

        O_piece = [[2, width // 2 - 1], [3, width // 2 - 1], [2, width // 2], [3, width // 2]]
        I_piece = [[2, width // 2 - 2], [2, width // 2 - 1], [2, width // 2], [2, width // 2 + 1]]

        J_piece = [[2, width // 2 - 2], [2, width // 2 - 1], [2, width // 2], [3, width // 2]]
        L_piece = [[3, width // 2 - 2], [2, width // 2 - 2], [2, width // 2 - 1], [2, width // 2], ]

        S_piece = [[3, width // 2 - 2], [3, width // 2 - 1], [2, width // 2 - 1], [2, width // 2]]
        Z_piece = [[2, width // 2 - 2], [2, width // 2 - 1], [3, width // 2 - 1], [3, width // 2]]

        T_piece = [[3, width // 2 - 2], [3, width // 2 - 1], [2, width // 2 - 1], [3, width // 2]]

        O_rotations = [[[0, 0] for i in range(4)] for j in range(4)]
        I_rotations = [[[-1, 2], [0, 1], [1, 0], [2, -1]]
            , [[2, 1], [1, 0], [0, -1], [-1, -2]]
            , [[1, -2], [0, -1], [-1, 0], [-2, 1]]
            , [[-2, -1], [-1, 0], [0, 1], [1, 2]]]

        J_rotations = [[[-1, 1], [0, 0], [1, -1], [0, -2]],
                       [[1, 1], [0, 0], [-1, -1], [-2, 0]],
                       [[1, -1], [0, 0], [-1, 1], [0, 2]],
                       [[-1, -1], [0, 0], [1, 1], [2, 0]]]
        L_rotations = [[[-2, 0], [-1, 1], [0, 0], [1, -1]],
                       [[0, 2], [1, 1], [0, 0], [-1, -1]],
                       [[2, 0], [1, -1], [0, 0], [-1, 1]],
                       [[0, -2], [-1, -1], [0, 0], [1, 1]]]
        S_rotations = [[[-1, 1], [0, 0], [1, 1], [2, 0]],
                       [[1, 1], [0, 0], [1, -1], [0, -2]],
                       [[1, -1], [0, 0], [-1, -1], [-2, 0]],
                       [[-1, -1], [0, 0], [-1, 1], [0, 2]]]

        Z_rotations = [[[0, 2], [1, 1], [0, 0], [1, -1]],
                       [[2, 0], [1, -1], [0, 0], [-1, -1]],
                       [[0, -2], [-1, -1], [0, 0], [-1, 1]],
                       [[-2, 0], [-1, 1], [0, 0], [1, 1]]]
        T_rotations = [[[-1, 1], [0, 0], [1, 1], [1, -1]],
                       [[1, 1], [0, 0], [1, -1], [-1, -1]],
                       [[1, -1], [0, 0], [-1, -1], [-1, 1]],
                       [[-1, -1], [0, 0], [-1, 1], [1, 1]]]
        self.pieces = [0, O_piece, I_piece, J_piece, L_piece, S_piece, Z_piece, T_piece]
        self.rotations = [0, O_rotations, I_rotations, J_rotations, L_rotations, S_rotations, Z_rotations, T_rotations]


        self.piece_value = piece_value

        self.pos = []
        for part in self.pieces[piece_value]:

            self.pos.append([part[0],part[1]])

    def moveDown(self):

        for part in self.pos:
            part[0] = part[0]+1
    def moveLeft(self):

        for part in self.pos:
            part[1] = part[1] -1

        return 0
    def moveRight(self):
        for part in self.pos:
            part[1] = part[1] + 1

    def rotateClockwise(self):
        rotation_matrix = self.rotations[self.piece_value][self.rotation]
        for part, move in zip(self.pos, rotation_matrix):
            part[0] = part[0] + move[0]
            part[1] = part[1] + move[1]
        self.rotation = (self.rotation + 1) % 4

    def __repr__(self):
        return f" value : {self.piece_value}"+f" position: {self.pos} \n"



