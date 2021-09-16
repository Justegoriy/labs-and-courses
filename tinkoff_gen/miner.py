import random

class SapperGame():

    size = (5, 5)
    bombs = random.randint(2, 5)
    flagged_bombs = None
    opened_cells = None
    current_field = []
    open_field = []

    def _change_parameters(self, size, bombs):
        self.size = tuple(map(int, input().split()))
        self.bombs = int(input())

    def _call_menu(self):
        pass
        return int(input())

    def _generate_field(self, first_try):
        for i in range(self.size[0]):
            self.current_field.append([])
            self.open_field.append([])
            for _ in range(self.size[1]):
                self.current_field[i].append('x')
                self.open_field[i].append(0)

        bombs_set = set()
        b = self.bombs
        first_position = (first_try[0] - 1) * self.size[1] + first_try[1] - 1
        bombs_set.add(first_position)
        first_top = first_position + self.size[1]
        first_bot = first_position - self.size[1]
        clear_positions = [first_position + 1, first_position - 1, first_top, first_top + 1, 
                            first_top - 1, first_bot, first_bot - 1, first_bot + 1]
        bombs_set.update(set(clear_positions))

        while b > 0:
            position = random.randint(0, self.size[0] * self.size[1] - 1)
            if position not in bombs_set:
                bombs_set.add(position)
                self.open_field[position // self.size[0]][position % self.size[1]] = 'b'
                b -= 1
            
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.open_field[i][j] != 'b':
                    for i_internal in range(i - 1, i + 2):
                        for j_internal in range(j - 1, j + 2):
                            if i_internal == -1 or i_internal == self.size[0] or j_internal == -1 or j_internal == self.size[1]:
                                continue
                            if self.open_field[i_internal][j_internal] == 'b':
                                self.open_field[i][j] += 1

    def _print_field(self, field):
        for i in range(self.size[0] + 2):
            for j in range(self.size[1] + 2):
                if i == 0 and j != 0 and j != 1:
                    print(j - 1, end=' ')
                elif i == 1 and j != 0 and j != 1:
                    print("-", end=' ')
                elif j == 0 and i != 0 and i != 1:
                    print(i - 1, end=' ')
                elif j == 1 and i != 0 and i != 1:
                    print("|", end=' ')
                elif i == 0 and j == 0 or i == 1 and j == 0 or i == 0 and j == 1:
                    print(" ", end=' ')
                elif i == 1 and j == 1:
                    print("+", end=' ')
                else:
                    print(field[i - 2][j-2], end=' ')
            if i != 0:
                print("|")
            else:
                print()
                

    def game_start(self):
        choice = self._call_menu()
        if choice == 1:
            print("В игре по умолчанию поле 5 на 5, на котором находится от 2 до 5 мин. Желаете изменит параметры игры? 1 - да, 2 - нет.")
            change_parameter_choice = int(input())
            if change_parameter_choice == 1:
                self._change_parameters()
            self.flagged_bombs = 0
            self.opened_cells = self.size[0] * self.size[1] - self.bombs
            print("Введите первые координаты")
            first_try = tuple(map(int, input().split()))
            self._generate_field(first_try)
            self._print_field(self.open_field)

game = SapperGame()
game.game_start()
