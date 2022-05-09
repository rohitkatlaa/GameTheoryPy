from typing import Dict, List
from GameTheoryPy.SimpleGame import SimpleGame
from GameTheoryPy.IterativeGame import IterativeGame, SimpleIterativeGame
from GameTheoryPy.EvolutionaryGame import EvolutionaryGame
import numpy as np

def game1():
  """Prisoners' dilemma - a simple game"""
  agents = ["A", "B"]
  actions = ["Cooperate", "Defect"]
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }


  game = SimpleGame(agents, actions, payoff_function)
  print("The nash equilibrium states are:")
  print(game.calculate_nash_states())

def game2():
  """A simple game with three actions."""
  agents = ["A", "B"]
  actions = [0, 1, 2]
  payoff_function = {
    (0,0): [2,1],
    (0,1): [1,2],
    (0,2): [0,1],
    (1,0): [1,2],
    (1,1): [1,0],
    (1,2): [0,0],
    (2,0): [0,1],
    (2,1): [0,0],
    (2,2): [2,1]
  }


  game = SimpleGame(agents, actions, payoff_function)
  print("The nash equilibrium states are:")
  print(game.calculate_nash_states())

def game3():
  """A simple game with three agents."""
  # https://economics.stackexchange.com/questions/34297/pure-nash-equilibria-3-players-game
  
  agents = ["A", "B", "C"]
  actions = [0, 1]
  payoff_function = {
    (0,0,0): [70,70,70],
    (0,1,0): [10,10,23],
    (1,0,0): [60,0,0],
    (1,1,0): [60,65,10],
    (0,0,1): [70,70,60],
    (0,1,1): [10,20,0],
    (1,0,1): [80,50,30],
    (1,1,1): [60,55,5],
  }

  game = SimpleGame(agents, actions, payoff_function)
  print("The nash equilibrium states are:")
  print(game.calculate_nash_states())


def game4():
  """Prisoners' dilemma with neutral trust."""
  agents = ["A", "B"]
  actions = ["Cooperate", "Defect"]
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }
  belief_values = {
    "A": np.array([[0.5, 0.5]]),
    "B": np.array([[0.5, 0.5]])
  }
  initial_choices_prob = {
    "A": [1, 0],
    "B": [1, 0]
  }
  belief_update_value = 0.1
  iter_count = 10

  game = SimpleIterativeGame(agents, actions, payoff_function, belief_values, initial_choices_prob, belief_update_value, iter_count)
  game.play_game()


def game5():
  """Prisoners' dilemma with high trust."""
  agents = ["A", "B"]
  actions = ["Cooperate", "Defect"]
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }
  belief_values = {
    "A": np.array([[0.8, 0.2]]),
    "B": np.array([[0.8, 0.2]])
  }
  belief_update_value = 0.1
  iter_count = 10

  game = SimpleIterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


def game6():
  """ Stag Hare Hunt with neutral trust"""
  agents = ["A", "B"]
  actions = ["Stag", "Hare"]
  payoff_function = {
    ("Stag", "Stag"): [3,3],
    ("Stag", "Hare"): [0,2],
    ("Hare", "Stag"): [2,0],
    ("Hare", "Hare"): [2,2]
  }
  belief_values = {
    "A": np.array([[0.5, 0.5]]),
    "B": np.array([[0.5, 0.5]])
  }

  belief_update_value = 0.1
  iter_count = 10

  game = SimpleIterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


def game7():
  """ Stag Hare Hunt with high trust"""
  agents = ["A", "B"]
  actions = ["Stag", "Hare"]
  payoff_function = {
    ("Stag", "Stag"): [3,3],
    ("Stag", "Hare"): [0,2],
    ("Hare", "Stag"): [2,0],
    ("Hare", "Hare"): [2,2]
  }
  belief_values = {
    "A": np.array([[0.8, 0.2]]),
    "B": np.array([[0.8, 0.2]])
  }

  belief_update_value = 0.1
  iter_count = 10

  game = SimpleIterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


def game8():
  """ Stag Hare Hunt where one guy trusts and other doesn't trust."""
  agents = ["A", "B"]
  actions = ["Stag", "Hare"]
  payoff_function = {
    ("Stag", "Stag"): [3,3],
    ("Stag", "Hare"): [0,2],
    ("Hare", "Stag"): [2,0],
    ("Hare", "Hare"): [2,2]
  }
  belief_values = {
    "A": np.array([[0.8, 0.2]]),
    "B": np.array([[0.5, 0.5]])
  }

  belief_update_value = 0.1
  iter_count = 10

  game = SimpleIterativeGame(agents, actions, payoff_function, belief_values, None, belief_update_value, iter_count)
  game.play_game()


def IPD_tit_vs_alld():
  """This is a Iterated Prisoners' Dilemma game between TIT FOR TAT and ALL D strategy."""
  def tit_for_tat(player: str, player_list: List, history: Dict[str, List]):
    assert len(history.keys()) == 2
    
    if len(history[player]) == 0:
      return "Cooperate"
    else:
      opponent_player_list = [i for i in player_list if i != player]
      return history[opponent_player_list[0]][-1]

  def all_d(player: str, player_list: List, history: Dict[str, List]):
    return "Defect"

  agents = ["A", "B"]
  actions = ["Cooperate", "Defect"]
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }
  iter_count = 10
  strategy_function = {
    "A": tit_for_tat,
    "B": all_d,
  }
  game = IterativeGame(agents, actions, payoff_function, strategy_function, iter_count)
  game.play_game()


