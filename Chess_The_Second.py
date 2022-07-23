def convertmove(m):
    if m == 'exit': raise EndOfTheGaem
    return (7 - (ord(m[0].upper()) - ord('A') ), int(m[1]) - 1)

def generator(num, times):
    for i in range(times):
        yield num

class Team():
    side = 0
    enemy = 0
class White(Team):
    side = -1
    enemy = 1
class Black(Team):
    side = 1
    enemy = -1

class Battlefield():
    def __init__(self):
        self.field = [ [Space() for i in range(8)] for j in range(8)]
        self.field[0] = [Rook(Black), Horse(Black), Elephant(Black),
                         Queen(Black), King(Black),
                         Elephant(Black), Horse(Black), Rook(Black)]
        self.field[1] = [Pawn(Black)] * 8
        self.field[-1] = [Rook(White), Horse(White), Elephant(White),
                          Queen(White), King(White), Elephant(White),
                          Horse(White), Rook(White)]
        self.field[-2] = [Pawn(White)] * 8

        for i, line in enumerate(self.field):
            for j, figure in enumerate(line):
                figure.x = i
                figure.y = j

    def __repr__(self):
        s = ''
        for i, line in enumerate(self.field):
            s += str(i + 1)  +  '| '
            for fig in line:
                if fig.__class__  == Space:
                    s += ' '
                elif fig.__class__ == Move:
                    s += str(fig) + ' '
                else:
                    s += fig.__class__.__name__[0] + ' '
            s += '\n'
        s += '   ________________'
        s += '\n   H G F E D C B A\n'
        return s
    
    def get_figure(self, current):
        while True:
            try:
                figure = convertmove(input('Enter coords of cel with figure u want 2 move: [LD]\nL - Letter, D - Digit\n'))
                dfigure = self.field[figure[1]][figure[0]]
                if dfigure.team != current: raise WrongCell
            except WrongCell:
                pass
            except (IndexError, ValueError):
                WrongCell()
            else:
                break
        dfigure.x = figure[1]
        dfigure.y = figure[0]
        return dfigure
    
    def clear(self):
        for i, line in enumerate(self.field):
            for j, cell in enumerate(line):
                if cell.__class__ == Move:
                    self.field[i][j] = self.field[i][j].figure
                    
    def make_move(self):
        while True:
            try:
                move = convertmove(input('Enter coords of move:\n'))
                if move[1] < 0:
                    self.clear()
                    raise Cancel
                move = move[1], move[0]
                if not move in moves:
                    raise WrongMove
                self.clear()
                self.field[move[0]][move[1]] = chosen
                self.field[chosen.x][chosen.y] = Space()
                moved = self.field[chosen.x][chosen.y]
                moved.x = chosen.x
                moved.y = chosen.y
            except WrongMove: pass
            except (IndexError, ValueError):
                WrongMove()
            else:
                break
        print(self)

    def find_king(self, king_team):
        for i, x in enumerate(self.field):
            for j, y in enumerate(x):
                if y.__class__ == King and y.team == king_team:
                    return y
        

    
class ChessException(Exception): pass

class EndOfTheGaem(ChessException):
    def __init__(self):
        
        print('King is dead\n')
        
class WrongCell(ChessException):
     def __init__(self):
         
         print('There\'s no your figure!\n')
         
class WrongMove(ChessException):
    def __init__(self):
        vls()
        print('U can\'t move your figure there!\n')
        
class PawnOnTheEdge(ChessException):
    def __init__(self):
        
        print('Pawn became another figure!\n')
        
class Cancel(ChessException): pass

class Shah(ChessException):
    def __init__(self):
        print('ШАХ')




class Figure(Battlefield):
    
    def __init__(self, team):
        self.team = team
        
    def __repr__(self):
        if self.__class__ == Space:
            return ''
        return self.__class__.__name__[0]
    
    def underAttack(self, battlefield, team, mode = 'common'): #team - под атакой какой команды 
        x = self.x
        y = self.y
        s = team.side
        show = battlefield.field    
        attackers = []

        if mode == 'common':
            return Rook.show_moves(self, battlefield, 'check',team = team ) or Horse.show_moves(self, battlefield, mode = 'check', team = team) or Elephant.show_moves(self, battlefield, mode = 'check', team = team)
        if mode == 'WhoAttack':
            attackers += Rook.show_moves(self, battlefield, 'WhoAttack', team)
            attackers += Pawn.show_moves(self, battlefield, 'WhoAttack', team)
            attackers += Elephant.show_moves(self, battlefield, mode = 'WhoAttack', team = team)
            attackers += Horse.show_moves(self, battlefield, mode  = 'WhoAttack', team = team)
            attackers += King.show_moves(self, battlefield, mode = 'WhoAttack', team = team)
            return attackers

