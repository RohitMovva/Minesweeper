from tkinter import *
import random
from tkinter import messagebox


class Coordinate:
    def __init__(self, x, y):
        """
        :param x: x coord
        :param y: y coord
        """
        self.x = x
        self.y = y

    def change(self, x, y):
        """
        :param x: x coord
        :param y: y coord
        :return: replaces the x and y coords
        """
        self.x = x
        self.y = y

    def getx(self):
        """
        :return: x coord
        """
        return self.x

    def gety(self):
        """
        :return: y coord
        """
        return self.y

    def __str__(self):
        """
        :return: string version of the object
        """
        return "(" + str(self.x) + " " + str(self.y) + ")"

    def issame(self, coord):
        """
        :param coord: Coordinate object
        :return: if self and coord are the same
        """
        if self.x == coord.getx() and self.y == coord.gety():  # checks if x coord and y coord are the same
            return True
        return False


class MinesweeperCell(Button):

    def __init__(self, master, coord, adjacents, adjacentList, isBomb):
        """
        :param master: MinesweeperGrid object
        :param coord: Coordinate object
        :param adjacents: number of adjacent bombs
        :param adjacentList: list of all adjacent MinesweeperCells
        :param isBomb: if self is a bomb
        """
        Button.__init__(self, master, height=1, width=3, text='',
                        bg='white', font=('Arial', 24), relief=RAISED)

        self.bind("<Button-1>", self.clear)
        self.bind("<Button-2>", self.set_bomb)
        self.bind("<Button-3>", self.set_bomb)
        # button

        self.coord = coord
        self.adjacents = adjacents
        self.isBomb = isBomb
        self.colermap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'balck', 'dim gray']
        self.adjacentList = adjacentList
        self.relief = 'stressed'
        # variables

    def clear(self, filler):
        """
        :param filler: empty parameter (got an error without a second param)
        :usage: clears itself (event triggered on left click)
        """
        if self.isBomb:  # loses if bomb
            self.master.lose()

        else:
            self['bg'] = self.colermap[8]
            self.unbind('<Button-1>')
            self.unbind('<Button-3>')

            if not self.adjacents == 0:
                self['text'] = self.adjacents
                self['disabledforeground'] = self.colermap[self.adjacents]
            # case for squares with adjacents

            if (self.adjacents == 0) and (self['state'] != DISABLED):
                self.master.square_cleared(self)
                self['relief'] = SUNKEN
                self.relief = 'relieved'
                self['state'] = DISABLED
                self['text'] = ''
                # case for squares with no adjacents and disabled

                self.master.clear(self.adjacentList)
            elif self['state'] != DISABLED:
                self.master.square_cleared(self)
                self['relief'] = SUNKEN
                if self.adjacents == 0:
                    self['text'] = ''
                self['state'] = DISABLED
            # case for squares that aren't disabled

    def set_bomb(self, filler):
        """
        :param filler: empty parameter (got an error without a second param)
        :usage: sets the square as a bomb
        """
        bombMarkers = self.master.get_bombs()  # number of bomb markers left

        if self['text'] == '*':
            self['text'] = ''
            self['state'] = NORMAL
            self.master.regenerate_bomb(self)
            self.master.square_regen(self)
        # case if already flagged

        elif bombMarkers > 0:
            self['text'] = '*'
            self['state'] = DISABLED
            self.master.delete_bomb(self)
            self.master.square_cleared(self)
        # case if there is still a bomb marker to place

    def is_bomb(self):
        """
        :return: if self is a bomb
        """
        if self.isBomb:
            return True
        return False

    def disable(self, bomb):
        """
        :param bomb: reveals unrevealed bombs
        :usage: disabling square on loss
        """
        if bomb:
            self.unbind('<Button-1>')
            self.unbind('<Button-3>')
            self['state'] = DISABLED

            self['relief'] = RAISED
            self['bg'] = self.colermap[3]
            self['text'] = '*'
        # case for bomb
        else:
            self.unbind('<Button-1>')
            self.unbind('<Button-3>')
            self['state'] = DISABLED

    def getx(self):
        """
        :return: x coord
        """
        return self.coord.getx()

    def gety(self):
        """
        :return: y coord
        """
        return self.coord.gety()


