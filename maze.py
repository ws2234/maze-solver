import random
from time import sleep
from cell import Cell


class Maze:
    def __init__(self, 
                 x1, 
                 y1, 
                 num_rows, 
                 num_cols, 
                 cell_size_x,
                 cell_size_y,
                 win,
                 seed=None,
                 ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.seed = seed
        if self.seed:
            self.seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._reset_cells_visted()

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j].visited = True
        while True:
            need_to_visit = []
            if i > 0 and not self._cells[i-1][j].visited:
                need_to_visit.append('left')
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                need_to_visit.append('right')
            if j > 0 and not self._cells[i][j-1].visited:
                need_to_visit.append('top')
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                need_to_visit.append('bottom')
            if need_to_visit:
                direction = random.choice(need_to_visit)
                if direction == 'left':
                    self._cells[i][j].has_left_wall = False
                    self._cells[i-1][j].has_right_wall = False
                    self._draw_cell(i, j)
                    self._break_walls_r(i-1, j)
                elif direction == 'right':
                    self._cells[i][j].has_right_wall = False
                    self._cells[i+1][j].has_left_wall = False
                    self._draw_cell(i, j)
                    self._break_walls_r(i+1, j)
                elif direction == 'top':
                    self._cells[i][j].has_top_wall = False
                    self._cells[i][j-1].has_bottom_wall = False
                    self._draw_cell(i, j)
                    self._break_walls_r(i, j-1)
                elif direction == 'bottom':
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i][j+1].has_top_wall = False
                    self._draw_cell(i, j)
                    self._break_walls_r(i, j+1)
            else:
                break

    def _reset_cells_visted(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r()

    def _solve_r(self, i=0, j=0):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        for direction in ["left", "right", "top", "bottom"]:
            if direction == "left" and i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
                self._cells[i][j].draw_move(self._cells[i-1][j])
                if self._solve_r(i-1, j):
                    return True
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
            elif direction == "right" and i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
                self._cells[i][j].draw_move(self._cells[i+1][j])
                if self._solve_r(i+1, j):
                    return True
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
            elif direction == "top" and j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
                self._cells[i][j].draw_move(self._cells[i][j-1])
                if self._solve_r(i, j-1):
                    return True
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
            elif direction == "bottom" and j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
                self._cells[i][j].draw_move(self._cells[i][j+1])
                if self._solve_r(i, j+1):
                    return True
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        


    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)

        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        sleep(0.05)
                
        