class Space(Figure):
    def __init__(self):
        self.side = 0
        self.team = Team()

        
class Pawn(Figure):
    def show_moves(self, battlefield, mode ='common', team = 0):
        x = self.x
        y = self.y
        show = battlefield.field
        moves = []
        s = self.team.side

        if mode == 'WhoAttack':
            attackers = []
            show = battlefield.field[:][:]
        
        if not x in range(0, 8):
            raise PawnOnTheEdge #Если пешка уперлась в край доски        

        if show[x + s][y].__class__ == Space:
            show[x + s][y] = Move(show[x + s][y])
            moves.append((x + s, y))

        if y - 1 >= 0 and show[x + s][y - 1].team.side == self.team.enemy:
            if mode == 'common':
                show[x + s][y - 1] = Move(show[x + s][y - 1])
                moves.append((x + s, y - 1))
            if mode == 'WhoAttack' and team == show[x + s][y - 1].team:
                attackers.append(show[x + s][y - 1])

        if y + 1 < 8 and show[x + s][y + 1].team.side == self.team.enemy:
            if mode == 'common':
                show[x + s][y + 1] = Move(show[x + s][y + 1])
                moves.append((x + s, y + 1))
            if mode == 'WhoAttack'and show[x + s][y + 1].team == team:
                attackers.append(show[x + s][y + 1])

        if x == 6 and self.team == White:
            if show[x - 2][y].__class__ == Space:
                show[x - 2][y] = Move(show[x - 2][y])
                moves.append((x - 2, y))

        if x == 1 and self.team == Black:
            if show[x + 2][y].__class__ == Space:
                show[x + 2][y] = Move(show[x + 2][y])
                moves.append((x + 2, y))

        if mode == 'common':
            
            print(battlefield)
            return moves
        if mode == 'WhoAttack':
            return attackers


class Rook(Figure):
    def show_moves(self, battlefield, mode = 'common', AddMoves = -1, AddShow = -1, team = 0):
        x = self.x
        y = self.y
        check = [zip(range(x + 1, 8), generator(y, 7 - x)),
                 zip(range(x - 1, -1, -1), generator(y, x)),
                 zip(generator(x, 7 - y), range(y + 1, 8)),
                 zip(generator(x, y), range(y - 1, -1, -1))]

        if AddMoves == -1:
            moves = []
        else:
            moves = AddMoves
            
        if AddShow == -1:
            show = battlefield.field
        else:
            show = AddShow
            
        if mode == 'check':
            show = battlefield.field[:][:]
        if mode == 'WhoAttack':
            attackers = []
            show = battlefield.field[:][:]

           
        for gen in check:
            for i, j in gen:
                cell = show[i][j]
                if (cell.__class__ == Rook or cell.__class__ == Queen) and cell.team == team:
                    if mode == 'check':
                        return True
                    if mode == 'WhoAttack':
                        attackers.append(cell)
                        break
                if cell.__class__ == Space or cell.team.side == self.team.enemy:
                    if mode == 'common' or mode == 'additional':
                        show[i][j] = Move(cell)
                        moves.append((i, j))
                    if cell.team.side == self.team.enemy:
                        break
                else: break

        if mode == 'common':
            
            print(battlefield)
            return moves
        elif mode == 'additional':
            return moves, show
        elif mode == 'check':
            return False
        elif mode == 'WhoAttack':
            return attackers

        
class Horse(Figure):
    def show_moves(self, battlefield, mode = 'common', team = 0): #team - команда, чьи фигуры надо чекать если mode == 'check'
        check = [(-2, 1), (-2, -1), (2, 1),
                 (2, -1), (1, 2), (-1, 2),
                 (1, -2), (-1, -2)]
        x = self.x
        y = self.y
        moves = []
        if mode == 'common':
            show = battlefield.field
        elif mode == 'check':
            show = battlefield.field[:][:]
        elif mode == 'WhoAttack':
            show = battlefield.field[:][:]
            attackers = []

        for i, j in check:
            try:
                if x + i < 0 or y + j < 0: raise IndexError
                
                cell = show[x + i][y + j]
                if cell.__class__ == Horse and cell.team == team:
                    if mode == 'check':
                        return True
                    if mode == 'WhoAttack':
                        attackers.append(cell)
                elif mode == 'common'  and (cell.__class__ == Space or cell.team.side == self.team.enemy):
                    show[x + i][y + j] = Move(cell)
                    moves.append((x + i, y + j))
            except IndexError:
                pass
            
        if mode == 'common':
            
            print(battlefield)
            return moves
        elif mode == 'check':
            return False
        elif mode == 'WhoAttack':
            return attackers