class MinesweeperGrid(Frame):

    def __init__(self, master, rows, columns, bombs):
        """
        :param master: root
        :param rows: number of rows
        :param columns: number of columns
        :param bombs: number of bombs
        """
        Frame.__init__(self, master, bg='black')
        self.grid()
        self.rowconfigure(rows + 1, minsize=1)
        self.bombs = bombs
        self.bombNumFrame = Frame(self, bg='white')  # new frame to hold buttons
        Label(self.bombNumFrame, text=self.bombs).grid(row=0, column=0)
        self.bombNumFrame.grid(row=columns, column=0, columnspan=rows)
        # visual setup

        self.colermap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']
        self.cells = {}  # set up dictionary for cells
        self.rows = rows
        self.columns = columns
        self.coords = []
        self.toGo = rows * columns
        # attributes

        xnums = [i for i in range(1, rows + 1)]
        ynums = [i for i in range(1, columns + 1)]
        bombList = []
        skip = False
        iteration = 0
        # variables

        while True:
            iteration += 1
            coord = Coordinate(random.choice(xnums), random.choice(ynums))
            for i in range(len(bombList)):
                if bombList[i].issame(coord):
                    skip = True
            if skip:
                skip = False
                continue
            bombList.append(coord)
            if len(bombList) >= bombs:
                self.bombList = bombList
                break
        # generates bombs

        for row in range(1, rows + 1):
            for column in range(1, columns + 1):
                coord = Coordinate(column, row)
                self.coords.append(coord)
                # makes a coord for the square

                adjacents = 0

                above = Coordinate(column, coord.gety() + 1)
                below = Coordinate(column, coord.gety() - 1)
                left = Coordinate(coord.getx() - 1, row)
                right = Coordinate(coord.getx() + 1, row)
                topLeft = Coordinate(coord.getx() - 1, coord.gety() + 1)
                topRight = Coordinate(coord.getx() + 1, coord.gety() + 1)
                bottomLeft = Coordinate(coord.getx() - 1, coord.gety() - 1)
                bottomRight = Coordinate(coord.getx() + 1, coord.gety() - 1)
                # all adjacent squares
                adjacentList = [above, below, left, right, topLeft, topRight, bottomLeft, bottomRight]
                isBomb = False

                for i in range(0, len(bombList)):
                    if coord.issame(bombList[i]):
                        isBomb = True
                        adjacents = -1
                # if square is a bomb

                if not isBomb:
                    for i in range(len(bombList)):
                        for j in range(len(adjacentList)):
                            if adjacentList[j].issame(bombList[i]):
                                adjacents += 1

                # finds all adjacent bombs

                self.cells[str(coord)] = MinesweeperCell(self, coord, adjacents, adjacentList, isBomb)
                # cells go in even-numbered rows/columns of the grid
                self.cells[str(coord)].grid(row=row - 1, column=column - 1)

        self.constantCoords = self.coords  # non-changing version of coords

    def delete_bomb(self, square):
        """
        :param square: square that got marked as a bomb
        :usage: removes a bomb marker
        """
        self.bombs -= 1
        Label(self.bombNumFrame, text=self.bombs).grid(row=0, column=0)
        coord = Coordinate(square.getx(), square.gety())

        for i in range(0, len(self.bombList)):
            if coord.issame(self.bombList[i]):
                self.bombList.remove(self.bombList[i])
                break

    def regenerate_bomb(self, square):
        """
        :param square: square that got unmarked as a bomb
        :usage: regenerates a bomb marker
        """
        self.bombs += 1
        Label(self.bombNumFrame, text=self.bombs).grid(row=0, column=0)
        self.bombList.append(square)

    def win(self):
        """
        :usage: carries out the sequence after the player wins the game
        """
        messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)

        for i in range(0, len(self.bombList)):
            self.cells[str(self.bombList[i])].disable(False)

    def lose(self):
        """
        :usage: carries out the sequence after the player loses the game
        """
        messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
        for i in range(0, len(self.constantCoords)):
            self.cells[str(self.constantCoords[i])].disable(False)
        # disables all cells
        for i in range(0, len(self.bombList)):
            self.cells[str(self.bombList[i])].disable(True)
        # disables all bombs and highlights them

   
    def square_regen(self, square):
        """
        :param square: square to regenerate
        :usage: regenerates a square (in the context of squares till winning the game)
        """
        coord = Coordinate(square.getx(), square.gety())
        self.coords.append(coord)

    def square_cleared(self, square):
        """
        :param square: square that got cleared
        :usage: removes the square (in the context of squares till winning the game)
        """
        coord = Coordinate(square.getx(), square.gety())

        for i in range(0, len(self.coords)):
            if coord.issame(self.coords[i]):
                self.coords.remove(self.coords[i])
                break

        if len(self.coords) == 0:
            self.win()

    def get_bombs(self):
        """
        :return: number of bomb markers left
        """
        return self.bombs


def minesweeper():
    """minesweeper()
    plays minesweeper"""
    grid_size = 100
    # defaults rows and columns so the while loop will be entered

    while grid_size > 15:
        grid_size = int(input("Grid size (1-15)? "))
        if grid_size > 15 or grid_size < 1:
            print("please enter a value less than or equal to 15")
        else:
            break

    # both must be less than 15 for all the squares to show
    rows = grid_size
    columns = grid_size
    bombs = int(input("Number of bombs? "))
    root = Tk()
    root.title('MineSweeper')
    sg = MinesweeperGrid(root, rows, columns, bombs)
    root.mainloop()


minesweeper()  # plays minesweeper!
