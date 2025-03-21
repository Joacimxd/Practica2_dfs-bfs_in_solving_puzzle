import random
from concurrent.futures import ThreadPoolExecutor

class Sudoku:
    def __init__(self, n):
        self.n = n
        matrix = [[j + self.n*i for j in range(1,self.n+1)]for i in range(self.n)]
        matrix[self.n - 1][self.n - 1] = " "
        self.matrix = matrix
        self.matrix_solved = matrix
        self.space_idx_y = self.n - 1
        self.space_idx_x = self.n - 1

    def move_up(self):
        if self.space_idx_y == 0:
            return None
        new = self.clone()
        new.matrix[new.space_idx_y][new.space_idx_x], new.matrix[new.space_idx_y - 1][new.space_idx_x] = \
            new.matrix[new.space_idx_y - 1][new.space_idx_x], new.matrix[new.space_idx_y][new.space_idx_x]
        new.space_idx_y -= 1
        return new

    def move_down(self):
        if self.space_idx_y == self.n - 1:
            return None
        new = self.clone()
        new.matrix[new.space_idx_y][new.space_idx_x], new.matrix[new.space_idx_y + 1][new.space_idx_x] = \
            new.matrix[new.space_idx_y + 1][new.space_idx_x], new.matrix[new.space_idx_y][new.space_idx_x]
        new.space_idx_y += 1
        return new

    def move_left(self):
        if self.space_idx_x == 0:
            return None
        new = self.clone()
        new.matrix[new.space_idx_y][new.space_idx_x], new.matrix[new.space_idx_y][new.space_idx_x - 1] = \
            new.matrix[new.space_idx_y][new.space_idx_x - 1], new.matrix[new.space_idx_y][new.space_idx_x]
        new.space_idx_x -= 1
        return new

    def move_right(self):
        if self.space_idx_x == self.n - 1:
            return None
        new = self.clone()
        new.matrix[new.space_idx_y][new.space_idx_x], new.matrix[new.space_idx_y][new.space_idx_x + 1] = \
            new.matrix[new.space_idx_y][new.space_idx_x + 1], new.matrix[new.space_idx_y][new.space_idx_x]
        new.space_idx_x += 1
        return new

    def shuffle(self):
        for _ in range(50):
            movements = [self.move_down, self.move_left, self.move_up, self.move_right]
            move = random.choice(movements)()
            if move:
                self.matrix = move.matrix
                self.space_idx_x, self.space_idx_y = move.space_idx_x, move.space_idx_y

    def clone(self):
        new_sudoku = Sudoku(self.n)
        new_sudoku.matrix = [row[:] for row in self.matrix]
        new_sudoku.space_idx_x = self.space_idx_x
        new_sudoku.space_idx_y = self.space_idx_y
        return new_sudoku

    def __str__(self):
        numbers = "\n"
        for i in range(self.n):
            numbers += "|"
            for j in range(self.n):
                if len(str(self.matrix[i][j])) == 2:
                    numbers += " " + str(self.matrix[i][j]) + " "
                else:
                    numbers += " " + str(self.matrix[i][j]) + "  "
            numbers += "|\n\n"
        return numbers

    def to_tuple(self):
        return tuple(tuple(row) for row in self.matrix)

def dfs(sudoku, steps=[], visited=set(), max_calls=500, calls=0):
    estado_actual = sudoku.to_tuple()

    if calls >= max_calls:
        return None

    if sudoku.matrix == sudoku.matrix_solved:
        return steps

    if estado_actual in visited:
        return None

    visited.add(estado_actual)

    movimientos = [
        (sudoku.move_up(), "up"),
        (sudoku.move_down(), "down"),
        (sudoku.move_left(), "left"),
        (sudoku.move_right(), "right")
    ]

    for nuevo_estado, direccion in movimientos:
        if nuevo_estado:
            resultado = dfs(nuevo_estado, steps + [direccion], visited, max_calls, calls + 1)
            if resultado:
                return resultado

    return None


def dfs_thread(sudoku, max_calls=500):
    resultado = dfs(sudoku, [], set(), max_calls=max_calls)
    if resultado:
        print("Solución encontrada:", resultado)

def ejecutar_multithreading(sudoku, num_hilos=4, max_calls=500):
    with ThreadPoolExecutor(max_workers=num_hilos) as executor:
        for i in range(num_hilos):
            print(f"Iniciando hilo {i + 1}...")
            executor.submit(dfs_thread, sudoku, max_calls)

if __name__ == "__main__":
    sudoku = Sudoku(3)
    sudoku.shuffle()

    ejecutar_multithreading(sudoku, num_hilos=4, max_calls=500)
    