class Elephant(Figure):
    def show_moves(self, battlefield, team = 0, mode = 'common',  AddMoves = -1, AddShow = -1):
        x = self.x
        y = self.y
        check = [ (range(1, 8), range(1, 8)), (range(1, 8), range(-1, -7, -1)),
                  (range(-1, -7, -1), range(1, 8)), (range(-1, -7, -1), range(-1, -7, -1)) ]
        
        if AddMoves == -1:
            moves = []
        else:
            moves = AddMoves
        if AddShow == -1:
            show = battlefield.field
        else:
            show = AddShow
            
        if mode == 'check':
            show = battlefield.field[:][:]
        if mode == 'WhoAttack':
            attackers = []
            show = battlefield.field[:][:]
        
        for a, b in check:
            for i, j in zip(a, b):
                try:
                    if x + i < 0 or y + j < 0: raise IndexError
                    
                    cell = show[x + i][y + j]
                    if cell.team == team and (cell.__class__ == Queen or cell.__class__ == Elephant):
                        if mode == 'check':
                            return True
                        if mode == 'WhoAttack':
                            attackers.append(cell)
                            break
                    if mode == 'common' and (cell.__class__ == Space or cell.team.side == self.team.enemy):
                        show[x + i][y + j] = Move(cell)
                        moves.append((x + i, y + j))
                    if cell.__class__ != Space:
                        break
                except IndexError:
                    pass
        if mode == 'common':
            
            print(battlefield)
            return moves
        elif mode == 'check':
            return False
        else:
            return moves, show

    
class Queen(Figure):
    def show_moves(self, battlefield):
        AMoves, AShow = Rook.show_moves(self, battlefield, 'additional')
        return Elephant.show_moves(self, battlefield, 0, 'common', AMoves, AShow)

    
class King(Figure):
    def show_moves(self, battlefield, mode = 'common', team = 0):
        x = self.x
        y = self.y
        moves = []
        if mode == 'common':
            show = battlefield.field
        elif mode == 'check':
            show = battlefield.field[:][:]
        elif mode == 'WhoAttack':
            show = battlefield.field[:][:]
            attackers = []
        if self.team == White:
            enemy = Black
        else:
            enemy = White
        try:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0 or x + i < 0 or y + j < 0: continue
                    try:
                        cell = show[x + i][y + j]
                        if not cell.underAttack(battlefield, enemy) and (cell.__class__ == Space or cell.team == enemy):
                            if mode == 'common':
                                show[x + i][y + j] = Move(cell)
                                moves.append((x + i, y + j))
                            if mode == 'WhoAttack':
                                attackers.append(cell)
                                raise ChessException
                    except IndexError: pass
        except ChessException:
            pass

        if mode == 'common':
            
            print(battlefield)
            return moves
        if mode == 'WhoAttack':
            return attackers
                
                
class Move(Figure):
    def __init__(self, figure):
        self.figure = figure
        self.team = figure.team
    def __repr__(self):
        if self.figure.__class__ == Space:
            return 'X'
        return self.figure.__repr__().lower()


waiting = Black
current = White
battlefield = Battlefield()
print(battlefield)


while True:
    try:
        chosen = battlefield.get_figure(current)
        moves = chosen.show_moves(battlefield)
        
        battlefield.make_move()
        print(battlefield)
        
        """Найти короля. Если король под ударом и есть свободные клетки, - шах
           Если король под ударом, свободных нет, но фигура, бьющая короля под ударом - шах
           Если король под ударом, свободных нет, фигура, бьющая короля - одна:
                   можно закрыться - шах
                   нельзя - мат
            бьющих фигур >= 2: мат"""
        
        king = battlefield.find_king(waiting)
        condition = king.underAttack(battlefield, current)
        if condition:
            raise Shah
        print(condition)
    except Shah:
        if len(king.show_moves(battlefield, 'WhoAttack')) == 0:
            attackers = king.underAttack(battlefield, current, 'WhoAttack')
            
            if len(attackers) > 1:
                break
            
            attacker = attackers[0]
            if attacker.underAttack(battlefield, waiting, 'WhoAttack'):
                print('SHAH!')
            else:
                break
    except EndOfTheGaem:
        break
    except ChessException:
        pass
    finally:
        current, waiting = waiting, current
print(' и МАТ!\nКоманда', current.__name__, "выиграла!")
