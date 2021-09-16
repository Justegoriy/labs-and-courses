import random
import os
import pickle

random.seed(0)

class SapperField():

    size = (5, 5)
    bombs = random.randint(2, 5)
    opened_cells = 0
    current_field = []
    open_field = []

    def change_parameters(self):
        print("Введите размер поля в формате [a b], где а - длина поля, b - ширина поля.")
        self.size = tuple(map(int, input().split()))
        print("Введите количество мин.")
        self.bombs = int(input())
        os.system('cls')

    def _generate_current_field(self):
        self.current_field = []
        for i in range(self.size[0]):
            self.current_field.append([])
            for _ in range(self.size[1]):
                self.current_field[i].append('x')

    def _generate_open_field(self, first_try):
        self.open_field = []
        for i in range(self.size[0]):
            self.open_field.append([])
            for _ in range(self.size[1]):
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
        for i in range(self.size[0] + 1):
            if i == 0:
                print(" ", end='')
            for j in range(self.size[1] + 1):
                if i == 0 and j != 0:
                    print(str(j).rjust(3), end='')
                elif j == 0 and i != 0:
                    print(str(i).ljust(3), end='')
                elif i != 0 and j != 0:
                    print(str(field[i - 1][j - 1]).center(2), end=' ')
            print()
        print(f"Мин установлено: {self.bombs}.\n")

    def _open_zero(self, x, y):
        self.current_field[x][y] = 0
        self.opened_cells += 1
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == -1 or i == self.size[0] or j == -1 or j == self.size[1] or i == x and j == y:
                    continue
                if self.current_field[i][j] == 'x' and self.open_field[i][j] != 'b':
                    if self.open_field[i][j] == 0:
                        self._open_zero(i, j)
                    else:
                        self.current_field[i][j] = self.open_field[i][j]
                        self.opened_cells += 1
        
    def game_play(self, new_game=True):
        os.system('cls')
        if new_game:
            self._generate_current_field()
            self._print_field(self.current_field)
            print("Введите координаты первой открытой клетки в формате [X Y],\nгде X и Y — координаты клетки на поле.")
            first_try = tuple(map(int, input().split()))
            self._generate_open_field(first_try)
            x = first_try[0] - 1
            y = first_try[1] - 1
            action = 'o'
        else: 
            input_str = self._game_input()
            if len(input_str) == 1:
                return None
            else:
                x = int(input_str[0]) - 1
                y = int(input_str[1]) - 1
                action = input_str[2]
        while True:
            os.system('cls')
            print(f"Введено: {x + 1} {y + 1} {action}")
            if self.current_field[x][y] == 'x' or self.current_field[x][y] == 'F':
                if action == 'o':
                    if self.open_field[x][y] == "b":
                        self.current_field[x][y] = 'b'
                        self._print_field(self.current_field)
                        print("Вы взорвались! Игра окончена!\n")
                        break
                    if self.open_field[x][y] == 0:
                        self._open_zero(x, y)
                    else:
                        self.current_field[x][y] = self.open_field[x][y]
                        self.opened_cells += 1
                elif action == 'f':
                    if self.current_field[x][y] == 'F':
                        print("Выбрана клетка с флагом. Введите новую команду.")
                    else:
                        self.current_field[x][y] = 'F'
                elif action == 'u':
                    if self.current_field[x][y] == 'x':
                        print("Выбрана клетка без флага. Введите новую команду.")
                    else:
                        self.current_field[x][y] = 'x'
            else:
                print("Выбрана уже открытая клетка. Введите координаты еще не открытой клетки.")
            if self.opened_cells == (self.size[0] * self.size[1]) - self.bombs:
                print("Победа! Вы разминировали поле!\n")
                self._print_field(self.current_field)
                break
            input_str = self._game_input()
            if len(input_str) == 1:
                return None
            else:
                x = int(input_str[0]) - 1
                y = int(input_str[1]) - 1
                action = input_str[2]
    
    def _game_input(self):
        self._print_field(self.current_field)
        print("Введите координтаты и команду в формате [X Y Действие],\nгде X и Y — координаты клетки на поле, а Действие – действие, которое необходимо совершить:")
        print("flag — установить флажок на соответвующую клетку, пометив её как предположительно содержащую бомбу;\nopen – раскрыть содержимое клетки; unflag - убрать флажок с клетки.")
        print("Введите menu для возврата в меню.")
        return input().split()


class SapperGame():

    game = None

    def _save_game(self):
        print("Введите название для файла сохранения. Файл будет создан автоматически.")
        name = './'  + input() + '.txt'
        with open(name, 'wb') as f:
            pickle.dump(self.game, f)

    def _load_game(self):
        print("Введите название файла сохранения.")
        with open(input(), 'rb') as f:
            self.game = pickle.load(f)
        self.game.game_play(new_game=False)

    def _call_menu(self):
        print('Добро пожаловать в "Сапер"')
        print("Введите 1 для старта новой игры. Все несохранненные данные будут удалены.")
        print("Введите 2 для загрузки игры. Все несохранненные данные будут удалены.")
        print("Введите 3 для сохранения текущей игры.")
        print("Введите 4 для ...")
        print("Введите 5 для выхода из игры. Все несохранненные данные будут удалены.")
        return int(input())

    def start(self):
        os.system('cls')

        while True:
            choice = self._call_menu()
            os.system('cls')
            if choice == 1:
                self.game = SapperField()
                print("По умолчанию установлено поле 5 на 5, на котором находится от 2 до 5 мин. Желаете изменит параметры игры? 1 - да, 2 - нет.")
                change_parameter_choice = int(input())
                os.system('cls')
                if change_parameter_choice == 1:
                    self.game.change_parameters()
                self.game.game_play()

            elif choice == 2:
                self._load_game()

            elif choice == 3:
                self._save_game()

            else:
                break

game = SapperGame()
game.start()
