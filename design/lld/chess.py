import numpy as np


positions = {}
positions['Pawn']   = [[np.array([j, i]) for i in range(8)] for j in (1, 6)]
positions['Rook']   = [[np.array([j, i]) for i in (0, 7)] for j in (0, 7)]
positions['Knight'] = [[np.array([j, i]) for i in (1, 6)] for j in (0, 7)]
positions['Bishop'] = [[np.array([j, i]) for i in (2, 5)] for j in (0, 7)]
positions['Queen']  = [[np.array([j, i]) for i in (3, )] for j in (0, 7)]
positions['King']   = [[np.array([j, i]) for i in (4, )] for j in (0, 7)]

class GamePiece(object):
  def __init__(self):
    self.__position = None # Position of a piece
    self.__name = None # Name of the piece
    self.__symbol = None # Symbol representing piece
    self.__id = -1 # Piece ID
    self.__status = False # Alive: True, Dead: False
    self.__kills = []
  
  def __str__(self):
    return f"{self.get_name()}, position {self.get_position()}"
  
  def __eq__(self):
    if self.get_ID() == other.get_ID():
      if self.get_colour() == other.get_colour():
                return True
            else:
                return False
        else:
            return False
  
  # Getters and Setters
  def get_ID(self) -> int:
        return self.__id

    def set_ID(self, ID: int):
        self.__id = ID

    def get_position(self) -> np.array:
        return self.__position

    def set_position(self, position: np.array):
        self.__position = position

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_symbol(self) -> str:
        return self.__symbol

    def set_symbol(self, symbol: str):
        self.__symbol = symbol

    def get_colour(self) -> str:
        return self.__colour

    def set_colour(self, colour: str):
        self.__colour = colour

    def get_possible_moves(self, enemy_team):
        pass

    def get_inrange_enemies(self, enemy_team) -> list:
        pass

    def get_enemy_threats(self, enemy_team) -> list:
        pass
class Pawn(GamePiece):
  def __init__(self):
    GamePiece.__init__(self)
    self.set_name(name='Pawn')
    self.set_symbol(symbol='p')


class Rook(GamePiece):
  def __init__(self):
    GamePiece.__init__(self)
    self.set_name(name='Rook')
    self.set_symbol(symbol='R')


class Knight(GamePiece):
  def __init__(self):
    GamePiece.__init__(self)
    self.set_name(name='Knight')
    self.set_symbol(symbol='H')


class Bishop(GamePiece):
  def __init__(self):
    GamePiece.__init__(self)
    self.set_name(name='Bishop')
    self.set_symbol(symbol='B')


class Queen(GamePiece):
  def __init__(self):
    GamePiece.__init__(self)
    self.set_name(name='Queen')
    self.set_symbol(symbol='Q')


class King(GamePiece):
  def __init__(self):
    GamePiece.__init__(self)
    self.set_name(name='King')
    self.set_symbol(symbol='K')

# Team
class Team(Object):
  @staticmethod
  def __assign_ID(piece, ID):
    piece.set_ID(ID)
  def __init__(self):
    self.__alive_pieces = [
      King(), Queen(), Bishop(), Bishop(), Knight(), Knight(), Rook(), Rook(),
    ] + [Pawn() for _ in range(8)]
    self.__dead_pieces = []
    self.__possible_moves = {}
    self.__possible_attacks = {}
    self.__possible_threats = {}
    self.__colour = None
    self.__piece_ids = []
    self.assign_IDs(range(0, 16))
  
  def move_piece(self, ID, move):
    pass
  
  def get_all_of_a_type(self, which):
    return [piece for piece in self.get_all_pieces() if piece.get_name() == which]
  
  def get_all_pieces(self):
    return self.get_live_pieces() + self.get_dead_pieces()
  
  def get_live_pieces(self) -> list:
    return self.__alive_pieces
  
  def get_dead_pieces(self) -> list:
    return self.__dead_pieces
  def kill_piece(self, piece_id):
    for idx, piece_i in enumerate(self.get_live_pieces()):
      if piece_i == piece_id:
        self.get_dead_pieces().append(self.get_live_pieces().pop(idx))
        break
      else:
        continue
  
  def raise_piece_from_dead(self, piece_id):
    pass
  
  def add_live_piece(self, piece):
    self.get_live_pieces().append(piece)
  
  def get_colour(self) -> str:
    return self.__colour

  def set_colour(self, colour):
    self.__colour = colour
    for piece in self.get_all_pieces():
      piece.set_colour(self.__colour)
  
  def get_IDs(self) -> list:
    return self.__piece_ids
  def assign_IDs(self, IDs):
    for piece, ID in zip(self.get_live_pieces(), IDs):
      self.__piece_ids.append(ID)
      self.__assign_ID(piece, ID)
  
  def __calculate_possible_moves(self, enemy_team):
    for piece in self.get_live_pieces():
      self.__possible_moves[piece.get_ID()] = piece.get_possible_moves(enemy_team=enemy_team)

  def __calculate_enemy_threats(self, enemy_team):
    for piece in self.get_live_pieces():
      self.__possible_threats[piece.get_ID()] = piece.get_enemy_threats(enemy_team=enemy_team)

  def __calculate_possible_attacks(self, enemy_team):
    for piece in self.get_live_pieces():
      self.__possible_attacks[piece.get_ID()] = piece.get_inrange_enemies(enemy_team=enemy_team)

  def get_possible_moves(self, enemy_team):
    self.__calculate_possible_moves(enemy_team=enemy_team)
      return self.__possible_moves

  def get_possible_attacks(self, enemy_team):
    self.__calculate_possible_attacks(enemy_team=enemy_team)
      return self.__possible_attacks

  def get_possible_threats(self, enemy_team):
    self.__calculate_enemy_threats(enemy_team=enemy_team)
      return self.__possible_threats

class WhiteTeam(Team):
  def __init__(self):
    Team.__init__(self)
    self.set_colour('White')

class BlackTeam(Team):
  def __init__(self):
    Team.__init__(self)
    self.set_colour('Black')
    
class Board(object):
  def __init__(self, team1, team2):
    self.__coordinates = np.zeros((8, 8))
    self.__teams = {'T1': team_1, 'T2': team_2}
    self.__assemble_board()
  def __assemble_board(self):
    for idx_1, team in enumerate(self.get_teams().values()):
      for kind in positions.keys():
        for idx_2, item in enumerate(team.get_all_of_a_type(kind)):
          position = positions[kind][idx_1][idx_2]
          item.set_position(position)
          self.__coordinates[position[0], position[1]] = item.get_ID()
  
  def move_piece(self, team, ID, move):
    pass
  
  def print_coordinates(self):
    print(self.__coordinates)
  
  def get_cordinates(self):
    return self.__coordinates
  
  def getTeams(slef):
    return self.__teams
  
if __name__ == "__main__":
  team1 = BlackTeam()
  team2 = WhiteTeam()
  board = Board(team1, team2)
  board.print_coordinates()
    