def IPD_tftt_vs_alld():
  """This is a Iterated Prisoners' Dilemma game between TIT FOR TAT and ALL D strategy."""
  def tit_for_two_tat(player: str, player_list: List, history: Dict[str, List]):
    assert len(history.keys()) == 2
    
    if len(history[player]) < 2:
      return "Cooperate"
    else:
      opponent_player = [i for i in player_list if i != player][0]
      if history[opponent_player][-1] == "Defect" and history[opponent_player][-2] == "Defect":
        return "Defect"
      return "Cooperate"

  def all_d(player: str, player_list: List, history: Dict[str, List]):
    return "Defect"

  agents = ["A", "B"]
  actions = ["Cooperate", "Defect"]
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }
  iter_count = 10
  strategy_function = {
    "A": tit_for_two_tat,
    "B": all_d,
  }
  game = IterativeGame(agents, actions, payoff_function, strategy_function, iter_count)
  game.play_game()


def SHH_tit_vs_allH():
  """This is a Iterated Prisoners' Dilemma game between TIT FOR TAT and ALL D strategy."""
  def tit_for_tat(player: str, player_list: List, history: Dict[str, List]):
    assert len(history.keys()) == 2
    
    if len(history[player]) == 0:
      return "Stag"
    else:
      opponent_player_list = [i for i in player_list if i != player]
      return history[opponent_player_list[0]][-1]

  def all_H(player: str, player_list: List, history: Dict[str, List]):
    return "Hare"

  agents = ["A", "B"]
  actions = ["Stag", "Hare"]
  payoff_function = {
    ("Stag", "Stag"): [3,3],
    ("Stag", "Hare"): [0,2],
    ("Hare", "Stag"): [2,0],
    ("Hare", "Hare"): [2,2]
  }
  iter_count = 10
  strategy_function = {
    "A": tit_for_tat,
    "B": all_H,
  }
  game = IterativeGame(agents, actions, payoff_function, strategy_function, iter_count)
  game.play_game()


def IPD_tft_vs_alld_evolutionary_game():

  def tit_for_tat(player: str, player_list: List, history: Dict[str, List]):
    assert len(history.keys()) == 2
    
    if len(history[player]) == 0:
      return "Cooperate"
    else:
      opponent_player_list = [i for i in player_list if i != player]
      return history[opponent_player_list[0]][-1]

  def all_d(player: str, player_list: List, history: Dict[str, List]):
    return "Defect"

  generations_count = 10
  game_count = 10
  iter_count = 50
  strategy_function = {
    "tit_for_tat": tit_for_tat,
    "all_d": all_d,
  }
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }
  agent_distribution = {
    "tit_for_tat": 10,
    "all_d": 90,
  }
  game = EvolutionaryGame(generations_count, game_count, iter_count, strategy_function, agent_distribution, payoff_function)
  game.simulate()


def IPD_tft_vs_alld_vs_ttft_evolutionary_game():

  def tit_for_tat(player: str, player_list: List, history: Dict[str, List]):
    assert len(history.keys()) == 2
    
    if len(history[player]) == 0:
      return "Cooperate"
    else:
      opponent_player_list = [i for i in player_list if i != player]
      return history[opponent_player_list[0]][-1]

  def all_d(player: str, player_list: List, history: Dict[str, List]):
    return "Defect"

  def tit_for_two_tat(player: str, player_list: List, history: Dict[str, List]):
    assert len(history.keys()) == 2
    
    if len(history[player]) < 2:
      return "Cooperate"
    else:
      opponent_player = [i for i in player_list if i != player][0]
      if history[opponent_player][-1] == "Defect" and history[opponent_player][-2] == "Defect":
        return "Defect"
      return "Cooperate"

  generations_count = 20
  game_count = 10
  iter_count = 10
  strategy_function = {
    "tit_for_tat": tit_for_tat,
    "all_d": all_d,
    "tit_for_two_tat": tit_for_two_tat
  }
  payoff_function = {
    ("Cooperate", "Cooperate"): [6,6],
    ("Cooperate", "Defect"): [0,10],
    ("Defect", "Cooperate"): [10,0],
    ("Defect", "Defect"): [1,1]
  }
  agent_distribution = {
    "tit_for_tat": 10,
    "all_d": 80,
    "tit_for_two_tat": 10
  }
  game = EvolutionaryGame(generations_count, game_count, iter_count, strategy_function, agent_distribution, payoff_function)
  game.simulate()


if __name__ == "__main__":
  # game1()
  # game2()
  # game3()
  # game4()
  # game5()
  # game6()
  # game7()
  # IPD_tit_vs_alld()
  # IPD_tftt_vs_alld()
  # SHH_tit_vs_allH()
  # IPD_tft_vs_alld_evolutionary_game()
  IPD_tft_vs_alld_vs_ttft_evolutionary_game()